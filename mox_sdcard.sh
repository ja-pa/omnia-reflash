#!/bin/bash

KITTENS=https://repo.turris.cz/hbk/medkit/mox-medkit-latest.tar.gz
DRAGONS=https://repo.turris.cz/hbd/medkit/mox-medkit-latest.tar.gz
DRAGONS_FAST=https://repo.turris.cz/hbd-fast/medkit/mox-medkit-latest.tar.gz

TARGET_DRIVE=/dev/sdb
TARGET_PART=/dev/sdb1
MEDKIT=
MEDKIT_FILE=mox-medkit-latest.tar.gz
MNT_DIR="/mnt/tmp"

create_sdcard() {

[ ! -d $MNT_DIR ] && mkdir -p $MNT_DIR

dd if=/dev/zero of="$TARGET_DRIVE" bs=1024 count=10240

(
echo n # Add a new partition
echo p # Primary partition
echo 1 # Partition number
echo   # First sector (Accept default: 1)
echo   # Last sector (Accept default: varies)
echo p #
echo w # Write changes
)| fdisk $TARGET_DRIVE

echo "Creating btrfs and subvolume"
echo "============================"

mkfs.btrfs -f "$TARGET_PART"
mount $TARGET_PART $MNT_DIR
btrfs subvolume create $MNT_DIR/@
sync
umount $MNT_DIR


echo "Creating btrfs and subvolume"
echo "============================"

mount $TARGET_PART -o subvol=@ $MNT_DIR

if [ -f "$MEDKIT" ]; then
	echo "do medkit"
else
	echo "Error! No medkit found!!!!"
fi

echo "extract medkit"
tar -C $MNT_DIR -xzf $MEDKIT
sync
umount $MNT_DIR


echo "Create factory"
echo "============================"
mount $TARGET_PART $MNT_DIR
cd $MNT_DIR
ln -s @/boot/boot-btrfs.scr boot.scr
btrfs subvolume snapshot $MNT_DIR/@ $MNT_DIR/@factory
sync
sleep 10
umount $MNT_DIR
}

print_help() {
	echo "Commands"
	echo "========"
	echo "kittens		Download kitten medkit"
	echo "dragons		Download dragon medkit"
	echo "dragons_fast	Download dragon fast medkit"
	echo "flash 		flash medkit to sdcard"
}

case $1 in
	dragons)
		echo "Downloading dragons"
		[ -f "$MEDKIT_FILE" ] && rm $MEDKIT_FILE
		wget $DRAGONS
		;;
	dragons_fast)
		echo "Downloading Dragons fast"
		[ -f "$MEDKIT_FILE" ] && rm $MEDKIT_FILE
		wget $DRAGONS_FAST
		;;
	kittens)
		echo "Downloading Kittens"
		[ -f "$MEDKIT_FILE" ] && rm $MEDKIT_FILE
		wget $KITTENS
		;;
	flash)
		echo "Flash medkit to sdcard"
		if [ "$EUID" -ne 0 ]; then
			echo "Please run as root"
			exit
		fi
		if [ ! -e "$TARGET_DRIVE" ]; then
			echo "Please insert sdcard"
			exit
		fi
		if [ -f "$MEDKIT_FILE" ]; then
			MEDKIT=$(realpath $MEDKIT_FILE)
			umount $MNT_DIR
			umount $TARGET_PART
			create_sdcard
		else
			echo "Medkit file wasn't found!"
		fi
		;;
	*)
		print_help
esac
