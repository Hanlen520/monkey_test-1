from runmonkey2 import MonkeyTester


if __name__ == "__main__":
    monkey = MonkeyTester()
    for config_info in monkey.get_config():
        monkey.uninstall_app(config_info)