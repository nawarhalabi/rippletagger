# -*- coding: utf-8 -*-

from rippletagger.tagger import Tagger

r = Tagger(language="fr")
print r.tag(u"Cette annonce a fait l' effet d' une véritable bombe .")

r = Tagger(language="sv")
print r.tag(u"Fördomen har alltid sin rot i vardagslivet")
