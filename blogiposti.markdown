Mutaatiotestaus
===============

[Mutaatiotestaus][1] (eng. mutation testing) on tapa testata koodia varten
kehitettyjä testejä. Idea on yksinkertainen: Luodaan testattavasta ohjelmasta
virheellisiä versioita ("mutantteja") ja ajetaan ne testien läpi. Jos testit
menevät läpi, niissä on puutteita.

Otetaan parempaa selitystä varten tarkasteluun seuraava - tarkoituksella
yksinkertaistettu - koodinpätkä...

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

    $ nosetests
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.008s

Voidaanko tällä perusteella sanoa, että testattava koodi toimii oikein?
Kysymykseen on tietysti useimmissa tapauksissa mahdoton vastata,

***

Implementaatiot
    Python
    Java
    Djangon yms testaus


[1]: http://en.wikipedia.org/wiki/Mutation_testing

http://en.wikipedia.org/wiki/Code_coverage

A. P. Mathur, Foundations of Software Testing, Prentice Hall, 2008

http://accu.org/var/uploads/journals/overload108.pdf
