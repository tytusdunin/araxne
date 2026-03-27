from kokosznicka import Kokosznicka
import re
import regex
import unicodedata

# Hipotezy badawcze:
# 1. Samogłoska stanowi 40% rymowalności sylaby
# 2. Wygłos jest równie ważny dla integralności rymu, co nagłos
# 3. Zwartość i szczelinowość są zjawiskami równoważnymi
# 4. Głębokość samogłoski jest zjawiskiem stopniowalnym, wysokość zaś – binarnym
# 5. Artykulacje drżąca, nosowa i boczna są bardziej zbliżone do siebie niż inne sposoby artykulacji
# 6. Brak wygłosu lub nagłosu w porówaniu z obecnym nagłosem/wygłosem uznawany jest za zerowe podobieństwo tej części
# 7. Wysokość jest najważniejsza jakością samogłoski, rozkład wszystkich trzech to 3:1:1

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
        "miękkość": False,
    },
    "l": {
        "głębokość": 4,
        "artykulacja": ["boczna"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "ł": {
        "głębokość": 6,
        "artykulacja": ["półsamogłoskowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": False,
    },
    "j": {
        "głębokość": 5,
        "artykulacja": ["półsamogłoskowa"],
        "dźwięczność": True,
        "nosowość": False,
        "miękkość": True,
    },

}

# Pomocne rzeczy z Metrificale
file_path = 'proparoksytona2.txt'
proparoksytona = set(line.strip() for line in open(file_path, 'r', encoding='utf-8'))

oksytona_path = 'oksytona.txt'
oksytona = set(line.strip() for line in open(oksytona_path, 'r', encoding='utf-8'))

false_path = 'false-friends.txt'
false_friends = set(line.strip() for line in open(false_path, 'r', encoding='utf-8'))

proproparoksytona = {'libyśmy', 'libyście', 'łybyśmy' 'łybyście'}

def weighted_average(nums, weights):
            return sum(x * y for x, y in zip(nums, weights)) / sum(weights)

def sprawdz_koniec(slowo, koncowka):
    return slowo.endswith(koncowka)

class Araxne:
    def __init__(self, version):
        self.version = "v1.0"
    
    def compare(str1, str2):
        # Najpierw ustalamy, ile sylab musimy sprawdzić – wybieramy liczbę sylab najmniejszą z obu stringów
        steps = min((Kokosznicka.syllablecount(str1)), (Kokosznicka.syllablecount(str2)))

        # Funkcja na później, naprawia problem wielu liter w wygłosie/nagłosie
        def fix_multiletter(mystring):

            głębokość_l = []
            artykulacja = []
            dźwięczność = False
            nosowość = False
            miękkość = False

            grafemy = regex.findall(r'\X', mystring)

            for l in grafemy:
                entry = spółgłoski[f"{l}"]
                głębokość_l.append(entry["głębokość"])
                artykulacja.extend(entry["artykulacja"])
                artykulacja = list(set(artykulacja))
                if entry["dźwięczność"] == True:
                    dźwięczność = True
                if entry["nosowość"] == True:
                    nosowość = True
                if entry["miękkość"] == True:
                    miękkość = True
            
            mix = {
                "głębokość" : (sum(głębokość_l) // len(głębokość_l)),
                "artykulacja" : artykulacja,
                "dźwięczność" : dźwięczność,
                "nosowość" : nosowość,
                "miękkość" : miękkość,
            }


            return mix

        # Dzielimy tekst na sylaby, normalizujemy go fonetycznie i zwracamy listę sylab
        def preprocess(string):
            initial_word = string
            string = Kokosznicka.normalize(Kokosznicka.hyphenate(string))
            string = string.lower()
            string = string.replace("ż", "ž")
            string = string.replace("ć", "ĉ")
            string = string.replace("ź", "ẑ")
            string = string.replace("ś", "ŝ")
            string = string.replace("h", "ĥ")
            string = string.replace("ń", "ň")
            string = string.replace("ĵ", "") #POMYSŁ: można też wykorzystać do zmiękczania samogłosek
            #string = string.replace("ł", "") #POMYSŁ: trzeba to jakoś zagospodarować
            #string = string.replace("j", "") #POMYSŁ: trzeba to jakoś zagospodarować
            # Pamiętać o literach ścieśnionych
            string = string.replace(" ", "-").split("-")
            proparoksytoneza_koncowkowa = any(sprawdz_koniec(initial_word.lower(), koncowka) for koncowka in proparoksytona) and initial_word.lower() not in false_friends
            proproparoksytoneza_koncowkowa = any(sprawdz_koniec(initial_word.lower(), koncowka) for koncowka in proproparoksytona)
            # Ucinamy wszystko przed akcentem
            
            if proproparoksytoneza_koncowkowa:
                string = string[-4:]
            elif proparoksytoneza_koncowkowa or initial_word in proparoksytona:
                string = string[-3:]
            elif initial_word in oksytona:
                string = string[-1:]
            elif len(string) > 2:
                string = string[-2:]
            return string
        
        syls1 = preprocess(str1)
        syls2 = preprocess(str2)


        scorelist = []
        
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
                
                for i, elem in enumerate(lista_s1):
                    if i == 0 and elem not in samogł:
                        s_nagłosy.append(elem)
                    elif elem in samogł:
                        s_samogłoski.append(elem)
                    else:
                        s_wygłosy.append(elem)

                for i, elem in enumerate(lista_s2):
                    if i == 0 and elem not in samogł:
                        s_nagłosy.append(elem)
                    elif elem in samogł:
                        s_samogłoski.append(elem)
                    else:
                        s_wygłosy.append(elem)
                
                #print(f"{lista_s1} + {lista_s2}: {s_nagłosy}, {s_samogłoski}, {s_wygłosy}")

                # Teraz liczymy podobieństwo

                def compare_spółgłoski(l1, fullscore):
                    if len(l1) == 0:
                        return fullscore
                    elif len(l1) == 1:
                        return 0
                    elif l1[0] == l1[1]:
                        return fullscore
                    else:
                        #for lit in l1[0]:
                        increm = fullscore // 5
                        score = 0
                        if len(l1[0]) == 1:
                            entry = spółgłoski[f"{l1[0]}"]
                        else:
                            entry = fix_multiletter(l1[0])

                        if len(l1[1]) == 1:
                            the_other = spółgłoski[f"{l1[1]}"]
                        else:
                            the_other = fix_multiletter(l1[1])

                        # Sprawdzamy głębokość
                        score += increm - abs(entry["głębokość"] - the_other["głębokość"])
                        if score <= 0:
                            score = 0
                        
                        # Sprrawdzamy dźwięczność
                        if entry["dźwięczność"] == the_other["dźwięczność"]:
                            score += increm

                        # Sprawdzamy nosowość
                        if entry["nosowość"] == the_other["nosowość"]:
                            score += increm
                        
                        # Sprawdzamy miękkość
                        if entry["miękkość"] == the_other["miękkość"]:
                            score += increm
                        
                        # Sprawdzamy artykulację
                        if entry["artykulacja"] == the_other["artykulacja"]:
                            score += increm
                        elif not set(entry["artykulacja"]).isdisjoint(the_other["artykulacja"]):
                            #penalty = len(set(entry["artykulacja"]).symmetric_difference(the_other["artykulacja"]))
                            #try:
                            #    score += (increm//penalty)
                            #except:
                            #    print(the_other["artykulacja"])
                            #    print(entry["artykulacja"])
                            score += (increm//2)
                        else:
                            score = 0

                        return score

                # Porównujemy samogłoski

                def compare_samogłoski(l1):
                    if l1[0] == l1[1]:
                        return 40
                    else:
                        score = 0
                        entry = samogłoski[f"{l1[0]}"]
                        the_other = samogłoski[f"{l1[1]}"]

                        # Sprawdzamy głębokość
                        score += 5 - (abs(entry["głębokość"] - the_other["głębokość"]))

                        # Sprawdzamy wysokość
                        if entry["wysokość"] == the_other["wysokość"]:
                            score += 10
                        
                        # Sprawdzamy nosowość
                        if entry["nosowość"] == the_other["nosowość"]:
                            score += 5

                        return score

                if len(s_nagłosy) != 0 and len(s_wygłosy) != 0:
                    s_finalscore = compare_spółgłoski(s_nagłosy, 30) + compare_samogłoski(s_samogłoski) + compare_spółgłoski(s_wygłosy, 30)
                elif len(s_nagłosy) != 0 and len(s_wygłosy) == 0:
                    s_finalscore = int(((compare_spółgłoski(s_nagłosy, 30) + compare_samogłoski(s_samogłoski)) / 70) * 100)
                elif len(s_nagłosy) == 0 and len(s_wygłosy) != 0:
                    s_finalscore = int(((compare_samogłoski(s_samogłoski) + compare_spółgłoski(s_wygłosy, 30)) / 70) * 100)
                else:
                    s_finalscore = int((compare_samogłoski(s_samogłoski) / 40) * 100)
                scorelist.append(s_finalscore)
                steps -= 1
        #print(scorelist)
        weightlist = [3]
        for l in scorelist:
            if len(weightlist) < len(scorelist):
                weightlist.append(1)
            elif len(weightlist) == len(scorelist):
                break
        
        #print(weightlist)
        
        result = weighted_average(scorelist, weightlist)
        return result

#str1 = "rozprawiał"
#str2 = "chował"

#print(Araxne.compare(str1, str2))

# sprawa : rawa zwraca 100
# ględzę : zrzędzę zwraca 93.5 (grupa : zupa tak samo)
# grupa : chmura zwraca 80
# masa : buka = 77.5, masa : buzka 77.0, maska : buzka 76.5