# -*- coding: utf-8 -*-
import argparse
from tqdm import tqdm
from bite import BITETokenizer
import os


parser = argparse.ArgumentParser()

parser.add_argument(
        "--data", "-d", default=None, type=str, required=True, help="The input data file (a text file)."
    )

parser.add_argument(
        "--output_dir", "-o", default=None, type=str, required=True, help="The output directory."
    )

parser.add_argument(
        "--data_len", '-l', default=None, type=int, required=False, help="Number of examples for ETA prediction."
    )

parser.add_argument(
        "--concat_inflections", "-c", action='store_true', required=False, help="Concatenate inflection tokens with their base forms."
    )

parser.add_argument(
        "--inflection_tag", "-it", action='store_true', required=False, help="Use full inflection tag instead of single character."
    )
parser.add_argument(
        "--generate", "-g", action='store_true', required=False, help="Decode raw text from BITE text."
    )

mutex_group = parser.add_mutually_exclusive_group()

mutex_group.add_argument("--moses", action='store_true', required=False, help="Use the Moses tokenizer for pretokenization.")

mutex_group.add_argument("--whitespace", "-ws", action='store_true', required=False, help="Pretokenize by splitting on whitespace.")

mutex_group.add_argument("--bert", action='store_true', required=False, help="Pretokenize with BERT Pretokenizer.")

args = parser.parse_args()

tqdm_total = args.data_len

if args.moses:
    bite = BITETokenizer('moses')
elif args.whitespace:
    bite = BITETokenizer('whitespace')
else:
    bite = BITETokenizer('bertpretokenizer')


single_char = not args.inflection_tag

print('data path:', args.data)
print('output dir:', args.output_dir)

if args.generate:
    out_name = os.path.join(args.output_dir, args.data.split('/')[-1]+'.decoded')
    with open(args.data, 'r',) as in_file:
        with open(out_name, 'w') as out_file:
            for line in tqdm(in_file, total=tqdm_total):
                tokens = line.strip().split()
                text = bite.detokenize(tokens).replace('@ - @', '@-@').replace('& apos ; ', '&apos;').replace('& quot ;', '&quot;')
                out_file.write(text+'\n')
else:
    out_ext = '.bite'
    if args.concat_inflections:
        out_ext += '.concat'
    out_name = os.path.join(args.output_dir, args.data.split('/')[-1]+out_ext)

    with open(args.data, 'r',) as in_file:
        with open(out_name, 'w') as out_file:
            for line in tqdm(in_file, total=tqdm_total):
                tokenized = ' '.join(bite.tokenize(line.strip(), map_to_single_char=single_char))
                if args.concat_inflections:
                    for char in bite.single_char_map.values():
                        tokenized = tokenized.replace(' '+char, char)
                out_file.write(tokenized+'\n')
