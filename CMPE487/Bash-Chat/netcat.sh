#!/usr/local/bin/bash

USER_NAME=""
MY_IP=""
MY_NETWORK=""
NOTIFY_TXT=notifications.txt

show_profile(){
    if [ -z "$MY_IP" ]; 
    then
        printf "Please check your network connection"
        sleep 3 
        exit
    else
        printf "\n\n  Username: $USER_NAME\n"
        printf "  Your IP: $MY_IP\n"
        printf "  Your Network: $MY_NETWORK\n\n"
    fi
} 

broadcastNetwork(){
    while [ true ];do
        for i in $(seq 1 254);do
            local change_ip="$MY_NETWORK.$i"
            if [ "$MY_IP" != "$change_ip" ]
            then
                echo "[$USER_NAME, $MY_IP, announce]" | nc -G 1 "$change_ip" 12345 &
                echo "[$USER_NAME, $change_ip, announce]" >> broadcast_log.txt
            fi
        done 
        sleep 10
    done
}

what_to_do(){
    # nc -l -k 12345
    while [ true ]; 
    do
        local request=$(nc -l 12345)
        local sender_name=$(echo "$request" | sed 's/[][]//g' | cut -d ',' -f 1 | sed 's/ //g')
        local sender_ip=$(echo "$request" | sed 's/[][]//g' | cut -d ',' -f 2 | sed 's/ //g') 
        local sender_type=$(echo "$request" | sed 's/[][]//g' | cut -d ',' -f 3 | sed 's/ //g')
        echo "$request" >> "asdddd.txt"
        if [ "$sender_type" == "message" ] 
        then
            local message_packet=$(echo "$request" | sed 's/[][]//g' | cut -d ',' -f 4)
            echo "$sender_name: $message_packet" "at $(date):" >> "$sender_name.txt"
            if [ ! -f "$NOTIFY_TXT" ] ; then
                touch $NOTIFY_TXT
            fi
            if grep -q $sender_name "$NOTIFY_TXT" ; then
                continue
            else
                echo "$sender_name" "$sender_ip" >> "$NOTIFY_TXT"
            fi
        elif [ "$sender_type" == "response" ] 
        then
            echo "$sender_name" "$sender_ip"  >> online_user.txt 
        elif [ "$sender_type" == "announce" ] 
        then
            echo "[$USER_NAME, $MY_IP, response]" | nc -G 1 "$sender_ip" 12345  &
        fi
    done
}

