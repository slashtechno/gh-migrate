import argparse
import os
import dotenv
from pathlib import Path
import sys

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

    # argparser.add_argument(
    #     "--migrate-all-repositories",
    #     action="store_true",
    #     help="Migrate all repositories from user to org",
    #     default=False
    # )
    argparser.add_argument(
        "--token",
        type=str,
        help="GitHub Token",
        default=os.environ["GH_MIGRATE_TOKEN"]
        if "GH_MIGRATE_TOKEN" in os.environ and os.environ["GH_MIGRATE_TOKEN"] != ""
        else None,
    )
    argparser.add_argument(
        "--new-owner",
        type=str,
        help="New owner of the repositories",
        default=os.environ["GH_MIGRATE_NEW_OWNER"] if "GH_MIGRATE_NEW_OWNER" in os.environ 
        and os.environ["GH_MIGRATE_NEW_OWNER"] != "" else None,
    )
    argparser.add_argument(
        "--team-id",
        type=int,
        help="Team IDs to add the repositories to",
        action="append",
        default=[int(os.environ["GH_MIGRATE_TEAM_ID"])] if "GH_MIGRATE_TEAM_ID" in os.environ
        and os.environ["GH_MIGRATE_TEAM_ID"] != "" else [],
    )

    check_required_args(["token", "new_owner"], argparser)

    # example_group = argparser.add_argument_group("example")
    # example_group.add_argument(
    #     "--flag",
    #     default=os.environ["ENV_VAR"]
    #     if "ENV_VAR" in os.environ and os.environ["ENV_VAR"] != ""
    #     else None,
    #     type=str,
    #     help="Example str flag that can be set via ENV_VAR",
    # )

def check_required_args(required_args: list[str], argparser: argparse.ArgumentParser):
    """
    Check if required arguments are set
    Useful if using enviroment variables with argparse as default and required are mutually exclusive
    """
    for arg in required_args:
        args = argparser.parse_args()
        if getattr(args, arg) is None:
            # raise ValueError(f"{arg} is required")
            print(f"{arg} is required")
            sys.exit(1)
set_argparse()