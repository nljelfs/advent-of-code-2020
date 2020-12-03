#!/usr/bin/python3

# Day 3 of https://adventofcode.com/2020

import argparse
import re
import sys


def valid_occurences(min, max, letter, pw):
    """Is password valid based on min/max occurrences of letter?"""
    found = 0
    for l in pw:
        if l == letter:
            found += 1
        if found > max:
            return False
    if found < min:
        return False
    return True


def valid_positions(position1, position2, letter, pw):
    """Is password valid based on positions in which letter found?"""
    return (pw[position1-1] == letter) != (pw[position2-1] == letter)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", type=argparse.FileType(),
                   help="input file (password policy + password per line)")
    args = p.parse_args()

    valid_occurrences_pws, valid_positions_pws = [], []
    regexp = r"(?P<one>\d+)-(?P<two>\d+) (?P<letter>[a-z]): (?P<password>.*)"
    for l in args.file:
        match = re.match(regexp, l)
        assert match is not None, f"{l} doesn't match {regexp}"
        one, two = int(match.group("one")), int(match.group("two"))
        letter, password = match.group("letter"), match.group("password")
        if valid_occurences(one, two, letter, password):
            valid_occurrences_pws.append(l)
        if valid_positions(one, two, letter, password):
            valid_positions_pws.append(l)
    print(f"{len(valid_occurrences_pws)} valid occurrences passwords")
    print(f"{len(valid_positions_pws)} valid positions passwords")


if __name__ == "__main__":
    main()
