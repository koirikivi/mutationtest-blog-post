Mutaatiotestaus
===============

[Mutaatiotestaus][1] (eng. mutation testing) on tapa testata koodia varten
kehitettyjä testejä. Idea on yksinkertainen: Luodaan testattavasta ohjelmasta
virheellisiä versioita ("mutantteja") ja ajetaan ne testien läpi. Jos testit
menevät läpi, niissä on puutteita.

Otetaan parempaa selitystä varten tarkasteluun seuraava funktio, jonka tarkitus
on palauttaa kahdesta luvusta isompi...

    def bigger_number(x, y):
        if x > y:
            return x
        elif x < y:
            return y

...ja sille seuraavat testit.

    class BiggerNumberTests(unittest.TestCase):
        def test_2_is_bigger_than_1(self):
            assert bigger_number(2, 1) == 2

        def test_1_is_smaller_than_2(self):
            assert bigger_number(1, 2) == 2

Testit menevät läpi:

    $ python -m unittest tests.py
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.008s

Voidaanko tällä perusteella sanoa, että testattava koodi toimii oikein?
Kysymykseen on tietysti mahdoton vastata täysin varmasti, mutta hyvä indikaatio
ohjelman toimivuudesta on sen testikattavuus. Edellisen koodinpätkän testit
kuitenkin suorittavat sen jokaisen rivin, joten ohjelmalla on täysi
testikattavuus\*:

    $ coverage run -m unittest tests.py && coverage report -m | grep testprogram
    testprogram       5      0   100%

Mutaatiotestaus on toinen tapa testata ohjelman testien kattavuutta.
Mutaatiotestausta varten ohjelmasta voitaisiin luoda vaikkapa seuraavanlaisia
versioita:

Mutantti 1:

    def bigger_number(x, y):
        if x > y:
            return x + 1
        elif x < y:
            return y

Mutantti 2:

    def bigger_number(x, y):
        if x >= y:
            return x
        elif x < y:
            return y

Mutanttiohjelmien tarkoituksena on poiketa normaalista ohjelmasta vain hieman,
jotta ne kuvastaisivat yleisiä ohjelmoijien tekemiä virheitä.

Seuraava vaihe mutaatiotestausprosessissa on ajaa nämä (virheelliset?)
ohjelmaversiot testien läpi. Ensimmäinen mutantti saa testit epäonnistumaan,
(bigger\_number(2, 1) != 2) joten sen osalta testit ovat tarpeeksi kattavia.
Toinen mutantti kuitenkin pääsee testien läpi! Ohjelman testien kannalta
tilanteilla x > y ja x >= y (ja täten x == y) ei siis ole eroa.  Tämä antaa
meille vihjeen tutkia tapausta, jossa x == y, esimerkiksi seuraavan testin
avulla:

     def test_1_and_1_are_equal(self):
         assert bigger_number(1, 1) == 1

Kun tämä testi lisätään, eivät testit enää mene läpi alkuperäisen ohjelman
osalta:

    $ python -m unittest tests.py
    F..
    ======================================================================
    FAIL: test_1_and_1_are_equal (tests.BiggerNumberTests)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "./tests.py", line 12, in test_1_and_1_are_equal
        assert bigger_number(1, 1) == 1
    AssertionError

Tämä johtuu siitä, että alkuperäisessä ohjelmassa tapaus x == y jätetään
kokonaan huomiotta. Korjataan asia muuttamalla ohjelma seuraavanlaiseksi:

    def bigger_number(x, y):
        if x > y:
            return x
        return y

Tämän jälkeen testit menevät taas mukavasti läpi.


Työkalut
--------

