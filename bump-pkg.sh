#!/bin/bash


bump_python_pkg() {
	local version="$2"
	local pkg_name="$1"
	local pkg_make_file="feeds/packages/lang/python/$1/Makefile"
	sed -i "s/PKG_HASH:=.*/PKG_HASH:=skip/" $pkg_make_file
	sed -i "s/PKG_VERSION:=.*/PKG_VERSION:=$version/" $pkg_make_file

	make package/$pkg_name/download V=s
	make package/$pkg_name/check FIXUP=1 V=s
	echo
	echo "make package/$pkg_name/{clean,compile} V=s"
	echo "make package/$pkg_name/{clean,configure} PY3=stdlib V=s"
	echo
}

python_commit() {
	local version="$2"
	local pkg_name="$1"
	local pkg_dir="$pkg_name-$version"

	mkdir -p "$pkg_name-$version"

}

print_help() {
	echo "Help"
	echo "example use"
	echo ./bump-pkg.sh python-typing-extensions 3.10.0.0 python-bump
	echo
}

echo "bump"
PKG_NAME="$1"
PKG_VERSION="$2"
action="$3"

case "$action" in
	python-bump)
		echo python package bump
		[ -z "$PKG_NAME" ] && echo "Package given!" && exit
		if [ -d "feeds/packages/lang/python/$PKG_NAME" ]; then
			[ -z "$PKG_VERSION" ] && echo "No pkg version" && exit
			echo "Bumping package"
			bump_python_pkg "$PKG_NAME" "$PKG_VERSION" #send version and
		else
			echo "No makefile found"
			echo "feeds/packages/lang/python/$PKG_NAME"
		fi
		;;
	--help| *)
		print_help
		;;
esac

