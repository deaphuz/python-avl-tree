import pickle
import sys
sys.setrecursionlimit(10000)
import csv

from os import system, name


def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac / linux
    else:
        _ = system('clear')

class AVLNode:
    parent = None
    left = None
    right = None
    key = None
    height = None

    def __init__(self, tree_data):
        self.parent = None
        self.key = tree_data
        self.left = None
        self.right = None
        self.height = 1

class PathNode:
    avlnode = None
    which_side_for_parent = None

    def __init__(self, node, side):
        self.avlnode = node
        self.which_side_for_parent = side


class AVLTree:
    root = None
    def __init__(self):
        self.root = None

    def get_height(self, pointer):
        if pointer == None:
            return 0
        return pointer.height

    def get_word(self, pointer):
        if pointer == None:
            return None
        return pointer.key[0]

    # DZIALA
    def insert(self, tree_data):
        if self.root == None:
            self.root = AVLNode(tree_data)
            return True

        return_path = []
        # etap 1 - wstawianie
        pointer = self.root
        while True:
            if tree_data[0] < pointer.key[0]:
                if pointer.left == None:
                    pointer.left = AVLNode(tree_data)
                    pointer.left.parent = pointer  # żeby było wiadomo gdzie wracać przy wyważaniu
                    pointer = pointer.left
                    break
                pointer = pointer.left

            elif tree_data[0] > pointer.key[0]:
                if pointer.right == None:
                    pointer.right = AVLNode(tree_data)
                    pointer.right.parent = pointer  # żeby było wiadomo gdzie wracać przy wyważaniu
                    pointer = pointer.right
                    break

                pointer = pointer.right
            else:
                # slowo w slowniku istnieje - suma zbiorow tlumaczen
                pointer.key[1] = pointer.key[1].union(tree_data[1])
                return True

        # etap 2 - sprawdzanie wywazenia
        while pointer != None:
            prev_node = pointer

            # aktualizacja sciezki powrotu
            if pointer != self.root:
                if pointer.parent.left == prev_node:
                    return_path.insert(0, PathNode(pointer, "L"))
                elif pointer.parent.right == prev_node:
                    return_path.insert(0, PathNode(pointer, "R"))
            else:
                if ( return_path[0].avlnode == self.root.left) and (self.root.left != None):
                    return_path.insert(0, PathNode(self.root, "L"))
                elif ( return_path[0].avlnode == self.root.right) and (self.root.right != None):
                    return_path.insert(0, PathNode(self.root, "R"))


            # zaburzenia wysokosci - ROTACJE
            if abs(self.get_height(pointer.right)-self.get_height(pointer.left)) > 1: # brak wywazenia
                if return_path[1].which_side_for_parent == "L" and return_path[2].which_side_for_parent == "L": # rotacja pojedyncza LL
                    self.rotate_l(pointer, pointer.left)

                elif return_path[1].which_side_for_parent == "L" and return_path[2].which_side_for_parent == "R": # rotacja podwojna LR
                    self.rotate_r(return_path[1].avlnode, return_path[2].avlnode)
                    self.rotate_l(return_path[0].avlnode, return_path[2].avlnode)

                elif return_path[1].which_side_for_parent == "R" and return_path[2].which_side_for_parent == "L": # rotacja podwojna RL
                    self.rotate_l(return_path[1].avlnode, return_path[2].avlnode)
                    self.rotate_r(return_path[0].avlnode, return_path[2].avlnode)

                elif return_path[1].which_side_for_parent == "R" and return_path[2].which_side_for_parent == "R": # rotacja pojedyncza RR
                    self.rotate_r(pointer, pointer.right)

                break # koniec wywazania

            # aktualizacje wysokosci
            new_height = 1 + pointer.height
            if pointer.parent != None:
                if new_height > pointer.parent.height:
                    pointer.parent.height = new_height

            # przejscie do rodzica
            pointer = pointer.parent

        return True


    # DZIALA
    def search(self, word):
        if self.root == None:
            return False
        pointer = self.root # pointer robi mi za pomocniczy wskaznik

        while pointer != None:
            if word < pointer.key[0]:
                pointer = pointer.left
            elif word > pointer.key[0]:
                pointer = pointer.right
            elif word == pointer.key[0]:
                return pointer
        return None

    def inorder(self, pointer):
        if pointer != None:
            self.inorder(pointer.left)
            print(pointer)
            self.inorder(pointer.right)

    def search_for_node_pred(self, cur): # metoda pomocnicza dla metody delete
        while not ( cur.right == None):
            cur = cur.right
        return cur

    # DZIALA
    def delete(self, word):
        if self.root == None:
            return False
        pointer = self.root # pointer robi mi za pomocniczy wskaznik

        deleted = 0
        ancestor = None
        return_path = []
        while pointer != None:
            if word < pointer.key[0]:
                pointer = pointer.left
            elif word > pointer.key[0]:
                pointer = pointer.right
            elif word == pointer.key[0]:
                # przodek
                ancestor = pointer.parent
                # give rodzica

                # if word == pointer.parent.left.key:
                #    pointer_parent = pointer.parent.left
                # elif word == pointer.parent.right.key:
                #    pointer_parent = pointer.parent.right

                # znaleziono element do usuniecia
                # 1) brak dzieci
                if pointer.left == None and pointer.right == None:
                    if word == self.get_word(pointer.parent.left):
                        return_path.insert(0, PathNode(None, "L"))
                        pointer.parent.left = None # rodzic traci dzieciaka
                    elif word == self.get_word(pointer.parent.right):
                        return_path.insert(0, PathNode(None, "R"))
                        pointer.parent.right = None # rodzic traci dzieciaka
                    # pointer = None --- i tak zgubilismy referencje
                    deleted = 1
                    break

                # 2) tylko jedno dziecko istnieje
                elif (pointer.left != None and pointer.right == None) or (pointer.left == None and pointer.right != None):
                    if pointer.left != None:
                        return_path.insert(0, PathNode(None, "L"))
                        pointer.parent.left = pointer.left # usuwamy wezel a jego dziecko staje sie dzieckiem rodzica
                    else:
                        return_path.insert(0, PathNode(None, "R"))
                        pointer.parent.right = pointer.right # usuwamy wezel a jego dziecko staje sie dzieckiem rodzica
                    # pointer = None --- i tak zgubilismy referencje
                    deleted = 1
                    break

                # 3) istnieja oba dzieciaki
                elif pointer.left != None and pointer.right != None:
                    helper = self.search_for_node_pred(pointer.left)
                    return_path.insert(0, PathNode(None, "L"))
                    pointer.key = helper.key
                    # kopiuje tylko klucz aby nie przestawiac wskaznikow nadmiarowo

                    # USUWANIE POPRZEDNIK
                    #
                    # jesli poprzednik ma poddrzewo to jest ono podpinane pod rodzica tego poprzednika
                    if helper.left != None:
                        helper.parent.right = helper.left
                    deleted = 1
                    break
        if deleted == 0:
            return False # nie ma takiego wezla do usuniecia
        # etap 2 - sprawdzanie wywazenia


        #ustawienie przodka usuwanego węzła
        pointer = ancestor


        while pointer != None:
            prev_node = pointer

            # aktualizacja sciezki powrotu
            if pointer != self.root:
                if pointer.parent.left == prev_node:
                    return_path.insert(0, PathNode(pointer, "L"))
                elif pointer.parent.right == prev_node:
                    return_path.insert(0, PathNode(pointer, "R"))
            else:
                if (return_path[0].avlnode == self.root.left) and (self.root.left != None):
                    return_path.insert(0, PathNode(self.root, "L"))
                elif (return_path[0].avlnode == self.root.right) and (self.root.right != None):
                    return_path.insert(0, PathNode(self.root, "R"))

            # zaburzenia wysokosci - ROTACJE
            if abs(self.get_height(pointer.right) - self.get_height(pointer.left)) > 1:  # brak wywazenia
                if return_path[1].which_side_for_parent == "L" and return_path[2].which_side_for_parent == "L":  # rotacja pojedyncza LL
                    self.rotate_l(pointer, pointer.left)

                elif return_path[1].which_side_for_parent == "L" and return_path[2].which_side_for_parent == "R":  # rotacja podwojna LR
                    self.rotate_r(return_path[1].avlnode, return_path[2].avlnode)
                    self.rotate_l(return_path[0].avlnode, return_path[2].avlnode)

                elif return_path[1].which_side_for_parent == "R" and return_path[2].which_side_for_parent == "L":  # rotacja podwojna RL
                    self.rotate_l(return_path[1].avlnode, return_path[2].avlnode)
                    self.rotate_r(return_path[0].avlnode, return_path[2].avlnode)

                elif return_path[1].which_side_for_parent == "R" and return_path[2].which_side_for_parent == "R":  # rotacja pojedyncza RR
                    self.rotate_r(pointer, pointer.right)

                # tu nie ma break bo w delete tak nie ma



            # aktualizacje wysokosci
            pointer.height = 1 + max(self.get_height(pointer.left), self.get_height(pointer.right))
            #if pointer.parent != None:
            #    if new_height > pointer.parent.height:
            #        pointer.parent.height = new_height

            # przejscie do rodzica
            pointer = pointer.parent

        return True # usunieto





    def rotate_l(self, a_node, b_node):

        # ustawienie rodzicow a_node i b_node
        _a_parent = b_node
        _b_parent = a_node.parent
        a_node.parent = _a_parent
        b_node.parent = _b_parent

        # ===
        # zamiana wezlow a_node i b_node gora-dol

        # referencje pomocnicze
        _b_right = a_node
        _a_left = b_node.right

        b_node.right = _b_right
        a_node.left = _a_left
        # ===

        # poprawianie rodzicow korzeni poddrzew b_node

        if b_node.parent != None:
            if b_node.parent.right == a_node:
                b_node.parent.right = b_node
            elif b_node.parent.left == a_node:
                b_node.parent.left = b_node


        # poprawianie rodzicow korzeni poddrzew a_node
        if a_node.left != None:
            a_node.left.parent = a_node
        if a_node.right != None:
            a_node.right.parent = a_node

        # jesli a_node jest korzeniem glownego drzewa to
        # korzeniem glownego drzewa staje sie b_node
        if a_node == self.root:
            self.root = b_node

        # fix na wysokosci
        a_node.height = 1 + max(self.get_height(a_node.left), self.get_height(a_node.right))
        b_node.height = 1 + max(self.get_height(b_node.left), self.get_height(b_node.right))

    def rotate_r(self, a_node, b_node):
        # ustawienie rodzicow a_node i b_node
        _a_parent = b_node
        _b_parent = a_node.parent
        a_node.parent = _a_parent
        b_node.parent = _b_parent

        # ===
        # zamiana wezlow a_node i b_node gora-dol

        # referencje pomocnicze
        _b_left = a_node
        _a_right = b_node.left

        b_node.left = _b_left
        a_node.right = _a_right
        # ===

        # poprawianie rodzicow korzeni poddrzew b_node

        if b_node.parent != None:
            if b_node.parent.right == a_node:
                b_node.parent.right = b_node
            elif b_node.parent.left == a_node:
                b_node.parent.left = b_node

        # poprawianie rodzicow korzeni poddrzew a_node
        if a_node.left != None:
            a_node.left.parent = a_node
        if a_node.right != None:
            a_node.right.parent = a_node

        # jesli a_node jest korzeniem glownego drzewa to
        # korzeniem glownego drzewa staje sie b_node
        if a_node == self.root:
            self.root = b_node

        # fix na wysokosci
        a_node.height = 1 + max(self.get_height(a_node.left), self.get_height(a_node.right))
        b_node.height = 1 + max(self.get_height(b_node.left), self.get_height(b_node.right))



