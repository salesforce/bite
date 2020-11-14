# -*- coding: utf-8 -*-
from transformers import BertTokenizer, BasicTokenizer
from lemminflect import getLemma, getInflection
import string
from nltk.tag.perceptron import PerceptronTagger
from nltk.tag.mapping import map_tag


class BiteWordpieceTokenizer(BertTokenizer):
    def __init__(self, vocab_file, do_lower_case=True, never_split=None,
                 additional_special_tokens=["[JJR]", "[JJS]", "[NNS]", "[NNP]", "[NNPS]", "[RBR]",
                                  "[RBS]", "[VBD]", "[VBG]", "[VBN]", "[VBP]", "[VBZ]"], **kwargs):
        self.inflection_tokens = additional_special_tokens
        self.tagger = PerceptronTagger()
        super().__init__(vocab_file, do_lower_case=do_lower_case, never_split=never_split, additional_special_tokens=additional_special_tokens, **kwargs)

        self.have_inflections = {'NOUN', 'ADJ', 'VERB'}
        self.lemma_tags = {'NN', 'VB', 'JJ', 'RB', 'MD', "NNP"}
        self.do_lower_case = do_lower_case
        if do_lower_case:
            self.cased_tokenizer = BasicTokenizer(do_lower_case=False, never_split=never_split)
        else:
            self.cased_tokenizer = self.basic_tokenizer

    def _tokenize(self, text):
        tokenized = self.cased_tokenizer.tokenize(text, never_split=self.all_special_tokens)
        #print(tokenized)
        ptb_pos_tagged = self.tagger.tag(tokenized)
        #print(pos_tagged)
        #print(pos_tagged)
        universal_pos_tagged = [(token, map_tag("en-ptb", 'universal', tag))
                                for (token, tag) in ptb_pos_tagged]
        #print(universal_pos_tagged)
        split_tokens = []
        for i, (word, pos) in enumerate(ptb_pos_tagged):
            if self.do_lower_case:
                word = word.lower()
            if universal_pos_tagged[i][1] in self.have_inflections and word not in (string.punctuation+'—') and pos not in self.lemma_tags:
                # (universal_)pos_tagged in the form of [(word, pos),(word, pos),...]
                # getLemma returns a tuple (lemma,)
                lemma = getLemma(word, upos=universal_pos_tagged[i][1])[0]
                if not lemma:
                    lemma = word
                wordpieced = self.wordpiece_tokenizer.tokenize(lemma)
                #print(wordpieced)
                split_tokens.extend(wordpieced)
                split_tokens.append('['+pos+']')
            else:
                wordpieced = self.wordpiece_tokenizer.tokenize(word)
                split_tokens.extend(wordpieced)
        return split_tokens

    def convert_tokens_to_string(self, tokens):
        result = []
        for i, token in enumerate(tokens):
            # combine wordpiece tokens
            if len(token) > 2 and token[:2] == '##':
                if result:
                    result[-1] += token[2:]
                else:
                    result.append(token[2:])
                continue
            if token in self.inflection_tokens:
                if i != 0:
                    inflected = getInflection(result[-1], tag=token[1:-1])
                    if inflected:
                        result[-1] = inflected[0]
            else:
                result.append(token)
        return ' '.join(result)


