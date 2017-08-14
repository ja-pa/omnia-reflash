#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 17:20:18 2017

@author: paja
"""
import urllib2
from terminaltables import AsciiTable
import argparse
import sys


class Packages:
    def __init__(self, branch="omnia-nightly"):
        self.__branch = branch
        self.__repo_url = 'http://repo.turris.cz/%s/packages/%s/Packages'
        self._pkg_list = []

    def search_by_name(self, name, case_sensitive=True):
        ret = []
        for item in self._pkg_list:
            if case_sensitive is True:
                pkg_name = item["Package"]
            else:
                pkg_name = item["Package"].lower()
                name = name.lower()
            if pkg_name.find(name) >= 0:
                ret.append(item)
        return ret

    def search_by_sha256(self, sha256):
        pass

    def get_pkg_list(self):
        feeds = ["base", "hardware", "lucics",
               "management", "openwisp", "packages",
               "php", "printing", "routing",
               "telephony", "turrispackages"]
        print "Branch", self.__branch, ":"
        print "Downloading feeds :",
        for feed in feeds:
            try:
                feed_list = self._download_list(feed)
                print feed + ", ",
                self._pkg_list = self._pkg_list + self._parse_packages(feed_list)
            except:
                print feed+"(not found),",
        print

    def _download_list(self, feed):
        response = urllib2.urlopen(self.__repo_url % (self.__branch, feed))
        return response.read()

    def _parse_signle_package(self, package):
        ret = []
        tmp = []
        for item in package.splitlines():
            if item.find(":") >= 0:
                tmp.append(map(str.strip, item.split(":", 1)))
        for item in tmp:
            if item != [""]:
                ret.append(item)
        return dict(ret)

    def _parse_packages(self, packages):
        ret = []
        for item in packages.split("\n\n"):
            single_package = self._parse_signle_package(item)
            if single_package != {}:
                ret.append(single_package)
        return ret


def parse_package_version():
    pass


def print_pkg(packages, header=["Package", "Version", "Filename"]):
    ret_tbl = []
    if len(packages) == 0:
        return [["No packages found"]]
    ret_tbl.append(header)
    for pkg in packages:
        tbl_line = []
        for val_name in header:
            tbl_line.append(pkg[val_name])
        ret_tbl.append(tbl_line)
    return ret_tbl


def main_cli(argv):
    header = ["Package", "Version", "Filename"]
    parser = argparse.ArgumentParser(description='Omnia')
    parser.add_argument('-fp', '--find-package', help='find package')
    parser.add_argument('-b', '--branch', action="store", default="omnia-nightly",
                        help='set omnia branch')
    parser.add_argument('-pd', '--print-description', action="store_const",
                        const="Description", help='Print description', default=None)
    parser.add_argument('-ps', '--print-section', action="store_const",
                        const="Section", help='Print section', default=None)
    parser.add_argument('-pss', '--print-source', action="store_const",
                        const="Source", help='Print print source', default=None)
    args = parser.parse_args(argv)
    if args.print_description:
        header.append(args.print_description)
    if args.print_section:
        header.append(args.print_section)
    if args.print_source:
        header.append(args.print_source)
    if args.find_package:
        abc = Packages(args.branch)
        abc.get_pkg_list()
        ccc = abc.search_by_name(args.find_package, False)
        table = AsciiTable(print_pkg(ccc, header))
        print "Find ", args.find_package, "in branch ", args.branch
        print
        print table.table

main_cli(sys.argv[1:])