# zapisywanie drzewka do pliku
def serialize(dict):
    with open("saved_dictionary.p", "wb") as f:
        pickle.dump(dict, f)

#=================
# ten mały fragmencik programu odpowiada za sklejanie
# 2 drzew a w zasadzie to dodaje jedno do drugiego
# oczywiście dałoby się to pewnie napisac wydajniej

    # wstawianie korzysta z wyszukiwania
    # korzen-lewy-prawy
def insert_klp(node, dest_dict):
    if node != None:
        dest_dict.insert(node.key)
        insert_klp(node.left, dest_dict)
        # insert nie przyjmuje calutkiego węzła z childami
        # i parentami, lecz tylko słówka

        insert_klp(node.right, dest_dict)

def add_dictionary(src_dict, dest_dict):
    insert_klp(src_dict.root, dest_dict)

#=================


def interface_switch(a, my_dictionary):
    if int(a) == 1:  # insert
        print("\n\n")
        print("Proszę wprowadzić słowo angielskie wraz z tłumaczeniami.")
        print("Wyrazy proszę oddzielić PRZECINKIEM!!!")

        dict_word = [element for element in input("> ").split(', ')]
        if len(dict_word) == 1:
            print(" /!\ Próbowano dodać słowo bez tłumaczeń!!! /!\ ")
            return
        dict_data = []
        dict_data.append(dict_word[0])
        dict_word.pop(0)
        dict_word = set(dict_word)
        dict_data.append(dict_word)
        try:
            my_dictionary.insert(dict_data)
            print("Słowo dodane ")
        except:
            pass

    if int(a) == 2:  # remove
        print("Proszę wprowadzić słowo angielskie do usunięcia.")
        print("Jeśli go nie ma to dam ci znać.")
        dict_data = input()
        if my_dictionary.delete(dict_data) == True:
            print(f"Usunięto słowo {dict_data}")
        else:
            print(f"Nie znaleziono słowa {dict_data}")

    if int(a) == 3:  # search
        print("\n\n")
        print("Wprowadź słowo angielskie: ")
        word = input()
        search_result = my_dictionary.search(word)
        if (search_result != None):
            print(f"Słowo: {search_result.key[0]},  tłumaczenia: {search_result.key[1]}")
        else:
            print("Nie znaleziono słowa: " + str(word))

    if int(a) == 4:  # serializacja
        serialize(my_dictionary)

    if int(a) == 5:  # wczytywanie...
        with open("saved_dictionary.p", "rb") as f:
            src_dict = pickle.load(f)
            add_dictionary(src_dict, my_dictionary)

