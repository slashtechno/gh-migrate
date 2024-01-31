import argparse
import os
import dotenv
from pathlib import Path

argparser = None


def set_argparse():
    global argparser

    if Path(".env").is_file():
        dotenv.load_dotenv()
        print("Loaded .env file")
    else:
        print("No .env file found")


    argparser = argparse.ArgumentParser(
        prog="GH Migrate",
        description="Migrate from GH user to GH org",  # noqa: E501
        epilog=":)",
    )


    # example_group = argparser.add_argument_group("example")
    # example_group.add_argument(
    #     "--flag",
    #     default=os.environ["ENV_VAR"]
    #     if "ENV_VAR" in os.environ and os.environ["ENV_VAR"] != ""
    #     else None,
    #     type=str,
    #     help="Example str flag that can be set via ENV_VAR",
    # )

set_argparse()