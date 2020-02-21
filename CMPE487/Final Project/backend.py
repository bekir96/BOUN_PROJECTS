import socket
from threading import Thread
import sys

from filehandler import FileHandler
from containers import *


class ListenerTCP(Thread):
    def __init__(self, address: Address, f_tcp_recv):
        super(ListenerTCP, self).__init__()
        self.daemon = True
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(address)
            self.s.listen(5)
        except socket.error as e:
            print('Failed to create TCP socket', file=sys.stderr)
            print(e, file=sys.stderr)
            print(f"{address}", file=sys.stderr)
            sys.exit(1)
        self.f_tcp_recv = f_tcp_recv

    def run(self):
        while True:
            conn, addr = self.s.accept()
            with conn:
                parts = list()
                while True:
                    part = conn.recv(500)
                    if not part:
                        break
                    parts.append(part)
                data = b"".join(parts)
                self.f_tcp_recv(data, addr[0])


class ListenerUDP(Thread):
    def __init__(self, address: Address, f_udp_recv):
        super(ListenerUDP, self).__init__()
        self.daemon = True
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind(address)
        except socket.error as e:
            print('Failed to create UDP socket', file=sys.stderr)
            print(e, file=sys.stderr)
            print(f"{address}", file=sys.stderr)
            sys.exit(1)
        self.f_udp_recv = f_udp_recv

    def run(self):
        while True:
            data, addr = self.s.recvfrom(30)
            self.f_udp_recv(data, addr[0])


