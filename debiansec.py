#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 21:19:54 2017

@author: cz_nic
"""

import urllib2
import re
from terminaltables import AsciiTable
import pickle
import os
import calendar
import time
import argparse
import sys


class DebianSecAnn:
    def __init__(self):
        self.__url_announce_tpl = "https://lists.debian.org/debian-security-announce/%i/threads.html"
        self.__url_page_tpl = "https://lists.debian.org/debian-security-announce/%i/%s"
        self.__ann_tbl = []
        self.__cache_filename = ".dsa_cache"
        self._load_cache()
        self._download_all(2017)
        self._download_all(2016)
        self._download_all(2015)
        self._save_cache()

    def _save_cache(self):
        with open(self.__cache_filename, "wb") as f:
            pickle.dump(self.__ann_tbl, f)

    def _load_cache(self):
        if os.path.isfile(self.__cache_filename):
            with open(self.__cache_filename, "rb") as f:
                self.__ann_tbl = pickle.load(f)

    def _contains_url(self, url):
        for item in self.__ann_tbl:
            if item['url'] == url:
                return True
        return False

    def _check_cache(self, timediff=3600):
        if os.path.isfile(self.__cache_filename):
            f = os.path.getmtime(self.__cache_filename)
            tmp_diff = calendar.timegm(time.gmtime()) - f
            print tmp_diff
            if tmp_diff < timediff:
                return True
        return False

    def _get_list(self, text):
        mm = re.findall('<li><strong><a name="(.*)" href="(.*)">', text)
        nn = [i[1] for i in mm]
        return nn

    def get_raw_data(self):
        return self.__ann_tbl

    def _extract_pre(self, text):
        return text.split("<pre>")[1].split("</pre>")[0]

    def _download_all(self, year=2017):
        web_list = urllib2.urlopen(self.__url_announce_tpl % year).read()
        msg_list = self._get_list(web_list)
        print
        print "Downloading list for %i" % year, " ",
        for msg in msg_list:
            url = self.__url_page_tpl % (year, msg)
            if self._contains_url(url) is False:
                msg_page = urllib2.urlopen(url).read()
                msg_page_clean = self._extract_pre(msg_page)
                print ".",
                sys.stdout.flush()
                self.__ann_tbl.append({"url": url,
                                      "full_text": msg_page_clean,
                                      "versions": self._get_version(msg_page_clean),
                                      "cve": self._get_cve(msg_page_clean),
                                      "package": self._get_package_name(msg_page_clean)})

    def _get_cve(self, text):
        try:
            cve_list = re.findall(r'CVE-(\d{4}-\d{4})', text)
            return ["CVE-" + i for i in cve_list]
        except:
            return []

    def _get_package_name(self, text):
        try:
            package = re.compile(r'Package(.*):(.*)')
            return package.search(text).group(2).strip()
        except:
            return ""

    def _get_version(self, text):
        ret = []
        match_texts = ['(.*)these problems have been fixed' "\n" 'in version(.*).',
                     '(.*)these problems have been fixed in' "\n" 'version(.*).',
                     '(.*)this problem has been fixed in' "\n" 'version(.*).',
                     '(.*)this problem has been fixed' "\n" 'in version(.*).']
        for i in match_texts:
            try:
                version = re.compile(i)
                ret.append(version.search(text).group(2))
            except:
                pass
        return [i.strip() for i in ret]

    def _search_by_name(self, tbl, name):
        # find_version=False):
        ret = []
        for pkg in tbl:
            if pkg["package"].find(name) >= 0:
                ret.append(pkg)
        return ret

    def _search_by_version(self, tbl, version):
        ret = []
        for pkg in tbl:
            print pkg['versions']
            for pkg_version in pkg["versions"]:
                print pkg_version
                if pkg_version.find(version) >= 0:
                    ret.append(pkg)
                    break
        return ret

    def search_pkg(self, name, version=None):
        ret = self._search_by_name(self.__ann_tbl, name)
        # if version:
        #    ret = self._search_by_version(self.__ann_tbl, version)
        return ret


def print_tbl(pkg_data, header=["package", "versions", "cve"]):
    ret_tbl = []
    ret_tbl.append(header)
    for pkg in pkg_data:
        tbl_line = []
        for name_header in header:
            tmp = pkg[name_header]
            if isinstance(tmp, list):
                tbl_line.append(",".join(tmp))
            else:
                tbl_line.append(tmp)
        ret_tbl.append(tbl_line)
    table = AsciiTable(ret_tbl)
    print
    print table.table


def main_cli(argv):
    header = ["package", "versions", "cve"]
    parser = argparse.ArgumentParser(description='Search')
    parser.add_argument('-fp', '--find-package', help='find package')
    args = parser.parse_args(argv)
    if args.find_package:
        aaa = DebianSecAnn()
        kkk = aaa.search_pkg(args.find_package, header)
        print_tbl(kkk)

main_cli(sys.argv[1:])
