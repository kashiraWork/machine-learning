from unicodedata import normalize
import string
import MeCab
import pysnooper

#
# テキスト前処理クラス
#
class TextPreprocessing(object):
    def __init__(self):
        self.mecab = MeCab.Tagger('/usr/local/lib/mecab/dic/mecab-ipadic-neologd/')

    def _del_stop_words(self, words, stop_words):
        for word in words:
            if word in stop_words:
                words.remove(word)

        return words

    def _wakati(self, text):
        morphs = []
        self.mecab.parse('')
        node = self.mecab.parseToNode(text)
        while node:
            meta = node.feature.split(',')
            if meta[0] == '名詞':
                morphs.append(node.surface)
            node = node.next

        return morphs

    #@pysnooper.snoop()
    def preprocess(self, text, stop_words=[]):
        text = normalize('NFKC', text).lower()
        text_cs = ''
        for c in text:
            if c in normalize('NFKC', string.punctuation):
                c = ''
            text_cs += c

        text_cs_wakati = self._wakati(text_cs)

        return ' '.join(self._del_stop_words(text_cs_wakati, stop_words))
