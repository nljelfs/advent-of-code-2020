#!/usr/bin/python3

# Day 3 of https://adventofcode.com/2020

import argparse
import itertools
import logging
from typing import List


def is_tree(lines: List[str], line: int, char: int) -> bool:
    """
    Is there a tree in position (line, char) in the set of lines
    repeated infinitely to the right?
    """
    return lines[line][char % len(lines[line])] == "#"


def navigate(lines: List[str], line_step: int, char_step: int) -> int:
    """
    Count the trees encountered and number of steps when navigating
    through the map that "lines" represents.
    """

    positions = list(
        zip(
            range(line_step, len(lines), line_step),
            itertools.count(char_step, char_step),
        )
    )
    trees = 0
    for line, char in positions:
        if is_tree(lines, line, char):
            logging.debug("Tree at (%u, %u)", line, char)
            trees += 1
        else:
            logging.debug("No tree at (%u, %u)", line, char)
    logging.info(
        "(%u, %u): encountered %u trees in %u steps",
        line_step,
        char_step,
        trees,
        len(positions),
    )
    return trees


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "-l",
        "--log-level",
        choices=("DEBUG", "INFO"),
        default="INFO",
        help="log level",
    )
    p.add_argument(
        "file",
        type=argparse.FileType(),
        help="input file (password policy + password per line)",
    )
    args = p.parse_args()

    logging.basicConfig(level=args.log_level)

    lines = args.file.read().splitlines()
    logging.info("Read %u lines from %s", len(lines), args.file.name)

    # Part 1
    logging.info("Part 1")
    navigate(lines, 1, 3)

    # Part 2
    logging.info("Part 2")
    total = 1
    for right, down in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        total *= navigate(lines, down, right)
    logging.info("Product = %u", total)


if __name__ == "__main__":
    main()
