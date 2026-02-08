from kokosznicka import Kokosznicka
import re

# Hipotezy badawcze:
# 1. Samogłoska stanowi 50% rymowalności sylaby
# 2. Wygłos jest ważniejszy dla integralności rymu niż nagłos (zakładana proporcja – 3:2)
# 3. Zwartość i szczelinowość są zjawiskami równoważnymi
# 4. Głębokość samogłoski jest zjawiskiem stopniowalnym, wysokość zaś – binarnym
# 5. Artykulacje drżąca, nosowa i boczna są bardziej zbliżone do siebie niż inne sposoby artykulacji
# 6. Brak wygłosu lub nagłosu w porówaniu z obecnym nagłosem/wygłosem uznawany jest za zerowe podobieństwo tej części

samogł = "aeiouyóęąAEIOUYÓĘĄ"

wyniki = []

samogłoski = {
    # Głębokość przyporządkowana na podstawie prostokąta Bella-Sweeta zmodyfikowanego przez Tytusa Benniego
    "i": { #pamiętać o chwilowym
        "głębokość": 1,
        "wysokość": "wysoka",
        "nosowość": False,
    },
    "y": {
        "głębokość": 2,
        "wysokość": "wysoka",
        "nosowość": False,
    },
    "u": { #pamiętać o chwilowym
        "głębokość": 5,
        "wysokość": "wysoka",
        "nosowość": False,
    },
    "e": {
        "głębokość": 2,
        "wysokość": "średnia",
        "nosowość": False,
    },
    "o": {
        "głębokość": 4,
        "wysokość": "średnia",
        "nosowość": False,
    },
    "a": {
        "głębokość": 3,
        "wysokość": "niska",
        "nosowość": False,
    },
    "ó": {
        "głębokość": 5,
        "wysokość": "wysoka",
        "nosowość": False,
    },
    # Prawdziwe nosówki
    "ę": {
        "głębokość": 2,
        "wysokość": "średnia",
        "nosowość": True,
    },
    "ą": {
        "głębokość": 4,
        "wysokość": "średnia",
        "nosowość": True,
    },

}

spółgłoski = {
    # Głębokość spółgłoski wyraża pozycję w jednym z sześciu miejsc:
    # 1 - dwuwargowa
    # 2 - wargowo-zębowa
    # 3 - zębowa
    # 4 - dziąsłowa
    # 5 - środkowojęzykowa
    # 6 - tylnojęzykowa
    "b": {
        "głębokość": 1,
        "artykulacja": ["zwarta"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "p": {
        "głębokość": 1,
        "artykulacja": ["zwarta"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "d": {
        "głębokość": 3,
        "artykulacja": ["zwarta"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "t": {
        "głębokość": 3,
        "artykulacja": ["zwarta"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ĝ": {
        "głębokość": 5,
        "artykulacja": ["zwarta"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },
    "k̂": {
        "głębokość": 5,
        "artykulacja": ["zwarta"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": True,
    },
    "g": {
        "głębokość": 6,
        "artykulacja": ["zwarta"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "k": {
        "głębokość": 6,
        "artykulacja": ["zwarta"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ʒ": {
        "głębokość": 3,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "c": {
        "głębokość": 3,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ǯ": {
        "głębokość": 4,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "č": {
        "głębokość": 4,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ʒ́": {
        "głębokość": 5,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },
    "ĉ": { #pamiętać też o "ć"
        "głębokość": 4,
        "artykulacja": ["zwarta", "szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": True,
    },
    "w": {
        "głębokość": 2,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "f": {
        "głębokość": 2,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "z": {
        "głębokość": 3,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "s": {
        "głębokość": 3,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ž": { #pamiętać o "ż"
        "głębokość": 4,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "š": {
        "głębokość": 4,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "ẑ": { #pamiętać o "ź"
        "głębokość": 5,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },
    "ŝ": { #pamiętać o "ś"
        "głębokość": 5,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": True,
    },
    "ĥ": { #pamiętać o "h"
        "głębokość": 6,
        "artykulacja": ["szczelinowa"],
        "dźwięczność": False,
        "nosowość": False,
        "miękkość": False,
    },
    "m": {
        "głębokość": 1,
        "artykulacja": ["nosowa"],
        "dźwięczność": True,
        "nosowość": True,
        "miękkość": False,
    },
    "n": {
        "głębokość": 3,
        "artykulacja": ["nosowa"],
        "dźwięczność": True,
        "nosowość": True,
        "miękkość": False,
    },
    "ň": { #pamiętać o "ń"
        "głębokość": 5,
        "artykulacja": ["nosowa"],
        "dźwięczność": True,
        "nosowość": True,
        "miękkość": True,
    },
    "r": {
        "głębokość": 4,
        "artykulacja": ["drżąca"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },
    "l": {
        "głębokość": 4,
        "artykulacja": ["boczna"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },

}

class Araxne:
    def __init__(self, version):
        self.version = "v1.0"
    
    def compare(str1, str2):
        # Najpierw ustalamy, ile sylab musimy sprawdzić – wybieramy liczbę sylab najmniejszą z obu stringów
        steps = min((Kokosznicka.syllablecount(str1)), (Kokosznicka.syllablecount(str2))) 

        # Dzielimy tekst na sylaby, normalizujemy go fonetycznie i zwracamy listę sylab
        def preprocess(string):
            string = Kokosznicka.normalize(Kokosznicka.hyphenate(string))
            return string.replace(" ", "-").split("-")

        syls1 = preprocess(str1)
        syls2 = preprocess(str2)

        # Iterujemy przez obiekt zip stworzony z odwróconych list sylab
        for s1, s2 in zip(reversed(syls1), reversed(syls2)):
            if steps == 0:
                break 
            else:
                s_nagłosy = []
                s_samogłoski = []
                s_wygłosy = []

                # Oddzielamy samogłoskę, nagłos i wygłos
                pattern = f"([{samogł}])"

                s1 = re.sub(pattern, r"|\1|", s1)
                s1 = s1.strip("|")
                lista_s1 = s1.split("|")

                s2 = re.sub(pattern, r"|\1|", s2)
                s2 = s2.strip("|")
                lista_s2 = s2.split("|")
                
                for elem in lista_s1:
                    if elem == lista_s1[0] and elem not in samogł:
                        s_nagłosy.append(elem)
                    elif elem in samogł:
                        s_samogłoski.append(elem)
                    else:
                        s_wygłosy.append(elem)

                for elem in lista_s2:
                    if elem == lista_s2[0] and elem not in samogł:
                        s_nagłosy.append(elem)
                    elif elem in samogł:
                        s_samogłoski.append(elem)
                    else:
                        s_wygłosy.append(elem)
                
                print(f"{lista_s1} + {lista_s2}: {s_nagłosy}, {s_samogłoski}, {s_wygłosy}")

                steps -= 1
        result = 0
        return result

str1 = "przepowiednia"
str2 = "przejść do Wiednia"

Araxne.compare(str1, str2)