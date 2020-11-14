# -*- coding: utf-8 -*-
from typing import List, Union
from tokenizers.pre_tokenizers import BertPreTokenizer
from sacremoses import MosesTokenizer, MosesDetokenizer
from lemminflect import getLemma, getInflection
import string
from nltk.tag.perceptron import PerceptronTagger
from nltk.tag.mapping import map_tag


class BITETokenizer(object):
    inflection_tokens = ["[JJR]", "[JJS]", "[NNS]", "[NNPS]", "[RBR]",
                    "[RBS]", "[VBD]", "[VBG]", "[VBN]", "[VBP]", "[VBZ]"]
    single_char_map = {"[JJR]": chr(9774), "[JJS]": chr(9775), "[NNS]": chr(9776),
                        "[NNPS]": chr(9777), "[RBR]": chr(9778), "[RBS]": chr(9779),
                        "[VBD]": chr(9780), "[VBG]": chr(9781), "[VBN]": chr(9782),
                        "[VBP]": chr(9783), "[VBZ]": chr(9784)}
    reverse_single_char_map = {v:k for k,v in single_char_map.items()}
    lemma_tags = {'NN', 'VB', 'JJ', 'RB', 'MD', "NNP"}
    have_inflections = {'NOUN', 'ADJ', 'VERB'}


    def __init__(self, pretokenizer='moses'):
        self.tagger = PerceptronTagger()
        self.pretok_type = pretokenizer
        if pretokenizer == 'bertpretokenizer':
            self.pretokenizer = BertPreTokenizer()
        elif pretokenizer == 'moses':
            self.pretokenizer = MosesTokenizer()
            self.detokenizer = MosesDetokenizer()
        elif pretokenizer == 'whitespace':
            pass
        else:
            raise ValueError("pretokenizer must be 'bertpretokenizer', 'moses', or 'whitespace'.")


    def _pretokenize(self, sentence: str) -> List[str]:
        if self.pretok_type == 'bertpretokenizer':
            return [tup[0] for tup in self.pretokenizer.pre_tokenize(sentence)]
        elif self.pretok_type == 'whitespace':
            return sentence.split()
        else:
            return self.pretokenizer.tokenize(sentence)


    def tokenize(self, sentence: Union[str, List[str]],
                 pretokenize: bool=True, map_to_single_char: bool=False) -> List[str]:
        if pretokenize:
            pretokenized = self._pretokenize(sentence)
        else:
            # Allow users to pass in a list of tokens if using custom pretokenizers
            pretokenized = sentence
        ptb_pos_tagged = self.tagger.tag(pretokenized)
        universal_pos_tagged = [(token, map_tag("en-ptb", 'universal', tag))
                                for (token, tag) in ptb_pos_tagged]
        tokenized = []
        for i, (word, pos) in enumerate(ptb_pos_tagged):
            if universal_pos_tagged[i][1] in self.have_inflections and word not in (string.punctuation+'—') and pos not in self.lemma_tags:
                lemma = getLemma(word, upos=universal_pos_tagged[i][1])[0]
                if not lemma:
                    lemma = word
                tokenized.append(lemma)
                tokenized.append('['+pos+']')
            else:
                tokenized.append(word)
        if map_to_single_char:
            tokenized = [self.single_char_map[token] if token in self.inflection_tokens else token for token in tokenized]
        return tokenized

    def detokenize(self, tokens: List[str], as_list: bool=False) -> Union[str, List[str]]:
        result = []
        for i, token in enumerate(tokens):
            # combine wordpiece tokens
            if token in self.reverse_single_char_map:
                token = self.reverse_single_char_map[token]
            if token in self.inflection_tokens:
                if i != 0:
                    inflected = getInflection(result[-1], tag=token[1:-1])
                    if inflected:
                        result[-1] = inflected[0]
            else:
                result.append(token)

        if as_list:
            # Allow users to detokenize using their own detokenizers
            return result
        if self.pretok_type == 'moses':
            return self.detokenizer.detokenize(result)
        return ' '.join(result)
