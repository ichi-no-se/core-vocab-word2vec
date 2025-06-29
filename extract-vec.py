# This script is dedicated to the public domain under CC0 1.0. https://creativecommons.org/publicdomain/zero/1.0/

import os
import json
import argparse
import gensim

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Extract vocabulary from a word2vec model.")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to the word2vec model file.",
    )
    parser.add_argument(
        "--vocab",
        type=str,
        default="data/vocab.txt",
        help="Input file containing the vocabulary to extract.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/vec.json",
        help="Output file to save the extracted vectors in JSON format.",
    )
    args=parser.parse_args()
    model=gensim.models.KeyedVectors.load(args.model)

    vectors = {}
    with open(args.vocab, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word in model.key_to_index:
                vectors[word] = model[word].tolist()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(vectors, f, ensure_ascii=False)