def main():
    my_dictionary = AVLTree()

    # wczytanie listy wyrazów z csv zakodowanego w UTF-8 i konwersja na listę list

    try:
        with open("data_in.csv", encoding="utf8") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for row in csvreader: # row to lista rzeczy w linii pliku csv
                # tworzenie slowa ktore ma byc dodane
                dict_word = []
                dict_word.append(row[0])
                xd = set()
                # dict word jest 2 elementowa lista - 1 element to slowo angielskie a 2 to zbior polskich tlumaczen

                iterator = iter(row)  # skipuje 1 element w row
                next(iterator)        # czyli SLOWO ANGIELSKIE !!!
                for element in iterator:
                    xd.add(element)   # dodaje tlumaczenia do zbioru tlumaczen

                dict_word.append(xd)  # dodaje zbior na liste

                # print(row) # usunac
                my_dictionary.insert(dict_word)
    except:
        print("Brak wejściowego pliku tekstowego UTF-8, drzewo jest puste\n\n")


    while(True):
        print("Witamy w słowniku angielsko-polskim!!!")
        print("Co chcesz zrobić?")
        print("1. Dodać słowo angielskie wraz z jego tłumaczeniami.")
        print("    * jeżeli w słowniku słowo już istnieje, to dodane zostaną")
        print("    * kolejne jego tłumaczenia")
        print("2. Usunąć słowo angielskie wraz z jego tłumaczeniami.")
        print("3. Znaleźć słowo angielskie i wypisać jego tłumaczenia.")
        print("4. Zapisać słownik do pliku (binarnego).")
        print("5. Wczytać słownik (jeśli obecny jest niepusty, słowniki ""skleją się"")")
        print("    * jeżeli w obu słownikach jest ten sam angielski wyraz to zbiór polskich")
        print("    * tłumaczeń będzie sumą zbiorów tłumaczeń z obu słowników")
        print("0. Zamknij program.")
        print("Inna liczba - nie rób nic.")
        a = input()

        if a.isnumeric() == True:
            interface_switch(a, my_dictionary)
            if int(a) == 0: # konczenie
                print("\n\n")
                print("Zapisać słownik do pliku (binarnego)?")
                print("1. Tak")
                print("Inna opcja - Nie")
                b = input()
                if b.isnumeric() == True:
                    if int(b) == 1:
                        serialize(my_dictionary)
                return 0
        else:
            print("Nie podano liczby :(")
        print("\n\nNaciśnij ENTER aby kontynuować...")
        input()
        clear()

main()



