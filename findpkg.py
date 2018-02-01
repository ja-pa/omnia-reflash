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
        self.__repo_url_turris = 'http://repo.turris.cz/%s/packages/%s/Packages'
        self.__repo_url_lede = 'https://downloads.lede-project.org/snapshots/packages/x86_64/%s/Packages'
        self._pkg_list = []
        self.__feeds_turris = ["base", "hardware", "lucics", "management",
                               "openwisp", "packages", "php", "printing",
                               "routing", "telephony", "turrispackages"]
        self.__feeds_lede = ["base", "luci", "packages",
                             "routing", "telephony"]

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

    def search_by_depends(self, name, case_sensitive=False, full_depends=False):
        ret = []
        for item in self._pkg_list:
            if "Depends" in item:
                if case_sensitive is True:
                    pkg_name = item["Depends"]
                else:
                    pkg_name = item["Depends"].lower()
                    name = name.lower()
                if pkg_name.find(name) >= 0:
                    ret.append(item)
        return ret

    def search_by_sha256(self, sha256):
        pass

    def get_pkg_list(self, project):
        if project == "turris":
            feeds = self.__feeds_turris
            print "Branch", self.__branch, ":"
        else:
            feeds = self.__feeds_lede
            print "Lede repo (latest snapshot:"
        print "Downloading feeds :",
        for feed in feeds:
            try:
                feed_list = self._download_list(feed, project)
                print feed + ", ",
                self._pkg_list = self._pkg_list + self._parse_packages(feed_list)
            except:
                print feed+"(not found),",
        print

    def _get_gitlab_url(self, pkg_source, branch="test"):
        ret = ""
        if pkg_source.startswith("feeds"):
            if pkg_source.startswith("feeds/turrispackages"):
                ret = pkg_source.replace("feeds/turrispackages/",
                                         "https://gitlab.labs.nic.cz/turris/turris-os-packages/tree/%s/" % branch)
            elif pkg_source.startswith("feeds/lucics"):
                ret = pkg_source.replace("feeds/lucics/",
                                         "https://gitlab.labs.nic.cz/turris/luci-cs/tree/master/")
            return ret
        elif pkg_source.startswith("package"):
            ret = pkg_source.replace("package/",
                                     "https://gitlab.labs.nic.cz/turris/openwrt/tree/%s/" % branch)
            return ret
        else:
            return ""

    def _download_list(self, feed, project="turris"):
        """ Download package feed list for project (lede,turris ) """
        if project == "turris":
            url_full = self.__repo_url_turris % (self.__branch, feed)
        else:
            url_full = self.__repo_url_lede % feed
        response = urllib2.urlopen(url_full)
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
        tmp_dict = dict(ret)
        if "Source" in tmp_dict:
            ret.append(["GitlabURL", self._get_gitlab_url(tmp_dict["Source"])])
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
    global abc
    header = ["Package", "Version", "Filename"]
    parser = argparse.ArgumentParser(description='Omnia')
    parser.add_argument('-fp', '--find-package', nargs='+',
                        help='find package')
    parser.add_argument('-fd', '--find-depends', help='find depend packages')
    parser.add_argument('-b', '--branch', action="store",
                        default="omnia-nightly", help='set omnia branch')
    parser.add_argument('-pl', '--project-lede', action="store_true",
                        help='Search in lede project')
    parser.add_argument('-pd', '--print-description', action="store_const",
                        const="Description", help='Print description',
                        default=None)
    parser.add_argument('-ps', '--print-section', action="store_const",
                        const="Section", help='Print section', default=None)
    parser.add_argument('-pss', '--print-source', action="store_const",
                        const="Source", help='Print print source',
                        default=None)
    parser.add_argument('-ppd', '--print-package-depends', action="store_const",
                        const="Depends", help='Print depends source',
                        default=None)
    parser.add_argument('-pu', '--print-url', action="store_const",
                        const="GitlabURL", help='Print gitlab url',
                        default=None)

    args = parser.parse_args(argv)
    if args.print_description:
        header.append(args.print_description)
    if args.print_section:
        header.append(args.print_section)
    if args.print_source:
        header.append(args.print_source)
    if args.print_package_depends:
        header.append(args.print_package_depends)
    if args.print_url:
        header.append(args.print_url)
    if args.find_package:
        abc = Packages(args.branch)
        if args.project_lede:
            abc.get_pkg_list("lede")
        else:
            abc.get_pkg_list("turris")
        ccc = []
        for pkg_name in args.find_package:
            ccc += abc.search_by_name(pkg_name, False)
        table = AsciiTable(print_pkg(ccc, header))
        print "Find ", args.find_package, "in branch ", args.branch
        print
        print table.table
    if args.find_depends:
        abc = Packages(args.branch)
        abc.get_pkg_list()
        ccc = abc.search_by_depends(args.find_depends, False)
        table = AsciiTable(print_pkg(ccc, header))
        print "Find ", args.find_depends, "in branch ", args.branch
        print
        print table.table

main_cli(sys.argv[1:])
