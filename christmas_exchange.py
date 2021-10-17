import argparse
from datetime import date
import json
from json.decoder import JSONDecodeError
import random
import sys


def set_seed(num):
    random.seed(num)


def generate_santa_list(people: list[str]) -> dict[str, str]:
    shuffled = random.sample(people, k=len(people))
    return dict(zip(people, shuffled))


def is_cyclic_permutation(santa_list: dict[str, str]) -> bool:
    all_people = set(santa_list)
    visited = set()
    current = list(all_people)[0]
    for _ in all_people:
        if current in visited:
            break
        visited.add(current)
        current = santa_list[current]
    return len(all_people) == len(visited)


def has_no_self_giving(santa_list: dict[str, str]) -> bool:
    for k, v in santa_list.items():
        if k == v:
            return False
    return True


def has_no_spouse_to_spouse(
    santa_list: dict[str, str], spouses: list[tuple[str, str]]
) -> bool:
    spouse_map = dict(spouses)
    spouse_map.update({v: k for k, v in spouse_map.items()})
    for k, v in santa_list.items():
        if spouse_map.get(k) == v:
            return False
    return True


def has_no_spouses_to_spouses(
    santa_list: dict[str, str], spouses: list[tuple[str, str]]
) -> bool:
    spouse_sets = {frozenset(couple) for couple in spouses}
    for couple in spouses:
        receivers = {santa_list[person] for person in couple}
        if receivers in spouse_sets:
            return False
    return True


def does_not_repeat_last_year(
    santa_list: dict[str, str], last_year: dict[str, str]
) -> bool:
    for k, v in santa_list.items():
        if last_year.get(k) == v:
            return False
    return True


def make_christmas_merry_again(people, spouses, last_year):
    while True:
        santa_list = generate_santa_list(people)
        if all(
            (
                is_cyclic_permutation(santa_list),
                has_no_self_giving(santa_list),
                has_no_spouse_to_spouse(santa_list, spouses),
                has_no_spouses_to_spouses(santa_list, spouses),
                does_not_repeat_last_year(santa_list, last_year),
            )
        ):
            return santa_list


def fa_la_la(santa_list, people):
    for person in people:
        print(f"{person} gives to {santa_list[person]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make Christmas great again.")
    parser.add_argument(
        "in_json",
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="A JSON file with input data",
    )
    parser.add_argument(
        "--out_json",
        "-o",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="Where to save the results",
    )
    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        help=(
            "Set the seed for the PRNG. "
            "Default is based on today's date YYYY - MM - DD."
        ),
    )
    args = parser.parse_args()
    try:
        data = json.load(args.in_json)
        people: list[str] = data["people"]
        spouses: list[tuple[str, str]] = data["spouses"]
        last_year: dict[str, str] = data["last_year"]
        today = date.today()
        seed = args.seed or today.year - today.month - today.day
        set_seed(seed)
        santa_list = make_christmas_merry_again(people, spouses, last_year)
        fa_la_la(santa_list, people)
        obj = {
            "today": str(today),
            "seed": seed,
            "santa_list": santa_list,
        }
        json.dump(obj, args.out_json, indent=2)
        args.out_json.write("\n")
    except (JSONDecodeError, KeyError):
        print(
            "Input is not properly formatted JSON.",
            'Required keys are "people", "spouses", "last_year".',
            "See README for more information."
        )
    finally:
        args.in_json.close()
        args.out_json.close()
