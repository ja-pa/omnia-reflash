#!/bin/sh

#set -e
URI_BASE="https://repo.turris.cz/omnia"
URI_HBD="https://repo.turris.cz/hbd/medkit/omnia-medkit-latest.tar.gz"
URI_HBK="https://repo.turris.cz/hbk/medkit/omnia-medkit-latest.tar.gz"
URI_HBS="https://repo.turris.cz/archive/4.0-alpha2/medkit/omnia-medkit-latest.tar.gz"

download_to4_files() {
	tmp_url=""
	if [ "$1" == "hbd" ]; then
		tmp_url=$URI_HBD
	elif [ "$1" == "hbk" ]; then
		tmp_url=$URI_HBK
	elif [ "$1" == "hbs" ]; then
		tmp_url=$URI_HBS
	else

		echo "Error! Unknown version $1"
		exit
	fi
        echo "Download (Medkit $1 Image) $tmp_url"
        curl --insecure "$tmp_url" > omnia-medkit-latest.tar.gz
}

download_files() {
	uri_rescue=$URI_BASE/nor_fw/omnia-initramfs-zimage
	uri_uboot=$URI_BASE/nor_fw/uboot-turris-omnia-spl.kwb
	uri_medkit=$URI_BASE/medkit/omnia-medkit-latest.tar.gz
	uri_medkit_failback=$URI_BASE/openwrt-mvebu-Turris-Omnia-rootfs.tar.gz

        echo "Download (Rescue Image) $uri_rescue"
        curl --insecure "$uri_rescue" > mtd

        echo "Download (Uboot) $uri_uboot"
        curl --insecure "$uri_uboot" > uboot


	echo "Download (Medkit) $uri_medkit"
	curl --insecure "$uri_medkit" > medkit.tar.gz

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
		rm medkit.tar.gz
		echo "Download (Medkit failback) $uri_medkit_failback"
		curl --insecure "$uri_medkit_failback" > medkit.tar.gz

		if grep -q "<title>404 Not Found</title>" medkit.tar.gz; then
			echo "Error medkit.tar.gz not found"
			rm mtd uboot medkit.tar.gz
			exit 1
		fi
	fi
}

reflash_to4_medkit() {
	cd /tmp
	if [ -f "omnia-medkit-latest.tar.gz" ]; then
		snapshot_num=$(schnapps list|tail -n1|awk -F"|" '{print $1}'|xargs)
		schnapps mount $snapshot_num
		rm -rf /mnt/snapshot-@$snapshot_num/*
		#tar xf omnia-medkit-latest.tar.gz -C /mnt/snapshot-@$snapshot_num/
		cd /mnt/snapshot-@$snapshot_num/

		gunzip -c /tmp/omnia-medkit-latest.tar.gz | tar xp

		schnapps rollback $snapshot_num
		schnapps modify $snapshot_num -d TO4
		echo "You can restart router to change system to TO4 !"
	else
		echo "No omnia-medkit-latest.tar.gz file found !!"
	fi
}

reflash_mtd() {
	echo "Flashing mtd..."
	#mtd write mtd /dev/mtd1
}

reflash_uboot() {
	echo "Flashing uboot..."
	#mtd write uboot /dev/mtd0
}

reflash_medkit() {
	echo "Flashing medkit..."
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

reflash_to3x_medkit() {
	echo "Flashing medkit..."
	medkit_name=medkit.tar.gz
	cd /tmp
	if [ -f "$medkit_name" ]; then
		snapshot_num=$(schnapps list|tail -n1|awk -F"|" '{print $1}'|xargs)
		if [ "$(echo $snapshot_num|wc -c)" -gt 50 ]; then
			echo "Creating first snapshot"
			schnapps create
			snapshot_num=1
		fi

		schnapps mount $snapshot_num
		rm -rf /mnt/snapshot-@$snapshot_num/*
		#tar xf omnia-medkit-latest.tar.gz -C /mnt/snapshot-@$snapshot_num/
		cd /mnt/snapshot-@$snapshot_num/

		gunzip -c /tmp/$medkit_name | tar xp

		schnapps rollback $snapshot_num
		schnapps modify $snapshot_num -d "TO3 new"
		echo "You can restart router to change system to TO4 !"
	else
		echo "No $medkit_name file found !!"
	fi
}


reflash() {
	which mtd
	if [ "$?" -eq 1 ]; then
		echo "mtd not found!"
	else
		echo "Flashing mtd..."
		reflash_mtd
		echo "Flashing uboot..."
		reflash_uboot
	fi
	echo "Flashing medkit..."
	reflash_medkit
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
	only-flash-scp)
		IP=192.168.1.1
		echo "Copy medkit files to router IP $IP "
		scp {medkit.tar.gz,mtd,reflash.sh,uboot} root@$IP:/tmp
		echo "Run flash command via ssh"
		ssh root@$IP 'cd /tmp && chmod +x reflash.sh && ./reflash.sh only-flash'
	;;
	flash)
		print_warning
		cd /tmp
		download_files "$2"
		reflash
		echo "Flash done!"
		reboot
	;;
	flash-to3)
		print_warning
		cd /tmp
		download_files "$2"
		reflash_to3x_medkit
		echo "Flash done!"
		reboot
	;;

	flash-to4)
		if [ ! -z "$2" ]; then
			cd /tmp
			download_to4_files $2
			reflash_to4_medkit
			reboot
		else
			echo "Error! You have to set HBD/HDK/HBS version of medkit"
		fi
	;;
	help|*)
		echo "Help:"
		echo "	only-flash			- flash medkit without donwload"
		echo "	only-flash-scp			- flash medkit without donwload via scp "
		echo "	flash <dev-name>		- downloadflash medkit from given branch"
		echo "	flash-to4 <hbd/hbk>		- downloadflash medkit from omnia TurrisOS 4"
		echo "  flash-to3 <dev-name>		- download and flash medkit via schnapps"
		echo "	download <dev-name>		- download medkit"
		echo "	help				- shows help"
	;;
esac