class Backend:
    # TODO same port
    PORT_TCP = 8888
    PORT_UDP = 9999

    def __init__(self, username: str, debug: bool):
        self.debug = debug
        self.listener_tcp = ListenerTCP(Address(self.get_ip(), self.PORT_TCP), self._f_tcp_recv)
        self.listener_tcp.start()
        self.listener_udp = ListenerUDP(Address('', self.PORT_UDP), self._f_tcp_recv)
        self.listener_udp.start()

        self.username = username.encode("ascii", "replace")[:10]
        self.username_str = username
        self.out_status_broadcast()

        self.overviews_since_request: List[Overview] = list()

    @staticmethod
    def get_ip() -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                ip = s.getsockname()[0]
            except:
                ip = '127.0.0.1'
        return ip

    @property
    def _padded_name(self) -> bytes:
        return self.username.ljust(10, b"\0")

    def _f_tcp_recv(self, data: bytes, ip: str):
        """
        upload ex: bekir\0\0\0\0\0\x00\x00Ufilename.txt\0this is a file\n

        Bounded 10-byte \0 padded from right username at the beginning
        Then one char command type

        [S] Status    -
        [U] Upload    filename\0bytestring
        [D] Download  filename
        [R] Rename    oldfilename\0newfilename
        [X] Delete    filename
        [O] Overview  json
        [P] Payload   filename\0bytestring
        [F] Failure   bjson
        [ ] Success
        """
        if len(data) < 11:
            print(f"header is not whole {data.decode()}", file=sys.stderr)
            return

        user = data[:10].rstrip(b"\0")
        if user == self.username:
            return
        agent = Agent(name=user, ip=ip)
        agent_instead = AgentHandler.none_if_proper(agent)
        """
        if agent_instead is not None:
            # TODO handle error
            # call out_failure
            print(f"There is an agent like this: {agent_instead}", file=sys.stderr)
            return
        """
        command = data[10:11]
        payload = data[11:]
        if command == b'S':
            self._inc_status(agent)
            return
        else:
            tokens = payload.split(b"\0", maxsplit=1)
            if command == b"U":
                if len(tokens) != 2:
                    return
                self._inc_upload(agent, *tokens)
            elif command == b"F":
                if len(tokens) != 1:
                    return
                self._inc_failure(agent, tokens[0])
            elif command == b"O":
                if len(tokens) != 1:
                    return
                self._inc_overview(agent, tokens[0])
            elif command == b"D":
                if len(tokens) != 1:
                    return
                self._inc_download(agent, tokens[0])
            elif command == b"P":
                if len(tokens) != 2:
                    return
                self._inc_payload(agent, *tokens)
            elif command == b"R":
                if len(tokens) != 2:
                    return
                self._inc_rename(agent, *tokens)
            elif command == b"X":
                if len(tokens) != 1:
                    return
                self._inc_delete(agent, tokens[0])
            else:
                print("Unknown command:", data)

    def _inc_status(self, agent: Agent) -> None:
        """
        Creates overview for the user, sends it.
        """
        ov = FileHandler.server_overview_of(agent.name.decode("ascii", "replace"), self.username_str)
        if ov is not None:
            self._send_tcp(b"O" + ov.to_bjson(), agent.ip)
        else:
            self.out_failure(agent, Fail(ErrorType.OVERVIEW))

    def out_status(self, agent: Agent) -> bool:
        # Sends STATUS command to agent.
        self.overviews_since_request = list()
        return self._send_tcp(b"S", agent.ip)
    
    def out_status_broadcast(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try:
                packet = self._padded_name + b"S"
                s.sendto(packet, ("<broadcast>", self.PORT_UDP))
                self.overviews_since_request = list()
                return True
            except:
                return False

    def _inc_upload(self, agent: Agent, filename: bytes, data: bytes) -> None:
        s_name = filename.decode("ascii", "replace")
        success = FileHandler.server_file_put(agent.name.decode("ascii", "replace"), s_name, data)
        if not success:
            self.out_failure(agent, Fail(ErrorType.PUT, filename=s_name))

    def out_upload(self, agent: Agent, filepath: Path, filename: Optional[bytes] = None) -> bool:
        data = FileHandler.client_file_read(filepath)
        if data is None:
            return False
        if filename is None:
            filename = filepath.name.encode("ascii", "replace")
        packet = b"U" + filename + b"\0" + data
        return self._send_tcp(packet, agent.ip)

    def _inc_overview(self, agent: Agent, bjson: bytes) -> None:
        try:
            overview = Overview.from_bjson(bjson)
            self.overviews_since_request.append(overview)
        except:
            self.out_failure(agent, Fail(error=ErrorType.PARSE, filename=None))

    def out_overview(self, agent: Agent, overview: Overview) -> bool:
        return self._send_tcp(b"O" + overview.to_bjson(), agent.ip)

    def get_overviews(self) -> List[Overview]:
        return self.overviews_since_request

    def _inc_failure(self, agent: Agent, bjson: bytes) -> None:
        try:
            fail_obj = Fail.from_bjson(bjson)
            print(f"FAIL from {agent.name.decode('ascii', 'replace')}", file=sys.stderr)
            print(fail_obj, file=sys.stderr)
        except:
            print(f"FAIL from {agent.name.decode('ascii', 'replace')}", file=sys.stderr)
            print(f"Could not parse fail obj", file=sys.stderr)
            print(bjson, file=sys.stderr)
            self.out_failure(agent, Fail(error=ErrorType.PARSE, filename=None))
            return

    def out_failure(self, agent: Agent, fail: Fail) -> bool:
        return self._send_tcp(b"F"+fail.to_bjson(), agent.ip)

    def _inc_download(self, agent: Agent, filename: bytes) -> None:
        s_name = filename.decode("ascii", "replace")
        data = FileHandler.server_file_get(agent.name.decode("ascii", "replace"), s_name)
        if data is not None:
            self.out_payload(agent, filename, data)
        else:
            self.out_failure(agent, Fail(ErrorType.GET, filename=s_name))

    def out_download(self, agent: Agent, filename: str, path: Path) -> bool:
        DownloadHandler.add_download(agent, filename, path)
        return self._send_tcp(b"D" + filename.encode("ascii", "replace"), agent.ip)

    def _inc_payload(self, agent: Agent, filename: bytes, payload: bytes) -> None:
        s_name = filename.decode("ascii", "replace")
        path = DownloadHandler.resolve_download(agent, s_name)
        if path is None:
            return
        success = FileHandler.client_file_write(path, payload)
        if not success:
            self.out_failure(agent, Fail(ErrorType.DOWNLOAD, s_name))
            DownloadHandler.add_download(agent, s_name, path)

    def out_payload(self, agent: Agent, filename: bytes, payload: bytes) -> bool:
        return self._send_tcp(b"P"+filename+b"\0"+payload, agent.ip)

    def _inc_rename(self, agent: Agent, old_filename: bytes, new_filename: bytes) -> bool:
        old_name = old_filename.decode("ascii", "replace")
        new_name = new_filename.decode("ascii", "replace")
        success = FileHandler.server_file_rename(agent.name.decode("ascii", "replace"), old_name, new_name)
        if not success:
            self.out_failure(agent, Fail(error=ErrorType.GET, filename=old_name))

    def out_rename(self, agent: Agent, old_filename: str, new_filename: str) -> bool:
        return self._send_tcp(b"R" + old_filename.encode("ascii", "replace") + b"\0" + new_filename.encode("ascii", "replace"), agent.ip)

    def _inc_delete(self, agent: Agent, filename: bytes):
        s_name = filename.decode("ascii", "replace")
        success = FileHandler.server_file_delete(agent.name.decode("ascii", "replace"), filename)
        if not success:
            self.out_failure(agent, Fail(error=ErrorType.GET, filename=s_name))  

    def out_delete(self, agent: Agent, filename: str) -> bool:
        return self._send_tcp(b"X" + filename.encode("ascii", "replace"), agent.ip)

    def _send_tcp(self, data: bytes, ip: str) -> bool:
        socket_timeout = 2
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(socket_timeout)  # seconds
            try:
                s.connect((ip, self.PORT_TCP))
            except Exception as e:
                print(e, file=sys.stderr)
                return False
            else:
                try:
                    packet = self._padded_name + data
                    s.sendall(packet)
                    return True
                except Exception as e:
                    print(e, file=sys.stderr)
                    return False


"""
    def _inc_download(self, user: bytes, filename: bytes):
        pass

    def _inc_rename(self, addr: Address, old_filename: bytes, new_filename: bytes):
        pass
    
    def _inc_delete(self, addr: Address, filename: bytes):
        pass

    def _inc_overview(self, addr: Address, pickled: bytes):
        pass
    
    def _inc_payload(self, addr: Address, data: bytes):
        pass

    
    THIS IS IMPORTANT! AgentHandler and DownloadHandler must be notified of related errors!
    def _inc_failure(self, addr: Address, fail_str: bytes, pickled: bytes):
        pass
"""
