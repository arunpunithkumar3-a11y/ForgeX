from forgeX.config.manager import ConfigManager


def main():
    print("Initializing ForgeX CLI...")
    # 1. Create config file if it doesn't exist
    ConfigManager().create()

    # 2. Add your main agent logic here
    print("Welcome to ForgeX AI Coding Agent!")


if __name__ == "__main__":
    main()
