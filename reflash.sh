#!/bin/sh

set -e
URI_BASE="https://api.turris.cz/openwrt-repo/omnia"

download_files() {
	wget --no-check-certificate "$URI_BASE/nor_fw/omnia-initramfs-zimage" -O mtd
	wget --no-check-certificate "$URI_BASE/nor_fw/uboot-turris-omnia-spl.kwb" -O uboot
	wget --no-check-certificate "$URI_BASE/omnia-medkit-latest.tar.gz" -O medkit.tar.gz
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
		download_files
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
		download_files
		reflash
		echo "Flash done!"
    reboot
	;;
	help|*)
	  echo "Help:"
  	echo "	only-flash				- flash medkit without donwload"
  	echo "	flash <dev-name>		- downloadflash medkit from given branch"
  	echo "	download <dev-name>		- download medkit"
  	echo "	help					- shows help"
	;;
esac
