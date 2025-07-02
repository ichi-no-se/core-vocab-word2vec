# This script is dedicated to the public domain under CC0 1.0. https://creativecommons.org/publicdomain/zero/1.0/

import os
import json
import argparse
import struct

def compress_vec_json(input_path, vocab_out, vecs_out):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    vocab = []
    vecs = []
    for word, vec in data.items():
        vocab.append(word)
        vecs.append(vec)
    num_words = len(vocab)
    vec_len = len(vecs[0])

    # Save vocab
    with open(vocab_out, "w", encoding="utf-8") as f:
        for word in vocab:
            f.write(word + "\n")

    # Save vectors as binary
    with open(vecs_out, "wb") as f:
        f.write(struct.pack('<i', num_words))
        f.write(struct.pack('<i', vec_len))
        for vec in vecs:
            for value in vec:
                f.write(struct.pack('<f', value))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress vector JSON to binary format.")
    parser.add_argument(
        "--input",
        type=str,
        help="Input JSON file containing vectors.",
    )
    parser.add_argument(
        "--vocab_out",
        type=str,
        help="Output file for vocabulary.",
    )
    parser.add_argument(
        "--vecs_out",
        type=str,
        help="Output file for vectors in binary format.",
    )
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.vocab_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.vecs_out), exist_ok=True)
    compress_vec_json(args.input, args.vocab_out, args.vecs_out)
