#!/usr/bin/env bash

# Remote IP
ip_rem=rpi.local
user_rem=pi

# Local path
path_local=/home/egeme/code/egemenbekir/

# RPi path
path_remote=/home/$user_rem/prog/peer_drive

rsync -avzhP --exclude-from="./sync_exclude" -e ssh $path_local $user_rem@$ip_rem:$path_remote