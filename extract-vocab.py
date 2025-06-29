# This script is dedicated to the public domain under CC0 1.0. https://creativecommons.org/publicdomain/zero/1.0/

import sys
import os
import re
import requests
import argparse
from bs4 import BeautifulSoup


def remove_non_japanese(text: str) -> str:
    pattern = r"[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]"
    return re.sub(pattern, "", text)


if __name__ == "__main__":
    URL = "https://ja.wiktionary.org/wiki/Wiktionary:%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%AE%E5%9F%BA%E6%9C%AC%E8%AA%9E%E5%BD%991000"
    parser = argparse.ArgumentParser(description="Extract vocabulary from a webpage.")
    parser.add_argument(
        "--output",
        type=str,
        default="data/vocab.txt",
        help="Output file to save the extracted vocabulary.",
    )
    parser.add_argument(
        "--speech",
        type=str,
        nargs="+",
        default=["名詞", "動詞", "形容詞", "形容動詞"],
        help="Part of speech to filter the vocabulary. Multiple values can be specified.",
    )
    parser.add_argument(
        "--no-related",
        dest="related",
        action="store_false",
        help="Do not include related words in the output vocabulary.",
    )
    parser.set_defaults(related=True)
    args = parser.parse_args()

    res = requests.get(URL)
    if res.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {res.status_code}")
        sys.exit(1)
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table", class_="wikitable")
    if not table:
        print("No table found on the webpage.")
        sys.exit(1)
    words = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue
        pos = cols[0].get_text(strip=True)
        if pos not in args.speech:
            continue
        # cols[5]：読み
        # cols[6]：漢字表記
        # cols[7]：関連語など
        if cols[6].get_text(strip=True) == "":
            # 漢字表記がない場合は，読みを使う
            words.append(cols[5].get_text(strip=True))
        else:
            words.append(cols[6].get_text(strip=True))
        if not args.related:
            continue
        text = cols[7].get_text(strip=True)
        # （）で囲まれた部分を除去
        text = re.sub(r"\（.*?\）", "", text).strip()
        for word in text.split("、"):
            word = word.strip()
            if word:
                words.append(word)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    words = [remove_non_japanese(word) for word in words if remove_non_japanese(word)]
    words = sorted(set(words))
    with open(args.output, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")
    print(f"Extracted {len(words)} words to {args.output}")
