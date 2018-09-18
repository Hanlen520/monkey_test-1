#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import shutil
import time
from time import ctime
import re
from utils.config import Config


class MonkeyTester(object):
    def __init__(self):
        pass

    def get_config(self):
        configs = Config()
        for config in configs.get():
            self.config_info = config
            yield self.config_info

    def chk_install(self, config_info):
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

    def install_app(self, config_info):
        phone_name = config_info.get('phone')
        apk_name = config_info.get('apk_name')
        if phone_name:
            install_app_command = "adb -s {0} install ./apk/{1}".format(phone_name, apk_name)
            print(install_app_command)
            result = os.system(install_app_command)
            if result == 0:
                print("Install successful")
                return True
            else:
                print("Failed to install")
                return False

    def uninstall_app(self, config_info):
        phone_name = config_info.get('phone')
        package_name = config_info.get('package_name')
        if phone_name:
            uninstall_app_command = "adb -s {0} uninstall {1}".format(phone_name, package_name)
            print(uninstall_app_command)
            result = os.popen(uninstall_app_command).readlines()
            if " ".join(result).strip("\n") == "Success":
                print("Uninstall successful")
                return True
            else:
                print("Failed to uninstall")
                return False

    @staticmethod
    def kill_app(config):
        force_stop_app = "adb -s {} shell am force-stop {}".format(config.get('phone'),\
                                                                   config.get('package_name'))
        print(force_stop_app)
        result = os.system(force_stop_app)
        if result == 0:
            print("Kill the server success")
        else:
            print("Un_know result")

    @classmethod
    def kill_app2(cls, config):
        force_stop_app = "adb -s {} shell am force-stop {}".format(config.get('phone'),\
                                                                   config.get('package_name'))
        print(force_stop_app)
        result = os.system(force_stop_app)
        if result == 0:
            print("Kill the server success")
        else:
            print("Un_know result")

    @classmethod
    def kill_monkey(cls, config_info):
        get_monkey_pid = 'adb -s {} shell "ps |grep monkey"'.format(config_info.get('phone'))
        pid_line = os.popen(get_monkey_pid).readlines()
        if len("".join(pid_line).split(" ")) >= 5:
            pid_num = "".join(pid_line).split(" ").pop(5)
            kill_cmd = 'adb -s {0} shell "kill {1}"'.format(config_info.get('phone'), pid_num)
            result = os.popen(kill_cmd).readlines()
            print("Success" if len(result) == 0 else None)
        else:
            print("Monkey has stoped")

    def run_monkey(self, config_info):
        # self.kill_app(self.config_info)
        monkey_cmd = "adb -s {0} shell monkey -v -v -v "\
                     "-p {1} --ignore-crashes --ignore-timeouts --ignore-security-exceptions "\
                     "-s 45906 --throttle 100 {2} 1>.\\report\\monkey_{3}.txt 2>.\\report\\monkey_error_{4}.txt".\
            format(config_info.get("phone"), config_info.get("package_name"),\
                   int(config_info.get("monkey_count")), config_info.get("phone"), config_info.get("phone"))
        print(monkey_cmd)
        os.popen(monkey_cmd).readlines()

    def create_bug_report(self,config_info):
        print("Create bug report file")
        # work_space = os.path.abspath(".")
        # report_time = time.strftime("%m-%d_%H_%M_%S", time.localtime())
        bug_report = "adb -s {0} shell bugreport > .\\report\\bug_report_{1}.txt".format( \
            config_info.get("phone"), config_info.get("phone"))
        os.popen(bug_report)
        time.sleep(10)
        print("Create bug report file,success")

    def log_analysis(self, config_info):
        print(self.config_info)
        filename = ".\\report\\bug_report_{}.txt".format(config_info.get("phone"))
        with open(filename,'r',encoding='utf-8') as fp:
            words = fp.readlines()
            print(words)
            for word in words:
                p1 = r"(ANR|CRASH|kernel.) (.*?)+"
                pattern1 = re.compile(p1, re.I)
                matcher1 = re.search(pattern1, word)
                if matcher1:
                    print(matcher1)

    def chkbugreport(self, config_info):
        filename = ".\\report\\bug_report_{}.txt".format(config_info.get("phone"))
        filefolder = ".\\report\\bug_report_{}_out".format(config_info.get("phone"))
        chk_cmd = "chkbugreport.jar {}".format(filename)
        if os.path.isdir(filefolder):
            shutil.rmtree(filefolder)
        result = os.system(chk_cmd)
        return result

def install_run_bug_ana():
    monkey.run_monkey(config_info)
    monkey.create_bug_report(config_info)
    monkey.chkbugreport(config_info)

if __name__ == "__main__":
    # monkey = MonkeyTester()
    # ret = monkey.chk_install()
    # if ret:
    #     monkey.uninstall_app()
    #     monkey.install_app()
    #     # monkey.kill_app2(configs)
    #     # monkey.run_monkey()
    #     monkey.create_bug_report()
    # else:
    #     monkey.install_app()
    #     monkey.run_monkey()
    #     monkey.create_bug_report()
    monkey = MonkeyTester()
    for config_info in monkey.get_config():
        print(config_info)
        ret = monkey.chk_install(config_info)
        if ret:
            print("Start Time:",ctime())
            monkey.run_monkey(config_info)
            # install_run_bug_ana()
            print("End Time:", ctime())
        else:
            monkey.install_app(config_info)
            # install_run_bug_ana()
            monkey.run_monkey(config_info)