#!/bin/sh

set -e
URI_BASE="https://api.turris.cz/openwrt-repo/omnia"

download_files() {
        echo "Download $URI_BASE/nor_fw/omnia-initramfs-zimage"
        curl --insecure "$URI_BASE/nor_fw/omnia-initramfs-zimage" > mtd

        echo "Download $URI_BASE/nor_fw/uboot-turris-omnia-spl.kwb"
        curl --insecure "$URI_BASE/nor_fw/uboot-turris-omnia-spl.kwb" > uboot
	
	if [ "$1" = "nightly" ]; then
		echo "Download $URI_BASE/medkit/omnia-medkit-latest.tar.gz"
		curl --insecure "$URI_BASE/medkit/omnia-medkit-latest.tar.gz" > medkit.tar.gz
	else
		echo "Download $URI_BASE/medkit/omnia-medkit-latest-minimal.tar.gz"
		curl --insecure "$URI_BASE/medkit/omnia-medkit-latest-minimal.tar.gz" > medkit.tar.gz
	fi

	if grep -q "<title>404 Not Found</title>" mtd; then
		echo "Error mtd not found"
		rm mtd uboot medkit.tar.gz
		exit 1
	fi
	if grep -q "<title>404 Not Found</title>" uboot; then
		echo "Error uboot not found"
		rm mtd uboot medkit.tar.gz
		exit 1
	fi
	if grep -q "<title>404 Not Found</title>" medkit.tar.gz; then
		echo "Error medkit.tar.gz not found"
		rm mtd uboot medkit.tar.gz
		exit 1
	fi
}

reflash() {
	mtd write mtd /dev/mtd1
	mtd write uboot /dev/mtd0
	mkdir -p btrfs
	mount /dev/mmcblk0p1 btrfs
	btrfs subvolume delete btrfs/@factory
	btrfs subvolume create btrfs/@factory
	cd btrfs/@factory
	gunzip -c /tmp/medkit.tar.gz | tar xp
	cd /tmp
	btrfs subvolume delete btrfs/certbackup
	umount btrfs
	schnapps rollback factory
}

print_warning()
{
	echo "You're running this script on your own responsibility."
	echo "It might be unsafe. If you lose power during the run, it will brick the device."
	echo "Going to flash from $URI_BASE. Prest Enter to continue, CTRL+C to abort."
	read
}

if [ "$2" ]; then
	URI_BASE="$URI_BASE-$2"
fi

cmd="$1"
case $cmd in
	download)
		download_files "$2"
	;;
	only-flash)
		print_warning
		cd /tmp
		reflash
		echo "Flash done!"
		reboot
	;;
	flash)
		print_warning
		cd /tmp
		download_files "$2"
		reflash
		echo "Flash done!"
    reboot
	;;
	help|*)
	  echo "Help:"
  	echo "	only-flash			- flash medkit without donwload"
  	echo "	flash <dev-name>		- downloadflash medkit from given branch"
  	echo "	download <dev-name>		- download medkit"
  	echo "	help				- shows help"
	;;
esac
