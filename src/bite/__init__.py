from .base_inflect import BITETokenizer
from .bite_wordpiece import BiteWordpieceTokenizer, LemmaWordpieceTokenizer, AblBiteWordpieceTokenizer

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
