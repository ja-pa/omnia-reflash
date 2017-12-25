#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script handles security issues dates.
"""

import gitlab
import sys
import argparse
from terminaltables import AsciiTable
import re
import os
import ConfigParser


class SecIssue:
    def __init__(self):
        self.issue_list = ["PUBLICLY_KNOWN",
                        "TURRIS_NOTICED",
                        "FIX_DEPLOYED",
                        "FIX_DEPLOYED_TURRISOS"]
        self.issue_dict = {key: "" for key in self.issue_list}

    def _parse_val(self, text, varname):
        try:
            val = re.compile(varname + '=(.*)')
            return val.search(text).group(1).strip()
        except:
            return ""

    def update_issue_text(self, text, issue_dict):
        tmp_text = []
        for var in self.issue_list:
            val = issue_dict.get(var, "")
            tmp_text.append("%s=%s" % (var, val))
        text += """\n```\n%s\n```""" % "\n".join(tmp_text)
        return text

    def get_issue_info(self, text):
        """ returns issue and dict with variables """
        text_out = []
        tmp_issue_dict = self.issue_dict.copy()
        add = True
        for line in text.splitlines():
            add = True
            for var in self.issue_list:
                # update issue dict
                if line.find(var+"=") >= 0:
                    val = self._parse_val(line, var)
                    tmp_issue_dict.update({var: val})
                    add = False
            if add and line.find("```") < 0:
                text_out.append(line)
        return '\n'.join(text_out), tmp_issue_dict


class Timestamp:
    def __init__(self):
        pass

    def get_time(self, timestamp):
        return timestamp.split("T")[1]

    def get_date(self, timestamp):
        return timestamp.split("T")[0]

    def get_empty(self):
        return "0000-00-00T00:00:00"

    def get_diff_days(self, ts1, ts2):
        pass

    def get_today(self):
        pass

    def check_date(self, str_date):
        # it's not perfect check...
        return bool(re.match('[1-3][0-9]{3}-[0-1][1-9]-[0-3][0-9]', str_date))

    def check_time(self, str_date):
        # it's not perfect check...
        return bool(re.match('[0-2][0-9]:[0-6][0-9]:[0-9]{2}', str_date))

    def check_timestamp(self, str_timestamp):
        if str_timestamp.find("T") >= 0:
            str_date = self.get_date(str_timestamp)
            str_time = self.get_time(str_timestamp)
            return self.check_date(str_date) and self.check_time(str_time)
        else:
            return self.check_date(str_timestamp)


class GitlabSec:
    def __init__(self, token, url='https://gitlab.labs.nic.cz'):
        # private token authentication
        self.__gl = gitlab.Gitlab(url, token)
        self.__gl.auth()

    def get_issues(self, repo_name, issue_state=None):
        """
        repo_name = turris/openwrt
        """
        project = self.__gl.projects.get(repo_name)
        ret = []
        for issue in project.issues.list(all=True):
            if issue_state == issue.state or issue_state is None:
                ret.append(issue)
        return ret

    def get_issue_description(self, issue_id, project_name):
        project = self.__gl.projects.get(project_name)
        issue = project.issues.get(issue_id)
        return issue.description

    def update_issue_info(self, issue_id, description, project_name):
        project = self.__gl.projects.get(project_name)
        issue = project.issues.get(issue_id)
        issue.description = description
        issue.save()


##################################################


def load_config(config_path):
    tmp_config_path = os.path.expanduser(config_path)
    if os.path.isfile(tmp_config_path):
        config = ConfigParser.ConfigParser()
        config.read(tmp_config_path)
        try:
            return {"token": config.get("gitlab", "token"),
                    "project_path": config.get("gitlab", "project_path")
                    }
        except:
            return None


def get_list_issues(GS, SI, project_path, header=["ID", "Title"] + SecIssue().issue_list):
    issues = GS.get_issues(project_path)
    ret_issues = [header]
    for i in issues:
        if ("security" in i.labels or "Security" in i.labels) and i.state == "opened":
            appa, issuedic = SI.get_issue_info(i.description)
            items = [i.id, i.title]
            for y in SI.issue_list:
                daaa = Timestamp().get_date(issuedic[y])
                items.append(daaa)
            ret_issues.append(items)
    return ret_issues


def update_sec_issue(GS, SI,
                     project_path, issue_id,
                     publicly_known=None, turris_noticed=None,
                     fix_deployed=None, fix_deployed_turrisos=None):
    """ This method updates only date info in given issue """
    description = GS.get_issue_description(issue_id)
    issue_text, issue_vars = SI.get_issue_info(description)
    if publicly_known:
        issue_vars["PUBLICLY_KNOWN"] = publicly_known
    if turris_noticed:
        issue_vars["TURRIS_NOTICED"] = turris_noticed
    if fix_deployed:
        issue_vars["FIX_DEPLOYED"] = fix_deployed
    if fix_deployed_turrisos:
        issue_vars["FIX_DEPLOYED_TURRISOS"] = fix_deployed_turrisos
    new_description = SI.update_issue_text(issue_text, issue_vars)
    GS.update_issue_info(issue_id, new_description, project_path)


def init_sec_issue(GS, SI, project_path, issue_id):
    description = GS.get_issue_description(issue_id)
    issue_text, issue_vars = SI.get_issue_info(description)

    for key, val in issue_vars.items():
        issue_vars.update({key: Timestamp().get_empty()})
    new_description = SI.update_issue_text(issue_text, issue_vars)
    GS.update_issue_info(issue_id, new_description)


def check_date(str_date):
    ts = Timestamp()
    if ts.check_timestamp(str_date):
        return True
    else:
        print "Error wrong date format. Use format YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD"
        return False


def main_cli(argv):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-l', '--list-issues', help='List security issues.', action='store_true')
    parser.add_argument('-pu', '--prit-url', help='Show url to issue', action='store_true')
    parser.add_argument('--init', type=int, help='Init issue dates with zeros')
    parser.add_argument('-o', '--opened', help="Show only opened issues", action='store_true', default=False)
    parser.add_argument('-u', '--update', type=int, help="Update issue number")
    parser.add_argument('-PK', '--PUBLICLY_KNOWN', help="Date of bug disclosure.")
    parser.add_argument('-TN', '--TURRIS_NOTICED', help="Date when Turris noticed.")
    parser.add_argument('-FD', '--FIX_DEPLOYED', help="Date of release.")
    parser.add_argument('-FDO', '--FIX_DEPLOYED_TURRISOS', help="Version of TurrisOS.")
    parser.add_argument('-gt', '--gitlab-token', help="Gitlab token.")
    parser.add_argument('-p', '--project', help="Gitlab project.")
    parser.add_argument('-c', '--config', help="Path to config file.", default="~/.gitlab_sec.ini")

    args = parser.parse_args(argv)
    si = SecIssue()

    if args.config:
        conf = load_config(args.config)
        if conf:
            gs = GitlabSec(conf["token"])
            project_path = conf["project_path"]
        else:
            print "Error! No config found. ( %s ) " % args.config
            print "Example of config file:"
            print "[gitlab]"
            print "token=XXXXXXXXXXXXXXX"
            print "project_path=turris/turris-os-packages"
            sys.exit()

    # note we want to be able rewrite some of these
    if args.gitlab_token:
        gs = GitlabSec(args.gitlab_token)

    if args.project:
        project_path = args.project

    if args.init:
        init_sec_issue(gs, si, project_path, args.init)

    if args.list_issues:
        bbb = get_list_issues(gs, si, project_path)
        table = AsciiTable(bbb)
        print table.table

    if args.update:
        print "Update issue %i" % args.update
        if args.PUBLICLY_KNOWN and check_date(args.PUBLICLY_KNOWN):
            print args.PUBLICLY_KNOWN
            update_sec_issue(gs, si, project_path, args.update, publicly_known=args.PUBLICLY_KNOWN)
        elif args.FIX_DEPLOYED and check_date(args.FIX_DEPLOYED):
            print args.FIX_DEPLOYED
            update_sec_issue(gs, si, project_path, args.update, fix_deployed=args.FIX_DEPLOYED)
        elif args.TURRIS_NOTICED and check_date(args.TURRIS_NOTICED):
            print args.TURRIS_NOTICED
            update_sec_issue(gs, si, project_path, args.update, turris_noticed=args.TURRIS_NOTICED)
        elif args.FIX_DEPLOYED_TURRISOS and check_date(args.FIX_DEPLOYED_TURRISOS):
            print args.FIX_DEPLOYED_TURRISOS
            update_sec_issue(gs, si, project_path, args.update, fix_deployed_turrisos=args.FIX_DEPLOYED_TURRISOS)
        else:
            print "No variable to update selected!"


if __name__ == "__main__":
    main_cli(sys.argv[1:])
