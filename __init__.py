#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, unicodedata, settings
from django.template.defaultfilters import slugify as django_slugify
import logging

logger = logging.getLogger("slugifornication")

stopwords = {
   "de": [
       u"aber",u"als",u"am",u"an",u"auch",u"auf",u"aus",u"bei",u"bin",u"bis",u"ist",u"da",u"dadurch",u"daher",
       u"darum",u"das",u"dass",u"dein",u"deine",u"dem",u"den",u"der",u"des",u"dessen",u"deshalb",u"die",u"dies",
       u"dieser",u"dieses",u"doch",u"dort",u"du",u"durch",u"ein",u"eine",u"einem",u"einen",u"einer",u"eines",u"er",
       u"es",u"euer",u"eure",u"für",u"hatte",u"hatten",u"hattest",u"hattet",u"hier",u"hinter",u"ich",u"ihr",u"ihre",
       u"im",u"in",u"ist",u"ja",u"jede",u"jedem",u"jeden",u"jeder",u"jedes",u"jener",u"jenes",u"jetzt",u"kann",
       u"kannst",u"können",u"könnt",u"machen",u"mal",u"mein",u"meine",u"mit",u"muss",u"mußt",u"musst",u"müssen",
       u"müsst",u"nach",u"nachdem",u"nein",u"nicht",u"nun",u"oder",u"seid",u"sein",u"seine",u"sich",u"sie",u"sind",
       u"soll",u"sollen",u"sollst",u"sollt",u"sonst",u"soweit",u"sowie",u"und",u"unser",u"unsere",u"unter",u"vom",
       u"von",u"vor",u"wann",u"warum",u"was",u"weiter",u"weitere",u"wenn",u"wer",u"werde",u"werden",u"werdet",
       u"weshalb",u"wie",u"wieder",u"wieso",u"wir",u"wird",u"wirst",u"wo",u"woher",u"wohin",u"zu",u"zum",u"zur",u"über",
    ],
   "en": [
       u"a",u"about",u"above",u"after",u"again",u"against",u"all",u"am",u"an",u"and",u"any",u"are",u"aren't",u"as",
       u"at",u"be",u"because",u"been",u"before",u"being",u"below",u"between",u"both",u"but",u"by",u"can't",u"cannot",
       u"could",u"couldn't",u"did",u"didn't",u"do",u"does",u"doesn't",u"doing",u"don't",u"down",u"during",u"each",
       u"few",u"for",u"from",u"further",u"had",u"hadn't",u"has",u"hasn't",u"have",u"haven't",u"having",u"he",u"he'd",
       u"he'll",u"he's",u"her",u"here",u"here's",u"hers",u"herself",u"him",u"himself",u"his",u"how",u"how's",u"i",
       u"i'd",u"i'll",u"i'm",u"i've",u"if",u"in",u"into",u"is",u"isn't",u"it",u"it's",u"its",u"itself",u"let's",u"me",
       u"more",u"most",u"mustn't",u"my",u"myself",u"no",u"nor",u"not",u"of",u"off",u"on",u"once",u"only",u"or",u"other",
       u"ought",u"our",u"ours",u"	 ourselves",u"out",u"over",u"own",u"same",u"shan't",u"she",u"she'd",u"she'll",
       u"she's",u"should",u"shouldn't",u"so",u"some",u"such",u"than",u"that",u"that's",u"the",u"their",u"theirs",
       u"them",u"themselves",u"then",u"there",u"there's",u"these",u"they",u"they'd",u"they'll",u"they're",u"they've",
       u"this",u"those",u"through",u"to",u"too",u"under",u"until",u"up",u"very",u"was",u"wasn't",u"we",u"we'd",u"we'll",
       u"we're",u"we've",u"were",u"weren't",u"what",u"what's",u"when",u"when's",u"where",u"where's",u"which",u"while",
       u"who",u"who's",u"whom",u"why",u"why's",u"with",u"won't",u"would",u"wouldn't",u"you",u"you'd",u"you'll",
       u"you're",u"you've",u"your",u"yours",u"yourself",u"yourselves",
    ]
}

umlauts = {
    u'ä': 'ae', u'ö':'oe', u'ü': 'ue', u'ß': 'ss',
}


def better_slugify(value, remove_stopwords=True, slugify=True, max_words=None):
    """
    Better slugify

    Enhancement of Django's own slugify function. Retains readability by replaceing Umlaut characters
    with standard ascii chars, shortens length, removes stopwords

    Arguments:
        value - string - The String to slugify
        remove_stopwords - boolean - Remove frequently used words. For a list see stopwords Dict
        slugify - boolean - Call Django's slugify function afterwards?
        max_words - int - Number of words that are allowed. Longer strings will be shortened
    """

    lang = settings.LANGUAGE_CODE.lower()

    logger.debug("Slugifying %s, language %s" % (value, lang))

    # remove stopwords
    if remove_stopwords and lang in stopwords:
        words = value.split()
        value = " ".join([ w for w in words if w not in stopwords[lang] ])

    # reduce to max_words
    if not max_words is None:
        value = " ".join(value.split()[:max_words])
        
    # replace umlauts
    for umlaut, replacement in umlauts.iteritems():
        value = unicode(value.replace(umlaut, replacement))

    # and slugify
    if slugify:
        value = django_slugify(value)

    logger.debug("Slugified: %s" % value)        

    return value
    