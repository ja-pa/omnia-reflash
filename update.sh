#!/bin/bash

update_repo() {

        package_name=$(curl http://repo.turris.cz/omnia-nightly/packages/turrispackages/|grep "cznic-repo-keys-test"|awk -F'href="' '{print $2}'|awk -F'"' '{print $1}')
        wget http://repo.turris.cz/omnia-nightly/packages/turrispackages/$package_name
        opkg install $package_name
        #opkg install cznic-repo-keys-test
        opkg update

        uci set updater.override=override
        uci set updater.override.branch=$1
        uci commit
        updater.sh
}

case "$1" in
"update")
        if [ ! -z "$2" ]; then
                echo "update repo"
                update_repo $2
        else
                echo "Error you have to set repo"
        fi
;;
* | "--help")
        echo "Help:"
        echo "[command] [option]"
        echo "Example:"
        echo "update rc|stable|master|nightly"
;;

esac

