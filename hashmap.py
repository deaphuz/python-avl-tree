# w tej haszmapie:
# kluczami są stringi
# danymi jest coś co ładnie wyświetla swoją reprezentację tekstową :)

class HashMapElement:
    key = None
    data = None

    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __str__(self):
        return f"{self.key}, {self.data}"

class HashMap:
    array = None
    length = None

    def __init__(self, length):
        self.array = []
        self.length = length
        for p in range(0, self.length):
            self.array.append(None)

    def put(self, key, data):
        try:
            # haszowanie
            x = ''.join(str(ord(c)) for c in key) # string -> wartosci ascii
            x = int(x) % self.length


            if self.array[x] == None:
                self.array[x] = []
            self.array[x].append(HashMapElement(key, data))
            return True
        except:
            return False

    def get(self, key):
        try:
            # haszowanie
            x = ''.join(str(ord(c)) for c in key) # string -> wartosci ascii
            x = int(x) % self.length


            for element in self.array[x]:
                if element.key == key:
                    return element
        except:
            return False
        return False


    def remove(self, key):
        try:
            # haszowanie
            x = ''.join(str(ord(c)) for c in key) # string -> wartosci ascii
            x = int(x) % self.length


            for element in self.array[x]:
                if element.key == key:
                    self.array[x].remove(element)
                    return True
        except:
            return False
        return False

    def clear(self):
        self.array = []




def main():
    dictionary = HashMap(1373)
    dictionary.put("dziesięć", 10)
    dictionary.put("jedenaście", 11)
    dictionary.put("trzydzieści siedem", 37)
    dictionary.put("osiemnaście", 18)
    dictionary.put("trzysta", 300)

    print(dictionary.get("jedenaście"))
    print(dictionary.get("trzysta"))
    print(dictionary.get(43))
    dictionary.clear()
    dictionary = HashMap(1373)
    dictionary.put("siedemnaście", "dwjdawjdiajwodajowidw")
    print(dictionary.get("siedemnaście"))
    dictionary.remove("siedemnaście")
    print(dictionary.get("siedemnaście"))


    #print(int.from_bytes(dictionary, "big"))




main()