#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:41:29 2019

@author: cznic
"""
from urllib.request import urlopen
from terminaltables import AsciiTable
import os
import sys
import argparse


class FailLogs:
    def __init__(self):
        self._faillog_url = "https://downloads.openwrt.org/snapshots/faillogs/%s/packages/%s/compile.txt"
        self._arch_list=[
        "aarch64_armv8-a","aarch64_cortex-a53","aarch64_cortex-a53_neon-vfpv4",
        "aarch64_cortex-a72","aarch64_generic","arc_arc700",
        "arc_archs","arm_arm1176jzf-s_vfp","arm_arm926ej-s",
        "arm_cortex-a15_neon-vfpv4", "arm_cortex-a5",
        "arm_cortex-a53_neon-vfpv4","arm_cortex-a5_neon-vfpv4",
        "arm_cortex-a5_vfpv4","arm_cortex-a7","arm_cortex-a7_neon-vfpv4",
        "arm_cortex-a8_neon","arm_cortex-a8_vfpv3","arm_cortex-a9",
        "arm_cortex-a9_neon","arm_cortex-a9_vfpv3",
        "arm_fa526","arm_mpcore","arm_mpcore_vfp",
        "arm_xscale","armeb_xscale","i386_geode",
        "i386_i486","i386_pentium","i386_pentium4","mips64_mips64",
        "mips64_octeon","mips64_octeonplus","mips64el_mips64",
        "mips_24kc","mips_mips32","mipsel_24kc","mipsel_24kc_24kf",
        "mipsel_74kc","mipsel_mips32","mipsel_mips32r2","powerpc_440",
        "powerpc_464fp","powerpc_8540","x86_64"]

    def get_pkg_build_error(self, arch, package):
        try:
            url_full=self._faillog_url % (arch,package)
            response = urlopen(url_full)        
            ttt=response.read().decode('utf-8')
            return ttt
        except:
            return None
        
    def get_log_scan(self, package):
        failed_list=[]
        passed_list=[]
        for item in self._arch_list:
            ret=self.get_pkg_build_error(item,package)
            if ret != None:
                failed_list.append([item,ret])
            else:
                passed_list.append([item,None])
        return {"failed":failed_list,"passed":passed_list}
    
    def save_logs(self, package, path, arch, log):
        file_name = "%s_failog.txt" % arch
        full_path=os.path.join(path, package)
        if not os.path.isdir(full_path):
            os.makedirs(full_path, exist_ok=True)
        with open(os.path.join(full_path, file_name)) as fp:
            fp.write(log)


def print_stats(log_scan):
    failed_count = len(log_scan["failed"])
    passed_count = len(log_scan["passed"])
    failed_per = failed_count/((failed_count+passed_count)*0.01)
    passed_per = passed_count/((failed_count+passed_count)*0.01)
    tbl=[["Failed","Passed"],
         [failed_count,passed_count],
         ["%i %%" % failed_per,"%i %%" % passed_per]]
    table = AsciiTable(tbl)
    print(table.table)
    
def print_fail_stat(log_scan, only_fails=False):
    tbl_f = [["Failed"]]
    tbl_p = [["Passed"]]
    for item in log_scan["failed"]:
        tbl_f.append([item[0]])
    for item in log_scan["passed"]:
        tbl_p.append([item[0]])
    table = AsciiTable(tbl_f)
    table2 = AsciiTable(tbl_p)
    print(table.table)
    if only_fails == False:
        print(table2.table)

def main_cli():
    pass


parser = argparse.ArgumentParser(description='Failed log')
parser.add_argument('-fp', '--find-package',
                        help='find package')
parser.add_argument('-pl', '--package-list', nargs='+',
                        help='set file with packages list')
parser.add_argument('-c', '--configuration', nargs='+',
                        help='set configuration file')

parser.add_argument('-f', '--print-fails', action="store_true",
                        help='Print only failures')
parser.add_argument('-p', '--print-passes', action="store_true",
                        help='Print only failures')
parser.add_argument('-s', '--print-statistics', action="store_true",
                        help='Print only failures')

args = parser.parse_args(sys.argv[1:])
if args.find_package:
    fl=FailLogs()
    print(args.find_package)
    log_scan=fl.get_log_scan(args.find_package)
    print_fail_stat(log_scan, args.print_fails)
    if args.print_statistics:
        print_stats(log_scan)
    
    
    