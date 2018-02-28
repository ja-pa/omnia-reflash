# Turris Omnia utilities

Requirements:
First, you need to have python. For me, it was better to install and use **python-pip**.

Open terminal and copy&paste this command:
``` sudo apt-get install python-pip ```

Almost every python script, which you can find here requires **python module terminaltables**, which you can install by the following command in terminal:

```pip install terminaltables```




## Find a Package
(tested on Ubuntu 17.10.)

You need to download **findpkg.py** from this repo to any folder on your disk, where you want and be in the same folder and in the terminal you can for example use this command:

``` python findpkg.py -fp name_of_package ```

<<<<<<< HEAD
### Usage

For finding any packages named **linux** in **omnia-nightly** you can use this command  ``` python findpkg.py -fp linux ```
and this will give you amazing output:

```
+-----------------------+------------------------------------------------+--------------------------------------------------------------------------+
| Package               | Version                                        | Filename                                                                 |
+-----------------------+------------------------------------------------+--------------------------------------------------------------------------+
| kmod-isdn4linux       | 4.4.118+0-1-afe98e9a77d54e7d4189fe065a4bb75b-0 | kmod-isdn4linux_4.4.118+0-1-afe98e9a77d54e7d4189fe065a4bb75b-0_mvebu.ipk |
| linux-atm             | 2.5.2-5                                        | linux-atm_2.5.2-5_mvebu.ipk                                              |
| gst1-mod-video4linux2 | 1.6.2-2                                        | gst1-mod-video4linux2_1.6.2-2_mvebu.ipk                                  |
| lcd4linux-custom      | r1203-4                                        | lcd4linux-custom_r1203-4_mvebu.ipk                                       |
| lcd4linux-full        | r1203-4                                        | lcd4linux-full_r1203-4_mvebu.ipk                                         |
| linuxptp              | 20151118-1                                     | linuxptp_20151118-1_mvebu.ipk                                            |
+-----------------------+------------------------------------------------+--------------------------------------------------------------------------+

```

If you want, you can search also packages in **OpenWRT**, which you can do with following command:

``` python findpkg.py -fp name_of_package -pl ```

=======
When I use for example this one: ``` python findpkg.py -fp vnstat ``` it will search package **vnstat** in omnia-nightly branch
and will give you this amazing output:

```

+------------------------+----------------------------+-----------------------------------------------------------+
| Package                | Version                    | Filename                                                  |
+------------------------+----------------------------+-----------------------------------------------------------+
| luci-app-vnstat        | git-17.212.24321-49c3edd-1 | luci-app-vnstat_git-17.212.24321-49c3edd-1_all.ipk        |
| luci-i18n-vnstat-ca    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-ca_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-cs    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-cs_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-de    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-de_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-el    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-el_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-en    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-en_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-es    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-es_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-fr    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-fr_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-he    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-he_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-hu    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-hu_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-it    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-it_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-ja    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-ja_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-ms    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-ms_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-no    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-no_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-pl    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-pl_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-pt-br | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-pt-br_git-17.212.24321-49c3edd-1_all.ipk |
| luci-i18n-vnstat-pt    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-pt_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-ro    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-ro_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-ru    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-ru_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-sk    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-sk_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-sv    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-sv_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-tr    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-tr_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-uk    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-uk_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-vi    | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-vi_git-17.212.24321-49c3edd-1_all.ipk    |
| luci-i18n-vnstat-zh-cn | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-zh-cn_git-17.212.24321-49c3edd-1_all.ipk |
| luci-i18n-vnstat-zh-tw | git-17.212.24321-49c3edd-1 | luci-i18n-vnstat-zh-tw_git-17.212.24321-49c3edd-1_all.ipk |
| vnstat                 | 1.12-2                     | vnstat_1.12-2_mvebu.ipk                                   |
| vnstati                | 1.12-2                     | vnstati_1.12-2_mvebu.ipk                                  |
+------------------------+----------------------------+-----------------------------------------------------------+

```
>>>>>>> origin/master

Other arguments which you can use, but be careful not every argument works.
```
  -fp FIND_PACKAGE [FIND_PACKAGE ...], --find-package FIND_PACKAGE [FIND_PACKAGE ...]
                        find package
  -fd FIND_DEPENDS, --find-depends FIND_DEPENDS
                        find depend packages
  -b BRANCH, --branch BRANCH
                        set omnia branch
  -pl, --project-lede   Search in lede project
  -pd, --print-description
                        Print description
  -ps, --print-section  Print section
  -pss, --print-source  Print print source
  -ppd, --print-package-depends
                        Print depends source
  -pu, --print-url      Print gitlab url
```


## Debian Security announcements

This will find any security issues from https://lists.debian.org/debian-security-announce

You need to download **debiansec.py** from this repo to any folder on your disk, where you want and be in the same folder and in the terminal you can look any package like **php7.0** has some security issues with this command:

```python debiansec.py -fp php7.0```

and it will give you this output:
```
Downloading list for 2018
Downloading list for 2017  
Downloading list for 2016  
Downloading list for 2015  
+---------+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| package | versions        | cve                                                                                                                                                                                                 |
+---------+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| php7.0  | 7.0.27-0+deb9u1 | CVE-2017-1114,CVE-2017-1114,CVE-2017-1162,CVE-2017-1293,CVE-2017-1293,CVE-2017-1293,CVE-2017-1664,CVE-2017-1114,CVE-2017-1114,CVE-2017-1162,CVE-2017-1293,CVE-2017-1293,CVE-2017-1293,CVE-2017-1664 |
+---------+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
<<<<<<< HEAD
```
=======
```
>>>>>>> origin/master
