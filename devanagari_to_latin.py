import re
from tqdm import tqdm
import glob
import os
from config import BASE_PATH

path = BASE_PATH

conversiontable = {
    'ॐ' : 'oṁ',
    #'ऀ' : 'ṁ',
    'ऀ' : 'm',
    #'ँ' : 'ṃ',
    'ँ' : 'n',
    #'ं' : 'ṃ',
    'ं' : 'n',
    'ः' : 'ḥ',
    'अ' : 'a',
    #'आ' : 'ā',
    'आ' : 'aa',
    'इ' : 'i',
    #'ई' : 'ī',
    'ई' : 'ee',
    'उ' : 'u',
    #'ऊ' : 'ū',
    'ऊ' : 'oo',
    'ऋ' : 'r̥',
    'ॠ' : ' r̥̄',
    'ऌ' : 'l̥',
    'ॡ' : ' l̥̄',
    'ऍ' : 'ê',
    'ऎ' : 'e',
    'ए' : 'e',
    'ऐ' : 'ai',
    'ऑ' : 'ô',
    'ऒ' : 'o',
    'ओ' : 'o',
    'औ' : 'au',
    #'ा' : 'ā',
    'ा' : 'aa',
    'ि' : 'i',
    #'ी' : 'ī',
    'ी' : 'ee',
    'ु' : 'u',
    #'ू' : 'ū',
    'ू' : 'oo',
    'ृ' : 'r̥',
    'ॄ' : ' r̥̄',
    'ॢ' : 'l̥',
    'ॣ' : ' l̥̄',
    'ॅ' : 'ê',
    'े' : 'e',
    'ै' : 'ai',
    'ॉ' : 'ô',
    'ो' : 'o',
    'ौ' : 'au',
    'क़' : 'q',
    'क' : 'k',
    'ख़' : 'x',
    'ख' : 'kh',
    'ग़' : 'ġ',
    'ग' : 'g',
    'ॻ' : 'g',
    'घ' : 'gh',
    'ङ' : 'ṅ',
    #'च' : 'c',
    'च' : 'ch',
    #'छ' : 'ch',
    'छ' : 'chh',
    'ज़' : 'z',
    'ज' : 'j',
    'ॼ' : 'j',
    'झ' : 'jh',
    'ञ' : 'ñ',
    #'ट' : 'ṭ',
    'ट' : 't',
    #'ठ' : 'ṭh',
    'ठ' : 'th',
    #'ड़' : 'ṛ',
    'ड़' : 'd',
    #'ड' : 'ḍ',
    'ड' : 'd',
    'ॸ' : 'ḍ',
    'ॾ' : 'd',
    #'ढ़' : 'ṛh',
    'ढ़' : 'rh',
    #'ढ' : 'ḍh',
    'ढ' : 'dh',
    #'ण' : 'ṇ',
    'ण' : 'n',
    'त' : 't',
    'थ' : 'th',
    'द' : 'd',
    'ध' : 'dh',
    'न' : 'n',
    'प' : 'p',
    'फ़' : 'f',
    'फ' : 'ph',
    'ब' : 'b',
    'ॿ' : 'b',
    'भ' : 'bh',
    'म' : 'm',
    'य' : 'y',
    'र' : 'r',
    'ल' : 'l',
    'ळ' : 'ḷ',
    'व' : 'v',
    #'श' : 'ś',
    'श' : 'sh',
    #'ष' : 'ṣ',
    'ष' : 'sh',
    'स' : 's',
    'ह' : 'h',
    'ऽ' : '\'',
    '्' : '',
    '़' : '',
    '०' : '0',
    '१' : '1',
    '२' : '2',
    '३' : '3',
    '४' : '4',
    '५' : '5',
    '६' : '6',
    '७' : '7',
    '८' : '8',
    '९' : '9',
    #'ꣳ' : 'ṁ',
    'ꣳ' : 'n',
    '।' : '.',
    '॥' : '..',
    ' ' : ' ',
    }

consonants = '\u0915-\u0939\u0958-\u095F\u0978-\u097C\u097E-\u097F'
vowelsigns = '\u093E-\u094C\u093A-\u093B\u094E-\u094F\u0955-\u0957'
nukta = '\u093C'
virama = '\u094D'

devanagarichars = '\u0900-\u097F\u1CD0-\u1CFF\uA8E0-\uA8FF'


def deva_to_latn(text):

    word = text.strip()

    # define a buffer to store the transliteration
    curr = ''

    for index, char in enumerate(word):

        # check if char is a Devanagari character. if true then continue processing.
        # otherwise, output char to curr

        if re.match('[' + devanagarichars + ']', char):

            # if char = consonant, then its transliteration is dependent upon various
            # factors. need to check if next char = nukta, virama, vowel sign.

            if re.match('[' + consonants + ']', char):

                # check next char
                nextchar = word[(index + 1) % len(word)]

                if nextchar:

                    # if next char = nukta, then add present char and nukta 
                    # to 'cons'. else just add present char. set variable
                    # to test for nukta when processing next char

                    if re.match('[' + nukta + ']', nextchar):
                        cons = char + nextchar
                        nukta_present = 1
                    else:
                        cons = char
                        nukta_present = 0

                    # if present char is nukta, then check next char

                    if nukta_present:
                        nextchar = word[(index + 2) % len(word)]

                    # if next char = combining sign or virama, convert consonant 
                    # without "a". else if next char != combining sign or virama, 
                    # add "a" to consonant

                    if re.match('[' + vowelsigns + virama +']', nextchar):
                        trans = conversiontable.get(cons, '')
                        curr = curr + trans
                    else:
                        trans = conversiontable.get(cons, '')
                        trans = trans + "a"
                        curr = curr + trans

            # transliterate all other chars

            else:
                trans = conversiontable.get(char, '')
                curr = curr + trans

        # char is not Devanagari. output char to curr

        else:
             curr = curr + char

    return curr

def get_latin(inputtext):

    word_syllables = []
    all_words = []

    try:
        for word in inputtext.split():

            latin_output = deva_to_latn(word)
            all_words.append(latin_output)
            joined_all_words = ' '.join(all_words)

        return joined_all_words
    except:
        # print('Couldn\'t split')
        return ''
