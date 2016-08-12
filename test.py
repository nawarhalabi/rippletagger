# -*- coding: utf-8 -*-

from rippletagger.tagger import Tagger

r = Tagger("French")
print r.tag(u"Cette annonce a fait l' effet d' une véritable bombe .")

r = Tagger("Swedish")
print r.tag(u"Fördomen har alltid sin rot i vardagslivet")
