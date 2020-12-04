#!/usr/bin/python3

# Day 4 of https://adventofcode.com/2020

import argparse
import logging
import re
from typing import List, Optional


def _main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "-l",
        "--log-level",
        choices=("DEBUG", "INFO"),
        default="INFO",
        help="log level",
    )
    p.add_argument(
        "file", type=argparse.FileType(), help="input file (passports)"
    )
    args = p.parse_args()

    logging.basicConfig(level=args.log_level)

    lines = args.file.read().splitlines()
    logging.info("Read %u lines from %s", len(lines), args.file.name)

    curr_passport = {}
    passports = []
    for l in lines:
        l = l.strip()
        if l != "":
            for f in l.split():
                k, v = f.split(":", 1)
                curr_passport[k] = v
        elif curr_passport != {}:
            passports.append(curr_passport)
            curr_passport = {}
    if curr_passport != {}:
        passports.append(curr_passport)
        curr_passport = {}

    # Part 1 - required fields
    valid_req, invalid_req = [], []
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for p in passports:
        if not all(field in p for field in required_fields):
            invalid_req.append(p)
        else:
            valid_req.append(p)
    logging.info(
        "%u valid, %u invalid (missing required fields) passports",
        len(valid_req),
        len(invalid_req),
    )

    # Part 2 - required and valid fields
    def _check_range(field: str, min: int, max: int) -> bool:
        return int(field) >= min and int(field) <= max

    def _check_height(field: str) -> bool:
        match = re.match(r"(?P<val>\d+)(?P<unit>cm|in)$", field)
        if match is None:
            return False
        if match.group("unit") == "cm":
            return _check_range(match.group("val"), 150, 193)
        elif match.group("unit") == "in":
            return _check_range(match.group("val"), 59, 76)
        return False

    def _check_regexp(field: str, regexp: str) -> bool:
        return re.match(regexp, field) is not None

    valid_val, invalid_val = [], []
    for p in valid_req:
        checks = [
            (_check_range, (p["byr"], 1920, 2002)),
            (_check_range, (p["iyr"], 2010, 2020)),
            (_check_range, (p["eyr"], 2020, 2030)),
            (_check_height, (p["hgt"],)),
            (_check_regexp, (p["hcl"], r"#[0-9a-f]{6}$")),
            (_check_regexp, (p["ecl"], r"(amb|blu|brn|gry|grn|hzl|oth)$")),
            (_check_regexp, (p["pid"], r"[0-9]{9}$")),
        ]

        for check, args in checks:
            if not check(*args):
                logging.info("Check failed: %s%s", check.__name__, args)
                invalid_val.append(p)
                break
        else:
            valid_val.append(p)
    logging.info(
        "%u valid, %u invalid (invalid fields) passports",
        len(valid_val),
        len(invalid_val),
    )


if __name__ == "__main__":
    _main()