Koska ylläkuvattu prosessi vaatii aikaa ja vaivaa, ei sitä ole mitään järkeä
tehdä käsin, vaan prosessi hoidetaan työkaluilla. All prosessi suoritettuna
Python 3:lle kehitetyllä [mut.py][2]-työkalulla:

    $ mut.py --target=testprogram --unit-test=tests -m
    [*] Start mutation process:
       - targets: testprogram
       - tests: tests
    [*] 2 tests passed:
       - tests [0.00008 s]
    [*] Start mutants generation and execution:
    ... snip ...
     1: def bigger_number(x, y):
    ~2:     if x >= y:
     3:         return x
     4:     elif x < y:
     5:         return y
    --------------------------------------------------------------------------------
    [0.00472 s] survived
       - [#   5] ROR testprogram.py:4  : 
    --------------------------------------------------------------------------------
     1: def bigger_number(x, y):
     2:     if x > y:
     3:         return x
    ~4:     elif x > y:
     5:         return y
    --------------------------------------------------------------------------------
    [0.00540 s] killed by test_1_is_smaller_than_2 (tests.BiggerNumberTests)
       - [#   6] ROR testprogram.py:4  : 
    --------------------------------------------------------------------------------
     1: def bigger_number(x, y):
     2:     if x > y:
     3:         return x
    ~4:     elif x <= y:
     5:         return y
    --------------------------------------------------------------------------------
    [0.00546 s] survived
    [*] Mutation score [0.08555 s]: 66.7%
       - all: 6
       - killed: 4 (66.7%)
       - survived: 2 (33.3%)
       - incompetent: 0 (0.0%)
       - timeout: 0 (0.0%)

Työkalu automatisoi mutanttien luomisen ja testien ajamisen niitä vasten.
Kuten raportista näkee, työkalu loi yhteensä kuusi mutanttia, joista kaksi pääsi
testien läpi.

mut.py on omien kokemuksieni perusteella kattavin Pythonille kehitetty
mutaatiotestaustyökalu. Sen ainoa miinus on, että se toimii vain Python 3
-koodin kanssa, eikä siis ole käyttökelpoinen Python 2 -ohjelmien - joita suurin
osa Python-ohjelmista kuitenkin vielä on - kanssa. Pythonille on saatavilla myös
nose-testiajurin päällä toimiva [elcap][3], joka toimii myös Python 2.x
-ohjelmien kanssa, mutta on muuten paljon mut.py:tä suppeampi ja heikommin
dokumentoitu kokonaisuus.

Muiden kielien mutaatiotestaustyökaluista mainittakoon erityisesti Javan päällä
pyörivä [PIT][4], jota en ole vielä päässyt testaamaan, mutta joka ainakin
web-sivujen perusteella vaikuttaa erittäin lupaavalta. Kattavampaa listaa
työkaluista löytyy mm. [Wikipediasta][5].


Puutteet
--------

Mutaatiotestauksen suurimpia ongelmia on, että mutanttiohjelmien määrä paisuu
helposti käsistä. Jo edellä mainitulle neljän rivin ohjelmapahaselle generoitiin
mut.py:n toimesta kuusi mutanttia, joten on helppo kuvitella, minkälainen luku
olisi kyseessä 2000 rivin luokkahirviön kanssa. Kun otetaan vielä huomioon, että
jokaiselle generoitudulle ohjelmalle pitää ajaa läpi pahimmassa tapauksessa
*kaikki* ohjelman testit, paisuvat mutaatiotestausprosessin viemä aika ja
resurssit helposti tuskallisiin sfääreihin.

Tämän helpottamiseksi mutaatiotestaustyökaluissa on usein kikkailuasetuksia
prosessin nopeuttamiseksi. Yksi tekniikka on mutatoida vain ne rivit koodista,
jotka ovat myös rivikattavuuden alla, koska muiden rivien mutatointi
todennäköisesti joka tapauksessa saisi mutantin menemään testien läpi. Myös
muita heuristiikkoja voidaan käyttää prosessin nopeuttamiseksi.

Ehkä radikaalein tapa kontrolloida mutaatiotestausprosessin viemää aikaa on
kuitenkin vaihtaa koko prosessia *heikoksi mutaatiotestaukseksi* (weak mutation
testing). Heikossa mutaatiotestauksessa ajetaan mutatoitua ja alkuperäistä
koodia rinnakkain ja verrataan ohjelman sisäistä tilaa testitulosten vertailun
sijaan. Mikään tutkimistani työkaluista ei tukenut heikkoa mutaatiotestausta.

Suuri ongelma on myös sen kanssa, että osa mutatoiduista ohjelmista oikeasti
toimii identtisesti oikean ohjelman kanssa, ja täten testien kuuluukin mennä
niiden osalta läpi. Otetaan esimerkiksi aiemmassa prosessissa vahvennettu
ohjelma:

    def bigger_number(x, y):
        if x > y:
            return x
        return y

Tästä ohjelmasta voidaan luoda seuraava mutantti, ja esim. mut.py luokin
sellaisen:

    def bigger_number(x, y):
        if x >= y:
            return x
        return y

Tämä mutantti on toiminnalisuudeltaan täysin sama alkuperäisen ohjelman kanssa,
joten se menee testien läpi ja täten myös mutaatiotestausprosessin läpi samoin
kuin logiikaltaan virheelliset mutantitkin menisivät. Tällöin esim mut.py:n
raportti näyttää samalta, kuin jos ohjelmasta puuttuisi (mutaatiotestauksen
mukaan) testejä.  Ongelma on kinkkinen, koska kahta ohjelmaa on hankala osoittaa
toiminnallisuudeltaan samanlaisiksi. Yksi mahdollisuus olisi poistaa
mutaatio-operaattori, joka muuttaa >-operaattorin >=-operaattoriksi, mutta
tällöin menetettäisiin myös paljon oikeita keissejä, jossa vastaava mutaatio
paljastaisi puutteelliset testit ja tällöin mahdollisesti virheellisen ohjelman.

Lyhyesti tulevaisuuden kehityksestä mutaatiotestauksen osalta täytyy sanoa sen
verran, että Python 2.x tarvitsisi robustin työkalun mutaatiotestausta varten
(vaikka elcap onkin ihan näppärä) ja että olisi hienoa nähdä työkaluja, joilla
heikko mutaatiotestaus onnistuisi tosimaailman sovelluksissa. Myös
ekvivalenttien mutanttien ongelman ratkaisu lienee tulevaisuudessa askarruttava
ongelma.


Käytännössä
-----------

Olen tutustunut mutaatiotestaukseen lähinnä akateemisesti kiinnostuneena.
Mutaatiotestaus vaikuttaa tekniikkana lupaavalta, mutta sen yhdistäminen
tosimaailman ohjelmistoprojekteihin ja testikehitykseen ei ole ihan
yksiselitteinen prosessi. Esimerkiksi omia [Django][6]-projektejani testaillessa
en ole vielä saanut hyödyllistä dataa mutaatiotestaustyökaluilla, ja
muutaman kerran prosessi on vienyt niin kauan aika, että prosessi on käytännössä
pitänyt sulkea.

Rehellisyyden nimissä en ole kuitenkaan myöskään käyttänyt yllä mainittuun
hirveänä aikaa, enkä ole aloittanut yhtään projektia mutaatiotestaus mielessä
tällaisen prosessin yrittämiseen. Esimerkiksi [Filip Van Laenen][7] antaa
mielenkiintoisen esimerkin mutaatiotestauksen käyttämisestä Test Driven
Development -prosessin vahvistamisessa.

TDD tai ei, mutaatiotestausta olisi hienoa kokeilla tosimaailman settingissä.
Meillä Arcusysillä käytetään ohjelmointikielinä paljon Javaa, Scalaa ja
Pythonia ja alustaratkaisuina mm. Djangoa ja Liferayta. Työkalut
mutaatiotestausta varten on saatavissa kielille, mutta alustojen sovellus voi
tuottaa haasteita. Tätä ei kuitenkaan näe, ennen kuin käytännössä kokeilee,
joten ehkäpä kuulemme aiheesta vielä enemmän vaikkapa tulevissa
blogipostauksissa... ;)


Referenssit / luettavaa
-----------------------

* [1]: http://en.wikipedia.org/wiki/Mutation_testing
* [2]: https://bitbucket.org/khalas/mutpy
* [3]: https://github.com/sk-/elcap
* [4]: http://pitest.org/
* [5]: http://en.wikipedia.org/wiki/Mutation_testing#External_links
* [6]: http://www.djangoproject.com/
* [7]: http://accu.org/var/uploads/journals/overload108.pdf
* A. P. Mathur, Foundations of Software Testing, Prentice Hall, 2008

Huomiot
-------

\*) Vaikka koodin rivikattavuus (line coverage) on 100%, ei sen haarakattavuus
(branch coverage) ole täydellinen, koska tilannetta, jossa kumpikaan if (elif)
-lauseista ei toteudu ei testata. Tässä tapauksessa haarakattavuusasetuksen
käyttäminen coverage-työkalussa (coverage run --branch) löytäisi myös puuttuvan
testin. Näin ei kuitenkaan ole aina.
