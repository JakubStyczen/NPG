import re
import math
#re do dokumentacji panowie poczytajcie cos i napiszcie o tym imporcie, mozecie opisac jak dziala ten patern ponziej  
#math do logarytmu o dowolnej podstawie 


#potrzebny do walidacji danych liczbowych
pattern = re.compile(r'(^\d+\.?\d*[+-]\d+\.?\d*j$|^\d+\.?\d*j?$)')



#testy to powyzszego regex

#test = '''
#-0
#2
#2+
#+2
#2j
#222j
#222
#2.222
#2.222j
#2+2j
#2.2+2.2j
#22+22
#j
#asdas
#sad+sad
#'''
#raw = test.split('\n')
#matches = pattern.match(test)
#for match in raw:
#    if pattern.match(match):
#        print(match)





##### WŁAŚCIWY KOD

#kolejka potrzebna do przechowywania ostatnich 10 dzialan
class Queue(object):
    #konstruktor inicjalizuje pusta liste
    def __init__(self):
        self.operations = []

    #metoda do wpisywania na ostatnie miejsce kolejki nowa operacje
    def enqueue(self, operation):
        self.operations.insert(0, operation)
    
    #Metoda do usuwania pierwszej operacji 
    def dequeue(self):
        return self.operations.pop()

    #zwraca dlugosc kolejki
    def size_of(self):
        return len(self.operations)

    #umozliwia iterowanie w petli po elementach kolejki
    def __iter__(self):
        return iter(self.operations)


#####FUNCKJE OBLICZAJACE
def add(arg1, arg2):
    return arg1 + arg2

def sub(arg1, arg2):
    return arg1 - arg2

def mul(arg1, arg2):
    return arg1 * arg2

def div(arg1, arg2):
    if arg2 != 0:
        return arg1 / arg2
    else: 
        print("Nie dziel przez 0!!!")  

def pot(podstawa, wykladnik):
    return podstawa**wykladnik

def nth_root(num ,n):
    return num**(1/n)


def logarytm(podstawa, arg):
    b = arg.real
    a = podstawa.real
    if (a > 0 and a != 1) and b > 0:
        return math.log(arg.real, podstawa.real)
    else:
        print('Liczby z poza dziedziny logarytmu!')

def calc(operator, arg1, arg2):    
    current_operation = operators[operator]
    return current_operation(arg1, arg2)




######Funkcje do walidacji danych wejsciowych
def isValid(text, expression):
    return True if text not in  expression else False

def isValidDigit(text, pattern):
    variable = input(text)
    while not (re.search(pattern, variable)):
        print('Bledne dane! Format to X, Yj lub X+Yj!')
        variable = input(text)
    return variable

def validatioInputString(input_string, expression):
    variable = input(input_string)
    while isValid(variable, expression):
        print('Bledne dane! ')
        variable = input(input_string)
    return variable


###FUNCKJE do formatowania wypisywania liczb 

def printForm(sol):
    if sol.imag == 0:
        print(f'{sol.real:.4f}')
    elif sol.real == 0:
        print(f'{sol.imag:.4f}j')
    else:
        print(f'{sol:.4f}')


#### PETLA GLOWNA

if __name__ == '__main__':
    try:
        operators = {'1' : add, '2' : sub,'3' : mul, '4' : div, '5' : pot, '6' : nth_root, '7' : logarytm}
        #str_operators = {'1' : '+', '2' : '-','3' : '*', '4' : '/', '5' : '^', '6' : '^1/'}
        store = Queue()
        print('\n------------------------------\n'+
        'Witaj w poteznym kalkulatorze TS, zostaniesz poproszony o wybor dzialnia ' +
        'oraz podanie argumrtow dzialnia.\nLiczby zespolone nalezy wpisywac w formacie X+Yj!\n'+
        '------------------------------\n')
        while True:
            #Przyjmowanie danych od uzytkownika
            operator = validatioInputString('Wybierz dzialanie +(1) -(2) *(3) /(4) ^(5) \u221A(6) log(7): ', operators.keys())
            ans1, ans2  = None, None
            #wybor wynikow do uzywanych argumentow
            if store.size_of() > 0:
                prev = validatioInputString('Czy chcesz użyc poprzecnich wynikow? Y/N ', ['Y', 'N'])
                if prev == 'Y':
                    for idx, sol in enumerate(store):
                        print(f'{idx+1}.', end = " ")
                        printForm(sol)
                    ans1 = int(validatioInputString('Podaj numer wyniku do 1 argumentu lub 0 jeżeli nie chcesz nic wpisywać: ', [str(x) for x in range(store.size_of() + 2)]))
                    ans2 = int(validatioInputString('Podaj numer wyniku do 2 argumentu lub 0 jeżeli nie chcesz nic wpisywać: ', [str(x) for x in range(store.size_of() + 2)]))
                    ans1 = store.operations[ans1 - 1] if ans1 != 0 else None
                    ans2 = store.operations[ans2 - 1] if ans2 != 0 else None
                    print(ans1, ans2)
            #wyprowadzenie argumentow         
            if ans1 == None:
                arg1 = isValidDigit('Podaj 1 arg: ', pattern)
                arg1 = complex(arg1)
            else: 
                arg1 = ans1
            if ans2 == None:    
                arg2 = isValidDigit('Podaj 2 arg: ', pattern)
                arg2 = complex(arg2)
            else: 
                arg2 = ans2

            #dodanie do kolejki wyniku
            solution = calc(operator, arg1, arg2)
            if store.size_of() == 10:
                store.dequeue()
                store.enqueue(solution)
            else:
                store.enqueue(solution)

            #podanie wyniku i pytanie o czyszczenie pamieci
            print('Wynik:', end = " ")
            printForm(solution)
            read = validatioInputString('Czy chcesz zobaczyc historie dzialan? Y/N ', ['Y', 'N'])
            if read == 'Y':
                clear = validatioInputString('Czy chcesz wyczyscic CALA pamiec? Y/N ', ['Y', 'N'])
                if clear == 'Y':
                    store.operations = []
                    print('Pamiec wyczyszczona! ')
                elif clear == 'N':
                    print('Ostatniew dzialania to... ')
                    for idx, sol in enumerate(store):
                        print(f'{idx+1}.', end = " ")
                        printForm(sol)
                        
    except KeyboardInterrupt:
        print("Wyjscie z programu")

