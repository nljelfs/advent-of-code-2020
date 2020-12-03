#!/usr/bin/python3

# Day 1 of https://adventofcode.com/2020

import argparse
from typing import List


def partition(lines: List[str], thresh: int):
    """
    Partition list of lines into two sets of integers:
    (> threshold, <= threshold).
    """
    small, large = [], []
    for l in lines:
        if int(l) > thresh:
            large.append(int(l))
        else:
            small.append(int(l))
    print(f"Partitions: ({len(large)} > {thresh}, {len(small)} <= {thresh})")
    return large, small


def check_two(x: int, y: int):
    """Check whether two integers sum to 2020."""
    if x + y == 2020:
        print(f"{x} + {y} = {x+y}")
        print(f"{x} * {y} = {x*y}")
        return True
    return False


def check_three(x: int, y: int, z: int):
    """Check whether three integers sum to 2020."""
    if x + y + z == 2020:
        print(f"{x} + {y} + {z} = {x+y+z}")
        print(f"{x} * {y} * {z} = {x*y*z}")
        return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", type=argparse.FileType(),
                   help="input file (one natural number per line)")
    args = p.parse_args()
    lines = args.file.readlines()
    print(f"Read {len(lines)} lines from {args.file.name}")

    # 2 numbers sum to 2020
    solved = False
    large, small = partition(lines, 1010)
    for i in large:
        for j in small:
            solved = check_two(i, j)
            if solved:
                break
        if solved:
            break
    if not solved:
        print("x + y = 2020 not found")

    # 3 numbers sum to 2020
    for i in large:
        for j in small:
            for k in small:
                if j == k:
                    continue
                solved = check_three(i, j, k)
                if solved:
                    break
            if solved:
                break
        if solved:
            break
    if not solved:
        print("x + y + z = 2020 not found")


if __name__ == "__main__":
    main()
