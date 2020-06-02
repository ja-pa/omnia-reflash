#!/bin/bash

if [ -d packages ]; then
	rm -rf packages
fi

update_openwrt_master() {
 	git clone https://github.com/ja-pa/openwrt
 	cd openwrt
 	git remote add upstream https://github.com/openwrt/openwrt.git
 	git fetch upstream
 	git pull upstream master
	git push
}

update_master() {
 	git clone https://github.com/ja-pa/packages
 	cd packages/
 	git remote add upstream https://github.com/openwrt/packages.git
 	git fetch upstream
 	git pull upstream master
	git push
}

update_branch() {
	branch="$1"

	git clone https://github.com/ja-pa/packages
	cd packages/
	git remote add upstream https://github.com/openwrt/packages.git
	git fetch upstream
	git checkout --track origin/$branch
	git pull upstream $branch
	git push
}

print_help() {

	echo Supported branch names
	echo master
	echo openwrt-18.06
	echo openwrt-19.07
	echo openwrt-master openwrt branch
}

cmd="$1"
case $cmd in
	master)
		echo "Update $cmd"
		update_master
	;;
	openwrt-master)
		echo "Update $cmd"
		update_openwrt_master
	;;
	openwrt-18.06|openwrt-19.07)
		echo "Update $cmd"
		update_branch $cmd
	;;
	*)
	       print_help
	;;
esac