notifications(){
    if [ ! -s "$NOTIFY_TXT" ]
    then
        printf "You have no notification\n"
        read -n 1 -s -r -p "Press any key to go main page..."
        selection
    else
        printf "\n\n  New notifications from: "
        while IFS= read line
        do
            printf "$(echo "$line" | cut -d ' ' -f 1) "
        done <"$NOTIFY_TXT"
        
        printf "\n  If you want to show, please enter yes: "
        read -r yes_no
        # Look uppercase lowercase situation
        if [ "$yes_no" == "yes" ]
        then
            local notify_user            
            printf "\n  Select user who send message(Just enter go main page): "
            read -r notify_user
            if [ ${#notify_user} -eq 0 ];then
                    selection
            elif ! grep -q $notify_user "$NOTIFY_TXT"
            then
                printf "\n  You chose invalid user."
                read -n 1 -s -r -p "Press any key to continue..."
                clear
                
                divider===============================
                divider=$divider$divider
                header="\n %22s \n"
                format=" %s %-17s %-10s\n"
                width=41
                pad=$(printf '%0.1s' "_"{1..17})

                printf "$header" "AVALIABLE USER"
                printf "%$width.${width}s\n" "$divider"

                while IFS= read line
                do
                    printf "$(echo "$line" | cut -d ' ' -f 1) "
                done <"$NOTIFY_TXT"
                
                printf "\n\nSelect valid user or go main page: "
                read -r notify_user
                if [ ! ${#notify_user} -eq 0 ] 
                then
                    if  grep -q $notify_user "$NOTIFY_TXT"
                    then
                        local target_ip=$(grep $notify_user $NOTIFY_TXT | cut -d ' ' -f 2)
                        send_message_packet "$notify_user" "$target_ip"
                    else
                        selection
                    fi
                else
                    selection
                fi
            else
                local target_ip=$(grep $notify_user $NOTIFY_TXT | cut -d ' ' -f 2)
                send_message_packet "$notify_user" "$target_ip"
            fi
        else 
            read -n 1 -s -r -p "  Press any key to go main page..."
            selection
        fi
    fi
}

send_message_packet(){
    clear

    local target_user_name=$1
    local target_ip=$2

    if [ ! -f "$target_user_name.txt" ]
    then
        printf "\n\nYou do not have any message with $target_user_name"
    else
        echo "$(< $target_user_name.txt)"
        sed -i '' "/$target_user_name/d" notifications.txt
    fi

    printf "\n\nEnter your message: \n"
    read -r message

    if [ ! ${#message} -eq 0  ]
    then
        echo "$USER_NAME: $message" "at $(date):" >> "$target_user_name.txt"
        echo "[$USER_NAME, $MY_IP, message, $message]" | nc -G 2 "$target_ip" 12345 &
        send_message_packet "$target_user_name" "$target_ip"
    else
        printf "\nWrite e to go main page or else to continue...\n"
        read -r key
        if [ "$key" == "e" ]
        then
            selection
        else
            send_message_packet "$target_user_name" "$target_ip"
        fi
    fi
}

start_chat(){
    pad=$(printf '%0.1s' "-"{1..60})
    printf '%*.*s' 0 $((4)) "$pad"
    printf " SELECT ONLINE USER WITH USERNAME "
    printf '%*.*s' 0 $((4)) "$pad"
    var=0

    if [ ! -f "online_user.txt" ]
    then
        printf "\n\n!!! There are no online user to contact. !!!\n\n"
        read -n 1 -s -r -p "Press any key to main page..."
        selection
    else
        divider===============================
        divider=$divider$divider
        header="\n\n %22s \n"
        width=41
        padding=$(printf '%0.1s' "_"{1..60})
        padlength=53
        printf "$header" "Online users:"
        printf "%$width.${width}s\n" "$divider"

        cat "online_user.txt" |  sort -u -t. -k 4n | while read -r user ; do
            var=$((var+1))
            printf '%d' "$var"
            printf '%*.*s' 0 $((padlength - ${#var} - ${#user} )) "$padding"
            printf "%s\n" "$(echo "$user" | cut -d" " -f1)" 
        done

        printf "\n\nEnter username(Write SIGEXIT to go main page): "
        read -r target_user_name

        if [ "$target_user_name" == "SIGEXIT" ]
        then
            selection
        else
            if [ ${#target_user_name} -eq 0 ] 
            then
                printf "\n\nPlease enter valid username\n"
                read -n 1 -s -r -p "Press any key to enter new username..."
                clear
                start_chat
            else
                if ! grep -q $target_user_name "online_user.txt" 
                then
                    printf "\n\nPlease enter valid username\n"
                    read -n 1 -s -r -p "Press any key to enter new username..."
                    clear
                    start_chat
                else
                    local target_ip=$(grep "$target_user_name" "online_user.txt" | cut -d " " -f 2)
                    send_message_packet "$target_user_name" "$target_ip"
                fi
            fi
        fi
    fi
}

list_online_user(){
    if [ ! -s "online_user.txt" ]
    then
        printf "\n\n!!! There are no online user to contact. !!!\n\n"
    else
        divider===============================
        divider=$divider$divider
        header="\n\n %22s \n"
        width=41
        padding=$(printf '%0.1s' "_"{1..60})
        padlength=49
        printf "$header" "Online users:"
        printf "%$width.${width}s\n" "$divider"

        cat "online_user.txt" | sort -u |  while read -r list_user; do
            printf " Name: "
            printf "$(echo "$list_user" | cut -d " " -f 1)"
            printf ", IP: "
            printf "$(echo "$list_user" | cut -d " " -f 2)\n"
        done

        printf "\n "
    fi

}

kill(){
    pgrep bash && killall bash 
}

selection(){
    clear

    divider===============================
    divider=$divider$divider
    header="\n %22s \n"
    format=" %s %-17s %-10s\n"
    width=41
    pad=$(printf '%0.1s' "_"{1..17})

    printf "$header" "SELECTION"
    printf "%$width.${width}s\n" "$divider"
    printf "$format" \
    "1)" "$pad" "Show My Information" \
    "2)" "$pad" "List Online User" \
    "3)" "$pad" "Send Message" \
    "4)" "$pad" "Notifications" \
    "5)" "$pad" "Quit" \

    printf "\n\nType the selection you want to: " 
    read -r selection

    case "$selection" in
        1) clear; show_profile; read -n 1 -s -r -p "Press any key to go main page..."; clear;;
        2) clear; list_online_user; read -n 1 -s -r -p "Press any key to go main page..."; clear;;
        3) clear; start_chat;;
        4) clear; notifications;;
        5) clear; pkill -f "nc -l -k *"; rm -f broadcast_log.txt; rm -f online_user.txt; pkill -f "tail -f";  printf "\n\n  WE WILL WAIT AGAIN DEAR $USER_NAME :)(: \n\n"; kill; exit 0;;
        *) clear; printf "Please enter valid selection \n\n"; read -n 1 -s -r -p "Press any key to go main page..."; clear;;
    esac;
         
}

pkill -f "tail -f"
pkill -f "nc -l -k *"
rm -f broadcast_log.txt
rm -f online_user.txt
rm -f $NOTIFY_TXT
            
echo "Write Username: "
read USER_NAME
while [ ${#USER_NAME} -eq 0 ];do
    printf "Please write valid input."
    echo " Write Username: "
    read USER_NAME
    clear
done
MY_IP=$(
        LANG=C /sbin/ifconfig  |
            sed -ne $'/127.0.0.1/ ! {
                s/^[ \t]*inet[ \t]\\{1,99\\}\\(addr:\\)\\{0,1\\}\\([0-9.]*\\)[ \t\/].*$/\\2/p;
            }')
MY_NETWORK=$(echo "$MY_IP" | cut -d "." -f 1-3)
clear
show_profile
read -r -p "Wait 5 seconds or press any key to continue immediately..." -t 5 -n 1 -s
what_to_do &
broadcastNetwork &
sleep 1
read -n 1 -s -r &

while [ true ]; do
    selection
done
