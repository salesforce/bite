# Base-Inflection Encoding
This repository contains code for the paper "[Mind Your Inflections! Improving NLP for Non-Standard Englishes with Base-Inflection Encoding](https://arxiv.org/abs/2004.14870)" (EMNLP 2020).

Authors: [Samson Tan](https://samsontmr.github.io), [Shafiq Joty](https://raihanjoty.github.io), [Lav Varshney](http://www.varshney.csl.illinois.edu), and [Min-Yen Kan](https://comp.nus.edu.sg/~kanmy)

# Installation
```
pip install git+https://github.com/salesforce/bite
```

# Usage
```
from bite import BITETokenizer

bite = BITETokenizer('moses')
print(bite.tokenize('I was going to the engine room!'))
```

We also include a script you can use to tokenize entire files (`run_bite.py`). The parser arguments (`--argument_name`) will give you an idea of the options supported by the script.

If you are using HuggingFace's BERT model, you may want to use the `BiteWordpieceTokenizer` instead. This is implementation we use in our BERT-based experiments.

## Pretokenization modes
Three types of pretokenizers are supported out of the box:

1. BertPreTokenizer (HuggingFace)
2. Moses (sacremoses)
3. Whitespace splitting

## Inflection symbols
Since subword tokenizers often operate on individual characters, running them on BITE-processed input with human readable inflection tags (e.g., `[VBD]`) would skew the character/subword statistics of the training corpus and occupy unnecessary slots in the subword vocabulary. Therefore, we recommend using single-character inflection symbols (by passing `map_to_single_char=True` to `tokenize`) when using BITE with such tokenizers.

# Dialectal Data
The scripts for cleaning the [CORAAL](https://oraal.uoregon.edu/coraal) data and scraping the Colloquial Singapore English data can be found in `paper_scripts`. Please be considerate when scraping and do not flood the site's servers with requests :)

# Citation
Please cite the following if you use the code in this repository:
```
@inproceedings{tan-etal-2020-mind,
    title = "Mind Your Inflections! {I}mproving {NLP} for Non-Standard {E}nglishes with {B}ase-{I}nflection {E}ncoding",
    author = "Tan, Samson  and
      Joty, Shafiq  and
      Varshney, Lav  and
      Kan, Min-Yen",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.455",
    pages = "5647--5663",
}
```
