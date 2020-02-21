#!/usr/bin/env python3

import click
import time
from pathlib import Path
from tabulate import tabulate
import attr
import pickle
import os

from backend import Backend
from filehandler import FileHandler
from containers import *

size = None

@click.group()
def main():
    pass


# TODO
@main.group()
def inwards():
    pass


@inwards.command()
@click.option("--user")
def overview(user: str):
    if user is not None:
        print(FileHandler.server_overview_of(user))
    else:
        print(FileHandler.server_storage_status())


def wait_and_print_overviews(backend: Backend) -> None:
    print("Loading...", end=" ", flush=True)
    time.sleep(1)
    print("Done. Your overviews:\n")
    overviews = backend.get_overviews()
    if len(overviews) > 0:
        ds = [attr.asdict(o) for o in overviews]
        print(tabulate(ds, headers="keys"))
    else:
        print("No overviews had been received.")
    print()

@main.group(invoke_without_command=True)
@click.option("--username", prompt=True)
@click.option("--debug", is_flag=True)
@click.pass_context
def outwards(ctx, username, debug):
    ctx.obj = Backend(username, debug=debug)
    wait_and_print_overviews(ctx.obj)


@outwards.command()
def listen():
    while True:
        time.sleep(0.33)


@outwards.command()
@click.pass_obj
def who_around(backend: Backend):
    backend.out_status_broadcast()
    wait_and_print_overviews(backend)


@outwards.command()
@click.argument("filepath", type=Path)
@click.argument("to_who")
@click.pass_obj
def upload(backend: Backend, filepath: Path, to_who: str):
    agent = AgentHandler.get_agent(to_who.encode("ascii", "replace"))
    if agent is None:
        print(f"No such agent with name '{to_who}' is found.")
    else:
        with open(filepath, "r") as f:
            data = f.read(30)
        print(f"Uploading file {filepath.name} to '{to_who}' with data like:\n{ data }...")
        if not backend.out_upload(agent, filepath):
            print("Not successful!")
    print()


@outwards.command()
@click.argument("filename")
@click.argument("from_who")
@click.argument("to_where", type=Path)
@click.pass_obj
def download(backend: Backend, to_where: Path, from_who: str, filename: str):
    agent = AgentHandler.get_agent(from_who.encode("ascii", "replace"))
    if agent is None:
        print(f"No such agent with name '{from_who}' is found.")
        return
    sent = backend.out_download(agent, filename, to_where)
    if not sent:
        print(f"Couldn't send the download command.")
        return
    print(f"Downloading file {filename} from '{from_who}' into:\n{ to_where }...")
    print(f"\nPlease wait until your download is ", end=" ")
    time.sleep(1)
    print("Done. Your file is: ")
    with to_where.open("rb") as f:
        print(f.read(40))
    print()

@outwards.command()
@click.argument("old_filename")
@click.argument("new_filename")
@click.argument("from_who")
@click.pass_obj
def rename(backend: Backend, old_filename: str, new_filename: str, from_who: str):
    agent = AgentHandler.get_agent(from_who.encode("ascii", "replace"))
    if agent is None:
        print(f"No such agent with name '{from_who}' is found.")
        return
    sent = backend.out_rename(agent, old_filename, new_filename)
    if not sent:
        print(f"Couldn't send the rename command.")
        return
    print(f"Rename file {old_filename} to {new_filename}")

@outwards.command()
@click.argument("filename")
@click.argument("from_who")
@click.pass_obj
def delete(backend: Backend, filename: str, from_who: str):
    agent = AgentHandler.get_agent(from_who.encode("ascii", "replace"))
    if agent is None:
        print(f"No such agent with name '{from_who}' is found.")
        return 
    sent = backend.out_delete(agent, filename)
    if not sent:
        print(f"Couldn't send the delete command.")
        return
    print(f"File {filename} is deleted.")

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

if __name__ == "__main__":
    dict = __unpickling__()
    if  dict == {}:
        size = input("Select size for storage: ")
        while not size or int(size) < 100000 :
            os.system('clear')
            size = input("Please select valid size for storage or greater than 100000: ")
        dict = {"size": int(size)}
        __pickling__(dict)
    else:
        size =  dict["size"]
    main()
