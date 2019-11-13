#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# ESTE PEDAZO CONTROLA LA SALIDA UTF-8 Y LA AYUDA
import argparse
parser = argparse.ArgumentParser(description=u'NLTK Básico en español')
parser.add_argument("-u", "--utf8", help=u"Codificar la salida como UTF-8.", action="store_true")
args = parser.parse_args()
import codecs,locale,sys
if args.utf8:
    sys.stdout = codecs.getwriter("utf8")(sys.stdout)
else:
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
######################################################
# Función de ayuda de impresión (no le hagan caso)
def addslashes(s):
    ech = [
        ("\r","\\r"),
        ("\n","\\n"),
        ("\t","\\t"),
    ]
    for e in ech:
        if e[0] in s:
            s = s.replace(e[0], e[1])
    return s
##############################################################
# Ahora sigamos un ejemplo similar al que se muestra la página
# de NLTK (nltk.org) pero "traducido" al español.
##############################################################
# "Tokenizar" y "taggear" un texto:
# nltk.download("maxent_ne_chunker")
# Siempre que definamos una cadena en código lo haremos con el prefijo (u)
cadena = u"—¡Joven «emponzoñado» con el whisky, qué fin… te aguarda exhibir!\nEl veloz murciélago hindú comía feliz cardillo y kiwi.\nLa cigüena tocaba el saxofón detrás del palenque de paja.\nEl pingüino Wenceslao hizo kilómetros bajo exhaustiva lluvia y frío, añoraba a su querido cachorro.\nExhíbanse politiquillos zafios,\ncon orejas kilométricas\n\ty unas de gavilán."

print u"Cadena:"
print "\t",cadena

# Ejemplo normal de tokenizador por palabras (las palabras se capturan con los signos de puntuación adyacentes)
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
tokens = tokenizer.tokenize(cadena)
print u"\nPalabras:"
print "\t","\n\t".join([addslashes(t) for t in tokens])

# Tokenizador que separa las palabras y luego los signos de puntuación
from nltk.tokenize import WordPunctTokenizer
word_punct_tokenizer = WordPunctTokenizer()
palabras = word_punct_tokenizer.tokenize(cadena)
print u"\nPalabras/Puntuación:"
print "\t","\n\t".join([addslashes(t) for t in palabras])

# Versión en español del tokenizador por frases
import nltk.data
spanish_tokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle")
frases = spanish_tokenizer.tokenize(cadena)
print u"\nFrases:"
print "\t","\n\t".join([addslashes(t) for t in frases])
