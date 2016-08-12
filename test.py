# -*- coding: utf-8 -*-

from rippletagger.tagger import Tagger

r = Tagger(language="fr")
assert (
    r.tag(u"Cette annonce a fait l' effet d' une véritable bombe .") ==
    [
        (u'Cette', 'DET'),
        (u'annonce', 'NOUN'),
        (u'a', 'AUX'),
        (u'fait', 'VERB'),
        (u"l'", 'DET'),
        (u'effet', 'NOUN'),
        (u"d'", 'ADP'),
        (u'une', 'DET'),
        (u'véritable', 'ADJ'),
        (u'bombe', 'NOUN'),
        (u'.', 'PUNCT')
    ]
)

r = Tagger(language="sv")
assert (
    r.tag(u"Fördomen har alltid sin rot i vardagslivet") ==
    [
        (u'Fördomen', 'NOUN'),
        (u'har', 'AUX'),
        (u'alltid', 'ADV'),
        (u'sin', 'PRON'),
        (u'rot', 'NOUN'),
        (u'i', 'ADP'),
        (u'vardagslivet', 'NOUN')
    ]
)
