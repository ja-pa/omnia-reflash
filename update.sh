#!/bin/bash

update_repo() {

	opkg update
	opkg install cznic-repo-keys-test

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
