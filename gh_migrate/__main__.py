from pathlib import Path

# import hjson as json

# from .utils import utils
from .utils.cli_args import argparser

args = None


def main():
    global args 
    args = argparser.parse_args()
    print("Hello, world!")


if __name__ == "__main__":
    main()
