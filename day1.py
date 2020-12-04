#!/usr/bin/python3

# Day 1 of https://adventofcode.com/2020

import argparse
import logging
from typing import Set, Tuple


def _partition(ints: Set[int], threshold: int) -> Tuple[Set[int], Set[int]]:
    """
    Partition list of lines into two sets of integers:
    (> threshold, <= threshold).
    """
    small: Set[int] = set()
    large: Set[int] = set()
    for l in ints:
        if l > threshold:
            large.add(l)
        else:
            small.add(l)
    logging.debug(
        "Partitions: (%u > %u, %u <= %u)",
        len(large),
        threshold,
        len(small),
        threshold,
    )
    return large, small


def _check_two(x: int, y: int) -> bool:
    """Check whether two integers sum to 2020."""
    return x + y == 2020


def _check_three(x: int, y: int, z: int) -> bool:
    """Check whether three integers sum to 2020."""
    return x + y + z == 2020


def _log_solutions(solutions: Set[Tuple]):
    if solutions == set():
        logging.warning("No solutions found")
    else:
        for solution in solutions:
            logging.info(
                "%s = %u",
                " + ".join([str(i) for i in solution]),
                sum(list(solution)),
            )
            product = 1
            for x in solution:
                product *= x
            logging.info(
                "%s = %u", " * ".join([str(i) for i in solution]), product
            )
        logging.info(
            "%u solution%s found",
            len(solutions),
            "" if len(solutions) == 1 else "s",
        )


def _main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--rubbish-method",
        action="store_true",
        help="rubbish (lucky) partitioning method",
    )
    p.add_argument(
        "file",
        type=argparse.FileType(),
        help="input file (one natural number per line)",
    )
    args = p.parse_args()
    lines = args.file.readlines()

    logging.basicConfig(level=logging.INFO)
    logging.info("Read %u lines from %s", len(lines), args.file.name)

    if not args.rubbish_method:
        # Obvious method ;-)
        ints = [int(l) for l in lines]
        set_ints, dupes = set(), set()
        for i in ints:
            if i in set_ints:
                dupes.add(i)
            else:
                set_ints.add(i)

        # 2 numbers sum to 2020
        solutions = set()
        for i in ints:
            target = 2020 - i
            if i == target and i not in dupes:
                continue
            if tuple(sorted([i, target])) in solutions:
                continue
            if target in set_ints:
                assert _check_two(i, target)
                solutions.add(tuple(sorted([i, target])))
        _log_solutions(solutions)

        # 3 numbers sum to 2020
        solutions = set()
        for i in ints:
            thresh = 2020 - i
            _, small = _partition(set_ints, thresh)
            for j in small:
                target = thresh - j
                if tuple(sorted([i, j, target])) in solutions:
                    continue
                if target in small:
                    assert _check_three(i, j, target)
                    solutions.add(tuple(sorted([i, j, target])))
        _log_solutions(solutions)
    else:
        # Rubbish partition method
        large, small = _partition(set(map(int, lines)), 1010)

        # 2 numbers sum to 2020
        solutions = {(i, j) for i in large for j in small if _check_two(i, j)}
        _log_solutions(solutions)

        # 3 numbers sum to 2020
        solutions = set()
        for i in large:
            for j in small:
                for k in small:
                    if j == k:
                        continue
                    if tuple(sorted([i, j, k])) in solutions:
                        continue
                    if _check_three(i, j, k):
                        solutions.add(tuple(sorted([i, j, k])))
        _log_solutions(solutions)


if __name__ == "__main__":
    _main()
