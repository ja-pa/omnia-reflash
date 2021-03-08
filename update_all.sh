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

update_openwrt_branch() {
	branch="$1"

	git clone https://github.com/ja-pa/openwrt
	cd openwrt/
	git remote add upstream https://github.com/openwrt/openwrt.git
	git fetch upstream
	git checkout --track origin/$branch
	git pull upstream $branch
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

update_master_luci() {
	git clone https://github.com/ja-pa/luci
	cd luci
	git remote add upstream https://github.com/openwrt/luci.git
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
	echo openwrt-21.02
	echo openwrt-master openwrt branch
	echo openwrt-main-19.07 openwrt branch
	echo luci-master
}

cmd="$1"
case $cmd in
	master)
		echo "Update $cmd"
		update_master
	;;
	openwrt-main-18.06|openwrt-main-19.07)
		echo "Update $cmd"
		update_openwrt_branch openwrt-19.07
	;;
	openwrt-master)
		echo "Update $cmd"
		update_openwrt_master
	;;
	openwrt-18.06|openwrt-19.07|openwrt-21.02)
		echo "Update $cmd"
		update_branch $cmd
	;;
	luci-master)
		echo "Update $cmd"
		update_master_luci
	;;
	*)
	       print_help
	;;
esac