class LemmaWordpieceTokenizer(BertTokenizer):
    def __init__(self, vocab_file, do_lower_case=True, never_split=None,
                 additional_special_tokens=["[JJR]", "[JJS]", "[NNS]", "[NNP]", "[NNPS]", "[RBR]",
                                  "[RBS]", "[VBD]", "[VBG]", "[VBN]", "[VBP]", "[VBZ]"], **kwargs):
        self.inflection_tokens = additional_special_tokens
        self.tagger = PerceptronTagger()
        super().__init__(vocab_file, do_lower_case=do_lower_case, never_split=never_split, additional_special_tokens=additional_special_tokens, **kwargs)

        self.have_inflections = {'NOUN', 'ADJ', 'VERB'}
        self.lemma_tags = {'NN', 'VB', 'JJ', 'RB', 'MD', "NNP"}
        self.do_lower_case = do_lower_case
        if do_lower_case:
            self.cased_tokenizer = BasicTokenizer(do_lower_case=False, never_split=never_split)
        else:
            self.cased_tokenizer = self.basic_tokenizer

    def _tokenize(self, text):
        tokenized = self.cased_tokenizer.tokenize(text, never_split=self.all_special_tokens)
        #print(tokenized)
        ptb_pos_tagged = self.tagger.tag(tokenized)
        #print(pos_tagged)
        #print(pos_tagged)
        universal_pos_tagged = [(token, map_tag("en-ptb", 'universal', tag))
                                for (token, tag) in ptb_pos_tagged]
        #print(universal_pos_tagged)
        split_tokens = []
        for i, (word, pos) in enumerate(ptb_pos_tagged):
            if self.do_lower_case:
                word = word.lower()
            if universal_pos_tagged[i][1] in self.have_inflections and word not in (string.punctuation+'—') and pos not in self.lemma_tags:
                # (universal_)pos_tagged in the form of [(word, pos),(word, pos),...]
                # getLemma returns a tuple (lemma,)
                lemma = getLemma(word, upos=universal_pos_tagged[i][1])[0]
                if not lemma:
                    lemma = word
                wordpieced = self.wordpiece_tokenizer.tokenize(lemma)
                #print(wordpieced)
                split_tokens.extend(wordpieced)
            else:
                wordpieced = self.wordpiece_tokenizer.tokenize(word)
                split_tokens.extend(wordpieced)
        return split_tokens

    def convert_tokens_to_string(self, tokens):
        result = []
        for i, token in enumerate(tokens):
            # combine wordpiece tokens
            if len(token) > 2 and token[:2] == '##':
                if result:
                    result[-1] += token[2:]
                else:
                    result.append(token[2:])
                continue
            if token in self.inflection_tokens:
                if i != 0:
                    inflected = getInflection(result[-1], tag=token[1:-1])
                    if inflected:
                        result[-1] = inflected[0]
            else:
                result.append(token)
        return ' '.join(result)


class AblBiteWordpieceTokenizer(BertTokenizer):
    def __init__(self, vocab_file, do_lower_case=True, never_split=None,
                 additional_special_tokens=["[JJR]", "[JJS]", "[NNS]", "[NNP]", "[NNPS]", "[RBR]",
                                  "[RBS]", "[VBD]", "[VBG]", "[VBN]", "[VBP]", "[VBZ]"], **kwargs):
        self.inflection_tokens = additional_special_tokens
        self.tagger = PerceptronTagger()
        super().__init__(vocab_file, do_lower_case=do_lower_case, never_split=never_split, additional_special_tokens=additional_special_tokens, **kwargs)

        self.have_inflections = {'NOUN', 'ADJ', 'VERB'}
        self.lemma_tags = {'NN', 'VB', 'JJ', 'RB', 'MD', "NNP"}
        self.do_lower_case = do_lower_case
        if do_lower_case:
            self.cased_tokenizer = BasicTokenizer(do_lower_case=False, never_split=never_split)
        else:
            self.cased_tokenizer = self.basic_tokenizer

    def _tokenize(self, text):
        tokenized = self.cased_tokenizer.tokenize(text, never_split=self.all_special_tokens)
        #print(tokenized)
        ptb_pos_tagged = self.tagger.tag(tokenized)
        #print(pos_tagged)
        #print(pos_tagged)
        universal_pos_tagged = [(token, map_tag("en-ptb", 'universal', tag))
                                for (token, tag) in ptb_pos_tagged]
        #print(universal_pos_tagged)
        split_tokens = []
        for i, (word, pos) in enumerate(ptb_pos_tagged):
            if self.do_lower_case:
                word = word.lower()
            if universal_pos_tagged[i][1] in self.have_inflections and word not in (string.punctuation+'—') and pos not in self.lemma_tags:
                # (universal_)pos_tagged in the form of [(word, pos),(word, pos),...]
                # getLemma returns a tuple (lemma,)
                lemma = getLemma(word, upos=universal_pos_tagged[i][1])[0]
                if not lemma:
                    lemma = word
                wordpieced = self.wordpiece_tokenizer.tokenize(lemma)
                #print(wordpieced)
                split_tokens.extend(wordpieced)
                split_tokens.append('[unused1]')
            else:
                wordpieced = self.wordpiece_tokenizer.tokenize(word)
                split_tokens.extend(wordpieced)
        return split_tokens

    def convert_tokens_to_string(self, tokens):
        result = []
        for i, token in enumerate(tokens):
            # combine wordpiece tokens
            if len(token) > 2 and token[:2] == '##':
                if result:
                    result[-1] += token[2:]
                else:
                    result.append(token[2:])
                continue
            if token in self.inflection_tokens:
                if i != 0:
                    inflected = getInflection(result[-1], tag=token[1:-1])
                    if inflected:
                        result[-1] = inflected[0]
            else:
                result.append(token)
        return ' '.join(result)
