from argparse import ArgumentParser
from os import listdir, makedirs, remove
from os.path import join as joinpath, basename, splitext
from typing import *


def is_augment(filename: str) -> bool:
    bn = basename(filename)
    bn, _ = splitext(bn)
    try:
        int(bn)
        return False
    except ValueError:
        return True


def get_paths(path: str) -> List[str]:
    files = listdir(path)
    return [joinpath(path, file) for file in files]


def main():
    parser = ArgumentParser()
    parser.add_argument("--directory", "-d", dest="directory", required=True)
    args = parser.parse_args()
    for file in get_paths(args.directory):
        if is_augment(file):
            remove(file)


main()
