#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import time
import sys
import re
from utils.config import Config

def get_work_config():
    apk_name = ''
    exec_count = 2
    monkey_count = 1000
    coding = sys.getdefaultencoding()
    config = {"monkey_count": monkey_count, "exec_count": exec_count, 'apk_name': apk_name}
    with open("./.config", "r", encoding=coding) as fp:
        while True:
            line = fp.readline()
            if line:
                lines_splict = line.strip().split(":")
                if lines_splict[0] == 'phone':
                    config['phone'] = lines_splict[1].strip()
                elif lines_splict[0] == 'apk_name':
                    config['apk_name'] = lines_splict[1].strip()
                elif lines_splict[0] == 'package_name':
                    config['package_name'] = lines_splict[1].strip()
                elif lines_splict[0] == 'monkey_count':
                    config['monkey_count'] = lines_splict[1].strip()
                elif lines_splict[0] == 'exec_count':
                    config['exec_count'] = lines_splict[1].strip()
            else:
                break
    print(config)
    return config

def get_config():
    configs = Config()
    for config in configs.get():
        yield config

def chk_install(config_info):
    phone_name = config_info.get('phone')
    package_name = config_info.get('package_name')
    if phone_name:
        check_app_command = "adb -s {0} shell pm list packages -f".format(phone_name)
        results = os.popen(check_app_command).readlines()
        all_packages = []
        for result in results:
            if len(result.split("=")) == 2:
                packages = result.split("=")[1].strip("\n")
                all_packages.append(packages)
        if package_name in all_packages:
            print("App had installed")
            return True
        else:
            print("App is not installed")
            return False


def install_app(config_info):
    phone_name = config_info.get('phone')
    apk_name = config_info.get('apk_name')
    if phone_name:
        install_app_command = "adb -s {0} install ./apk/{1}".format(phone_name, apk_name)
        print(install_app_command)
        # result = os.popen(install_app_command).readlines()
        result = os.system(install_app_command)
        if result == 0:
            print("Install successful")
            return True
        else:
            print("Failed to install")
            return False


def uninstall_app(config_info):
    phone_name = config_info.get('phone')
    package_name = config_info.get('package_name')
    if phone_name:
        uninstall_app_command = "adb -s {0} uninstall {1}".format(phone_name, package_name)
        print(uninstall_app_command)
        result = os.popen(uninstall_app_command).readlines()
        if " ".join(result).rstrip("\n").strip(" ") == "Success\n":
            print("Uninstall successful")
            return True
        else:
            print("Failed to uninstall")
            return False


def kill_app(config_info):
    force_stop_app = "adb -s {} shell am force-stop {}".format(config_info.get('phone'),\
                                                               config_info.get('package_name'))
    print(force_stop_app)
    result = os.system(force_stop_app)
    if result == 0:
        print("Kill the server success")
    else:
        print("Unknow result")


def run_monkey(config_info):
    kill_app(config_info)
    monkey_cmd = "adb -s {0} shell monkey -v -v -v "\
                 "-p {1} --ignore-crashes --ignore-timeouts --ignore-security-exceptions "\
                 "-s 123456 --throttle 10 {2} 1>.\\report\\monkey.txt 2>.\\report\\monkey_error.txt".\
        format(config_info.get("phone"), config_info.get("package_name"), int(config_info.get("monkey_count")))
    print(monkey_cmd)
    os.popen(monkey_cmd).readlines()


def create_bug_report(config_info):
    print("Create bug report file")
    # work_space = os.path.abspath(".")
    # report_time = time.strftime("%m-%d_%H_%M_%S", time.localtime())
    bug_report = "adb -s {0} shell bugreport > .\\report\\bug_report_{}.txt".format(\
        config_info.get("phone"),config_info.get("phone"))
    os.popen(bug_report)
    time.sleep(10)
    print("Create bug report file,success")


def log_analysis(config_info):
    filename = ".\\report\\bug_report_{}.txt".format(config_info.get("phone"))
    with open(filename) as fp:
        words = fp.readlines()
        for word in words:
            p1 = r"(ANR|CRASH|kernel.) (.*?)+"
            pattern1 = re.compile(p1, re.I)
            matcher1 = re.search(pattern1, word)
            if matcher1:
                print(matcher1)

config = get_config()
for i in config:
    print(i)
# config = get_work_config()
# ret = chk_install(config)
# if ret:
#     uninstall_app(config)
    # install_app(config)
    # run_monkey(config)
    # create_bug_report(config)
# else:
    # install_app(config)
#     run_monkey(config)
#     create_bug_report(config)
# # log_analysis()
