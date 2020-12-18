def osebe(obiski):
    return set([(x) for x,y  in obiski])

def aktivnosti(obiski):
    return set([y for x,y in obiski])

def udelezenci(aktivnosti, obiski):
    return {x for x,y in obiski if y == aktivnosti}


def po_aktivnostih(obiski):
    return {aktivnost: udelezenci(aktivnost, obiski) for oseba, aktivnost in obiski}

def skupine(obiski):
    return [udelezenci(aktivnost, obiski) for aktivnost in aktivnosti(obiski)]

def okuzeni(skupine, nosilci):
    rez = []
    for okuzen in nosilci:
        for ljudi in skupine:
            if okuzen in ljudi:
                for x in ljudi:
                    if x not in rez and x not in nosilci:
                      rez.append(x)
    return set(rez)





def zlati_prinasalec(skupine):
    vsi = set()
    for manj_skup in skupine:
        for ljudi in manj_skup:
            vsi.add(ljudi)

    slov = {oseba: len(okuzeni(skupine, {oseba})) for oseba in vsi}

    max = 0
    index = []
    for x in slov:
        if slov[x] > max:
            max = slov[x]
            index = [x]
        elif slov[x] == max:
            index.append(x)

    index.sort()

    return index[0]


def korakov_do_vseh(skupine, prvi):
    vsi = set()
    for manj_skup in skupine:
        for ljudi in manj_skup:
            vsi.add(ljudi)
    counter = 0
    okuzeni = set()
    temp = set()
    okuzeni.add(prvi)
    while okuzeni != vsi:
        okuzeni = okuzeni.union(temp)
        temp = set()
        for skup1 in skupine:
            for x in okuzeni:
                if x in skup1:
                    for mordaOkuzen in skup1:
                        if mordaOkuzen not in okuzeni:
                            temp.add(mordaOkuzen)
                    break
        counter += 1
        if counter > 10000:
            return None

    if counter != 0:
        return counter-1
    else:
        return None

"""
        skupine = [{"Cilka", "Ema", "Jana", "Saša"},
                   {"Ema"},
                   {"Fanči", "Greta", "Saša"},
                   {"Greta", "Nina"},
                   {"Greta", "Olga", "Rebeka"},
                   {"Micka", "Ana", "Klara"},
                   {"Fanči", "Iva", "Berta", "Špela"},
                   {"Klara", "Cilka", "Dani"},
                   {"Petra", "Dani", "Lara", "Špela"}]

"""


import unittest
import random
import ast


