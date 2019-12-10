#!/usr/bin/env python3
#ulimit -Sn 10000

import sys
import time
import os
import socket
import time
from _thread import *
from threading import Timer
import threading
import subprocess
import os
import pandas as pd
import pickle
import select


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    class fg: 
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg: 
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

class PythonChat :
    __total_unread__ = 0
    __all_users__ = {}
    __store_messages__ = {}
    __handle_announce__ = {}

    def __init__(self, __username__, __port__):
        self.__username__ = __username__
        self.__ip__ = self.get_ip()
        self.__network__ = self.__ip__[:self.__ip__.rfind('.')]
        self.__port__ = __port__

    def send_packet(self, __ip__, __port__, __packet__):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((__ip__, __port__))
                s.send(__packet__.encode('ascii', 'replace'))
                s.close()
        except:
            pass

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            __IP__ = s.getsockname()[0]
        except:
            __IP__ = '127.0.0.1'
        finally:
            s.close()
        return __IP__

    def show_profile(self):
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        print("\n\n\n  Username: " + "\033[0;27;46m " + self.__username__ + " \x1b[0m" + "\n")
        print("  Your IP: " + "\033[0;27;46m " + self.__ip__ + " \x1b[0m" + "\n")
        print("  Your Network: " + "\033[0;27;46m " + self.__network__ + " \x1b[0m" + "\n")
        self.yellow_flag("[->]", "Press enter key to go main page...")

    def broadcast_thread(self):
        __broadcast_thread__ = threading.Thread(target=self.broadcast_network)
        __broadcast_thread__.setDaemon(True)
        __broadcast_thread__.start()

    def broadcast_network(self):
        while True:
            __control__ = 3
            while __control__:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    tmp_username = "[" + self.__username__ 
                    tmp_ip = " " + self.__ip__
                    __packet__ = ','.join([tmp_username, tmp_ip, " announce]"])
                    self.write_file("broadcast_log.txt", __packet__)
                    s.bind(('', 0))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    try:
                        s.sendto(__packet__.encode('ascii', 'replace'), ('<broadcast>', self.__port__))
                        __control__-=1
                    except Exception:
                        continue
                    s.close()
                time.sleep(0.25)
            time.sleep(60)    

    def what_to_do_thread(self):
        print(" \033[100F \033[2K \r" + "\033[0;01m " + "[->] " +  " \033[1;47;42m " + self.__username__ + "\x1b[0m" 
                                                                            + "\033[0;37;42m" + ", welcome again." + " \x1b[0m", end="")
        __what_to_do_thread__ = threading.Thread(target=self.what_to_do)
        __what_to_do_thread__.setDaemon(True)
        __what_to_do_thread__.start()

    def what_to_do(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.__ip__, self.__port__))
            s.listen()
            while True:
                conn, addr = s.accept()
                data = conn.recv(2048)
                if not data:
                    break
                __request__ = str(data.decode('ascii', 'replace'))
                try:
                    __sender_name__, __sender_ip__, __sender_type__, *__message_packet__ = __request__[1:-1].split(",")
                    __sender_name__ = __sender_name__.strip()
                    __sender_ip__ = __sender_ip__.strip()
                    __sender_type__ = __sender_type__.strip()

                    if __sender_type__ == "message":
                        if __sender_name__ not in self.__all_users__:
                            continue
                        else:
                            self.green_flag("[!]", __sender_name__, "has sent new message.")
                            self.__all_users__[__sender_name__][2]+=1
                            self.__total_unread__+=1
                            __message_packet__ = __sender_name__ + ": " + str(*__message_packet__).strip() + "\n"
                            if __sender_name__ not in self.__store_messages__ :
                                self.__store_messages__[__sender_name__] = [__message_packet__]
                            else :
                                self.__store_messages__[__sender_name__].append(__message_packet__)

                    elif __sender_type__ == "response":
                        if __sender_name__ not in self.__all_users__:
                            self.__all_users__[__sender_name__] = [__sender_ip__, __sender_name__, 0]
                        else:
                            self.__all_users__[__sender_name__][1] = __sender_name__
                        self.green_flag("[!]", __sender_name__, "is online")

                    elif __sender_type__ == "announce":
                        if __sender_name__ in self.__handle_announce__:
                            if self.__handle_announce__[__sender_name__] == 3:
                                self.__handle_announce__[__sender_name__]=1
                                self.green_flag("[!]", __sender_name__, "has opened chat")
                                tmp_username = "[" + self.__username__ 
                                tmp_ip = " " + self.__ip__
                                __packet__ = ','.join([tmp_username, tmp_ip, " response]"])
                                start_new_thread(self.send_packet, (__sender_ip__, self.__port__, __packet__))
                            else:
                                self.__handle_announce__[__sender_name__]+=1
                        else:
                            self.__handle_announce__[__sender_name__]=1
                            self.green_flag("[!]", __sender_name__, "has opened chat")
                            tmp_username = "[" + self.__username__ 
                            tmp_ip = " " + self.__ip__
                            __packet__ = ','.join([tmp_username, tmp_ip, " response]"])
                            start_new_thread(self.send_packet, (__sender_ip__, self.__port__, __packet__))
                    else:
                        self.write_file("error_log.txt", "Unknown packet from %s\n" % __sender_ip__)
                except ValueError:
                    self.write_file("error_log.txt", "Unknown packet from %s\n" % __sender_ip__)
                conn.close()
            s.close()

    def udp_what_to_do_thread(self):
        __udp_what_to_do_thread__ = threading.Thread(target=self.udp_what_to_do)
        __udp_what_to_do_thread__.setDaemon(True)
        __udp_what_to_do_thread__.start()

    def udp_what_to_do(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', self.__port__))
            s.setblocking(0)
            while True:
                result = select.select([s], [], [])
                data = result[0][0].recv(1024)
                if not data:
                    break
                __request__ = str(data.decode('ascii', 'replace'))
                try:
                    __sender_name__, __sender_ip__, __sender_type__, *__message_packet__ = __request__[1:-1].split(",")
                    __sender_name__ = __sender_name__.strip()
                    __sender_ip__ = __sender_ip__.strip()
                    __sender_type__ = __sender_type__.strip()
                    if __sender_ip__ != self.__ip__:
                        if __sender_type__ == "announce":
                            if __sender_name__ in self.__handle_announce__:
                                if self.__handle_announce__[__sender_name__] == 3:
                                    self.__handle_announce__[__sender_name__]=1
                                    self.green_flag("[!]", __sender_name__, "has opened chat")
                                    tmp_username = "[" + self.__username__ 
                                    tmp_ip = " " + self.__ip__
                                    __packet__ = ','.join([tmp_username, tmp_ip, " response]"])
                                    start_new_thread(self.send_packet, (__sender_ip__, self.__port__, __packet__))
                                else:
                                    self.__handle_announce__[__sender_name__]+=1
                            else:
                                self.__handle_announce__[__sender_name__]=1
                                self.green_flag("[!]", __sender_name__, "has opened chat")
                                tmp_username = "[" + self.__username__ 
                                tmp_ip = " " + self.__ip__
                                __packet__ = ','.join([tmp_username, tmp_ip, " response]"])
                                start_new_thread(self.send_packet, (__sender_ip__, self.__port__, __packet__))
                        else:
                            self.write_file("error_log.txt", "Unknown packet from %s\n" % __sender_ip__)
                except ValueError:
                    self.write_file("error_log.txt", "Unknown packet from %s\n" % __sender_ip__)
            s.close()

    def notifications(self):
        if self.__total_unread__ == 0:
            self.red_flag("[!]", "You have no notification")
            print("\033[0;01;34m" + "\n\n      Press any key to main page..." +  "\033[0;37;40m" , end = "")
            tmp = input()
            os.system('clear')
        else:
            self.green_flag("[->]", "", "New notifications from: ")
            print("\n")
            for k, v in self.__all_users__.items():
                if self.__all_users__[k][2] != 0 :
                    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
                    __string__ = "(" + str(self.__all_users__[k][2]) + " unread message" + ")"
                    print( " " + bcolors.BOLD + self.__all_users__[k][1] + bcolors.ENDC 
                                            + "\033[5;01;34m " + __string__ + "\033[0;37;40m" , end ="")
                    print("\n " +  "-" * 35)
                else :
                    continue

            print("\033[0;01;34m" + "\n\n If you want to show, please enter yes: " +  "\033[0;37;40m" , end = "")
            __yes_no__ = input()

            if __yes_no__.lower() == "yes" :
                print("\033[0;01;34m" + "\n Select user who send message(Just enter go main page): " +  "\033[0;37;40m" , end = "")
                __notify_user__ = input()
                
                if __notify_user__ == "":
                    os.system('clear')
                elif __notify_user__ not in self.__all_users__:
                    self.red_flag("[!]", "You chose invalid user. Press any key to continue...")
                    tmp = input()
                    os.system('clear')
                    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
                    self.list_online_user()
                    print("\n")
                    print("\033[0;01;34m" + "\n\nSelect valid user or go main page: " +  "\033[0;37;40m" , end = "")
                    __notify_user__ = input()

                    if __notify_user__ != "" :
                        if __notify_user__ in self.__all_users__:
                            self.send_message_packet(__notify_user__, self.__all_users__[__notify_user__][0])
                        else :
                            selection()
                    else :
                        selection()
                else :
                    self.send_message_packet(__notify_user__, self.__all_users__[__notify_user__][0]) 
            else :
                self.red_flag("[!]", "Press enter key to go main page...")
                tmp = input()
                selection

    def send_message_packet(self, __target_user_name__, __target_user_ip__):
        os.system('clear')
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        print('\n\n')
        if __target_user_name__ in self.__store_messages__ :
            for items in self.__store_messages__[__target_user_name__] :
                print(items)

            self.__total_unread__-=self.__all_users__[__target_user_name__][2]
            self.__all_users__[__target_user_name__][2] = 0

        else:
            self.red_flag("[!]","You do not have any message with ",__target_user_name__)
        
        print("\033[0;01;34m" + "\n\n\n\n\n\n\nEnter your message: " +  "\033[0;37;40m" , end = "")
        __message__ = input()
        if __message__ != "" :
            __message_packet__ = self.__username__ + ": " + __message__ + "\n"
            if __target_user_name__ not in self.__store_messages__ :
                self.__store_messages__[__target_user_name__] = [__message_packet__]
            else :
                self.__store_messages__[__target_user_name__].append(__message_packet__)
            tmp_username = "[" + self.__username__ 
            tmp_ip = " " + self.__ip__
            __message__ = " " + __message__ + "]"
            __packet__ = ','.join([tmp_username, tmp_ip, " message", __message__])
            start_new_thread(self.send_packet, (__target_user_ip__, self.__port__, __packet__))
            self.send_message_packet(__target_user_name__, __target_user_ip__)
        else :
            self.red_flag("[!]","Write e to go main page or else to continue...")
            __key__ = input()
            if __key__ == "e":
                selection
            else :
                self.send_message_packet(__target_user_name__, __target_user_ip__)

    def start_chat(self):
        if not bool(self.__all_users__):
            self.red_flag("[!]","There are no online user to contact.")
            print("\033[0;01;34m" + "\n\n      Press any key to main page..." +  "\033[0;37;40m" , end = "")
            tmp = input()
            os.system('clear')
        else :
            self.list_online_user()
            print("\033[0;01;34m" + "\n\nEnter username(Write SIGEXIT to go main page): " +  "\033[0;37;40m" , end = "")
            __target_user_name__ = input()
            if __target_user_name__ == 'SIGEXIT' :
                selection()
            else:
                if __target_user_name__ not in self.__all_users__ :
                    self.red_flag("[!]","Please enter valid username")
                    tmp = input()
                    os.system('clear')
                    self.start_chat()
                else :
                    self.send_message_packet(__target_user_name__, self.__all_users__[__target_user_name__][0])

    def write_file(self, file, str):
        f= open(file,'a')
        f.write(str)
        f.write('\n')
        f.close()

    def list_online_user(self):
        self.yellow_flag("[->]", "You see avaliable online users below")
        print("\n\n")
        __header__ = "AVALIABLE USER"
        print(__header__.center(46, ' '))
        print('=' * 46)
        print('| {0:s}  {1:s}|'.format("NAME".ljust(21), "IP".ljust(21)))
        print('-' * 46)
        for __elem__ in sorted(self.__all_users__.items()):
            print('| {0:s}  {1:s}|'.format(__elem__[0].ljust(21), __elem__[1][0].ljust(21)))
            print('-' * 46)

    def red_flag(self, __punctuation__, __str__, __optional__=""):
        print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[0;37;41m " + __str__ + " \x1b[0m" 
                                                                            + "\033[1;30;41m" + __optional__ + " \x1b[0m", end="")

    def yellow_flag(self, __punctuation__, __str__, __optional__=""):
        print("\033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[0;37;43m " + __str__ + " \x1b[0m" 
                                                                            + "\033[1;47;43m" + __optional__ + " \x1b[0m", end="")

    def green_flag(self, __punctuation__, __str__, __optional__=""):
        print("\033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[1;47;42m " + __str__ + " \x1b[0m" 
                                                                            + "\033[0;37;42m " + __optional__ + " \x1b[0m", end="")
        
class Switcher(object):
    def indirect(self,i):
        __method_name__ = 'number_' + str(i)
        __method__ = getattr(self, __method_name__, lambda :'Invalid option')
        return __method__()

    def number_1(self):
        os.system('clear')
        chat.show_profile()
        tmp = input()
        os.system('clear')

    def number_2(self):
        os.system('clear')
        chat.list_online_user()
        chat.yellow_flag("[->]","Press enter key to go main page...")
        tmp = input()
        os.system('clear')
        
    def number_3(self):
        os.system('clear')
        chat.start_chat()

    def number_4(self):
        os.system('clear')
        chat.notifications()

    def number_5(self):
        os.system('clear')
        __pickling__(chat.__store_messages__)
        chat.yellow_flag("[!]","Thank you for using this application dear",__username__)
        print("\n")
        sys.exit(0)

def __pickling__(__list__):
    with open("store.txt", "wb") as fp:   # Pickling
        pickle.dump(__list__, fp)

def __unpickling__():
    if os.path.isfile("store.txt") :
        if os.path.getsize("store.txt") > 0 :
            with open("store.txt", "rb") as fp :   # Unpickling
                b = pickle.load(fp)
            return b
    else :
        dict = {}
        f=open("store.txt", "w+")
        return dict

def selection():
    os.system('clear')  
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __header__ = "SELECTION"
    print("\n\n")
    print(__header__.center(48, ' '))
    print('=' * 48)
    print('| {0:s}  {1:s}|'.format("1)".ljust(17), "Show My Information".ljust(26)))
    print('| {0:s}  {1:s}|'.format("2)".ljust(17), "List Online User".ljust(26)))
    print('| {0:s}  {1:s}|'.format("3)".ljust(17), "Send Message".ljust(26)))
    __string__ = ""
    if chat.__total_unread__ == 0 or chat.__total_unread__ == 1 :
        __string__ = "(" + str(chat.__total_unread__) + " message" + ") "
    else :
        __string__ = "(" + str(chat.__total_unread__) + " messages" + ")"
    print("| 4)                 Notifications" + "\033[5;01;34m " + __string__  + "\033[0;37;40m" + "|" )
    # print('-' * 42)
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    print('| {0:s}  {1:s}|'.format("5)".ljust(17), "Quit".ljust(26)))
    print('=' * 48)
    
    print("\033[0;01;34m " + "\n\nType the selection you want to: " +  "\033[0;37;40m" , end = "")
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __selection__ = input()
    try:
        val = int(__selection__)
        if val > 5 :
            chat.red_flag("[!]","Please choose valid selection...")
            tmp = input()
        else :                                                        
            s = Switcher()
            s.indirect(__selection__)
    except ValueError:
        chat.red_flag("[!]","Please choose valid selection...")
        tmp = input()
    

if os.path.isfile("broadcast_log.txt"):
    os.remove("broadcast_log.txt")
if os.path.isfile("error_log.txt"):
    os.remove("error_log.txt")

os.system('clear')
__username__ = ""

while not __username__:
    try:
        print(" \033[100F \033[2K" + "\033[0;01m \r " + "[.]" +  "  \033[0;37;43m " + "Please write your user name" + "\x1b[0m" 
                                                                            + "\033[1;35;43m " + "" + " \x1b[0m", end="")
        print("\033[0;01;34m" + "\n\n      Write Username: "  "\033[0;37;40m" , end = "")
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        __username__ = input()
        os.system('clear')
        if not __username__:
            raise SyntaxError('Please write valid input. Enter to continue.')
    except SyntaxError as e:
        print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + "[!]" +  "  \033[0;37;41m " + str(e) + " \x1b[0m" 
                                                                            + "\033[1;30;41m" + "" + " \x1b[0m", end="")
        tmp = input()
        os.system('clear')

chat = PythonChat(__username__, 12345)
chat.__store_messages__ = __unpickling__()
chat.show_profile()
tmp = input()
os.system('clear')
chat.broadcast_thread()
chat.what_to_do_thread()
chat.udp_what_to_do_thread()
time.sleep(1.5)

while True:
    selection()