class TestObvezna(unittest.TestCase):
    ime = "".join(random.choice("qwertyuiop") for _ in range(10))
    aktivnost = "".join(random.choice("asdfghjkl") for _ in range(10))
    rnd_obiski = [(ime, aktivnost)]

    obiski = [("Ana", "kava"), ("Berta", "kava"), ("Cilka", "telovadba"),
              ("Dani", "zdravnik"), ("Ana", "zdravnik"), ("Cilka", "kava"),
              ("Ema", "telovadba")]

    def test_osebe(self):
        self.assertEqual({"Ana", "Berta", "Cilka", "Dani", "Ema"}, osebe(self.obiski))
        self.assertEqual({self.ime}, osebe(self.rnd_obiski))
        self.assertEqual(set(), osebe([]))

    def test_aktivnosti(self):
        self.assertEqual({"zdravnik", "kava", "telovadba"}, aktivnosti(self.obiski))
        self.assertEqual({self.aktivnost}, aktivnosti(self.rnd_obiski))
        self.assertEqual(set(), aktivnosti([]))

    def test_udelezenci(self):
        self.assertEqual({"Ana", "Berta", "Cilka"}, udelezenci("kava", self.obiski))
        self.assertEqual(set(), udelezenci("sprehod", self.obiski))
        self.assertEqual({self.ime}, udelezenci(self.aktivnost, self.rnd_obiski))
        self.assertEqual(set(), udelezenci(self.aktivnost, []))

    def test_po_aktivnostih(self):
        self.assertEqual({
            "kava": {"Ana", "Berta", "Cilka"},
            "zdravnik": {"Ana", "Dani"},
            "telovadba": {"Cilka", "Ema"}},
            po_aktivnostih(self.obiski))
        self.assertEqual({self.aktivnost: {self.ime}}, po_aktivnostih(self.rnd_obiski))

    def test_skupine(self):
        def form(s):
            return sorted(s, key=lambda x: "-".join(sorted(x)))

        self.assertEqual(
            form([{"Ana", "Berta", "Cilka"}, {"Dani", "Ana"}, {"Cilka", "Ema"}]),
            form(skupine(self.obiski)))

        self.assertEqual(
            form([{self.ime}]),
            form(skupine([(self.ime, self.aktivnost)])))

    def test_okuzeni(self):
        skupine = [{"Ana", "Berta", "Cilka"}, {"Dani", "Ana"}, {"Cilka", "Ema"}, {"Fanči"}]

        self.assertEqual({"Berta", "Cilka", "Dani"},
                         okuzeni(skupine, {"Ana"}))
        self.assertEqual({"Ana", "Berta", "Ema"},
                         okuzeni(skupine, {"Cilka"}))
        self.assertEqual({"Ana", "Cilka"},
                         okuzeni(skupine, {"Ema", "Dani"}))
        self.assertEqual({"Ana", "Ema"},
                         okuzeni(skupine, {"Cilka", "Berta"}))
        self.assertEqual({"Berta", "Cilka", "Dani"},
                         okuzeni(skupine, {"Ana", "Ema"}))
        self.assertEqual({"Cilka"},
                         okuzeni(skupine, {"Ema"}))
        self.assertEqual(set(),
                         okuzeni(skupine, {"Fanči"}))
        self.assertEqual(set(),
                         okuzeni(skupine, set()))
        self.assertEqual({self.ime},
                         okuzeni([{self.ime, self.aktivnost}], {self.aktivnost}))

    def test_zlati_prinasalec(self):
        self.assertEqual(
            "Ana",
            zlati_prinasalec([{"Ana", "Berta", "Cilka"}, {"Dani", "Ana"}, {"Cilka", "Ema"}, {"Cilka"}]))
        self.assertEqual(
            "Cilka",
            zlati_prinasalec([{"Fanči", "Berta", "Cilka"}, {"Dani", "Fanči"}, {"Cilka", "Ema"}, {"Cilka"}]))
        self.assertEqual(
            "Cilka",
            zlati_prinasalec([{"Fanči", "Berta", "Cilka"}, {"Dani", "Fanči"}, {"Cilka", "Ema"}, {"Fanči"}]))

    def test_korakov_do_vseh(self):
        skupine = [{"Cilka", "Ema", "Jana", "Saša"},
                   {"Ema"},
                   {"Fanči", "Greta", "Saša"},
                   {"Greta", "Nina"},
                   {"Greta", "Olga", "Rebeka"},
                   {"Micka", "Ana", "Klara"},
                   {"Fanči", "Iva", "Berta", "Špela"},
                   {"Klara", "Cilka", "Dani"},
                   {"Petra", "Dani", "Lara", "Špela"}]
        self.assertEqual(5, korakov_do_vseh(skupine, "Ana"))
        self.assertEqual(4, korakov_do_vseh(skupine, "Klara"))
        self.assertEqual(4, korakov_do_vseh(skupine, "Dani"))
        self.assertEqual(3, korakov_do_vseh(skupine, "Ema"))

        skupine.append({"Tina"})
        self.assertIsNone(korakov_do_vseh(skupine, "Ema"))
        self.assertIsNone(korakov_do_vseh(skupine, "Tina"))
        skupine[-1].add("Urša")
        skupine[-1].add("Vesna")
        skupine.append({"Zala", "Žana"})
        self.assertIsNone(korakov_do_vseh(skupine, "Ema"))
        self.assertIsNone(korakov_do_vseh(skupine, "Tina"))


class TestOneLineMixin:
    functions = {elm.name: elm
                 for elm in ast.parse(open(__file__, "r", encoding="utf-8").read()).body
                 if isinstance(elm, ast.FunctionDef)}

    def assert_is_one_line(self, func):
        func
        body = self.functions[func.__code__.co_name].body
        self.assertEqual(len(body), 1, "\nFunkcija ni dolga le eno vrstico")
        self.assertIsInstance(body[0], ast.Return, "\nFunkcija naj bi vsebovala le return")

    def test_nedovoljene_funkcije(self):
        dovoljene_funkcije = {
            "preberi_zapiske", "osebe", "aktivnosti", "udelezenci",
            "po_aktivnostih", "skupine", "okuzeni", "zlati_prinasalec",
            "korakov_do_vseh"}
        for func in self.functions:
            self.assertIn(func, dovoljene_funkcije, f"\nFunkcija {func} ni dovoljena.")


class TestDodatna(unittest.TestCase, TestOneLineMixin):
    def test_oneline(self):
        for func in (osebe, aktivnosti, udelezenci, po_aktivnostih, skupine):
            self.assert_is_one_line(func)


class TestIzziv(unittest.TestCase, TestOneLineMixin):
    def test_oneline(self):
        for func in (okuzeni, zlati_prinasalec):
            self.assert_is_one_line(func)


if __name__ == "__main__":
    unittest.main()