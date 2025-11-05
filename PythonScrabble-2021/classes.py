# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:22:08 2021

@author: Iliopoulou
"""

''' Scrabble 2021 - Ηλιοπούλου'''
import json
import random
from datetime import date
from itertools import permutations

#Αρχικά, ορίζω την αξία και την συχνότητα των γραμμάτων
lets={'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]}

#Συνάρτηση που βρίσκει την αξία μιας λέξης
def value(word):
    v=0
    for i in word:
        v += lets[i][1]
    return v

#Συχνότητα μιας λέξης
def freq(i):
    return lets[i][0]

#Εισάγω τις λέξεις. Το λεξικό είναι πιο γρήγορη μέθοδος, θα την προτιμήσω για να μην έχω καθυστερήσεις με το παιχνίδι.
gr7={}
f = open("greek7.txt", encoding="utf-8")
for l in f.readlines():
    l = l.replace("\n", '')
    gr7[l]=l
f.close()

#Συνάρτηση που δείχνει αν μια λέξη υπάρχει στο αρχείο greek7
def accepted(w):
    if w in gr7:
        return True
    else:
        return False

#Συνάρτηση που δείχνει εάν ένα γράμμα βρίσκεται στο σακουλάκι
#Έχω χρησιμοποιήσει λίστα και τη μέθοδο remove για τις περιπτώσεις όπου σε μια λέξη έχω γράψει το ίδιο γράμμα παραπάνω φορές από όσες έχω στο σακούλι μου
def exist(w,lex):
    li=list(lex)
    a=0
    for i in w:
        if i not in li:
            a=a - 1
        else:
            li.remove(i)
    if a>-1:
        return True
    else:
        return False
       
        

    

class SakClass:

    def __init__(self):
        self.letters = []
        
        for letter in lets:
            self.addletters(letter, freq(letter))
        self.randomize_sak()


    def __repr__(self):
        return self.letters.__repr__()

   
    def getletters(self, n):
        if n > len(self.letters):
            return False
        l = self.letters[:n]
        del self.letters[:n]
        return l

    def putbackletters(self, letters):
        for l in letters:
            self.letters.append(l)
        self.randomize_sak()


    def randomize_sak(self):
        random.shuffle(self.letters)

    def addletters(self,letter, times):
        for i in range(times):
            self.letters.append(letter)

class Player:
    def __init__(self):
        self.letters = []
        self.score = 0
        

    def __repr__(self):
        pass

    def restore_leters(self, sak):
        if len(self.letters) < 7:
            newletters = sak.getletters(7-len(self.letters))
            if not newletters:
                self.letters = False
                return False
            self.letters = self.letters + newletters

    def change_letters(self,sak):
        old = self.letters
        self.letters = sak.getletters(7)
        if not self.letters:
            return False
        sak.putbackletters(old)
        return True

class Human(Player):
    
    
    def play(self, sak):
        msg = ''
        for i in self.letters:
            msg += i + ',' +str(value(i)) + ' - '
        print('Γράμματα στο σακουλάκι:', len(sak.letters))
        print('\nΉρθε η σειρά σου!')
        print('\nΔιαθέσιμα γράμματα: ', msg)
        
        while True:
            word = input('Γράψε τη λέξη σου!\n')
            removed = []
            if word=='q' or word=='p':
                break
            if not exist(word,self.letters):
                print('ΑΚΥΡΟ!\n Έχεις χρησιμοποιήσει γράμμα που δεν υπάρχει στο σακουλάκι σου!\n')
                continue
            if not accepted(word):
                print('Η λέξη που έγραψες δεν υπάρχει!\n')
                continue
            for l in word:
                removed.append(l)
                self.letters.remove(l)
            break
            
        self.restore_leters(sak)
        return word
    
    
    

class Computer(Player):

    def __init__(self):
        Player.__init__(self)
        self.level = "SMART - FAIL"

    

    def smartfail(self, sak):
        perm = ""
        for l in self.letters:
            perm += l
        allwords = []
        allvalues = []
        for i in range(8, 2, -1):
            words = list(permutations(perm, i))
            for w in words:
                w = ''.join(w)
                if accepted(w) and w not in allwords:
                    allwords.append(w)
                    allvalues.append(value(w))
    #Δημιουργώ μία δομή η οποία έχει ως στοιχεία πλειάδες ανίστοιχων λέξεων - αξιών
    #Με τη συνάρτηση sorted(), ταξινομώ τα ζευγάρια κατά αύξουσα σειρά.
    # Αυτό σημαίνει πως το τελευταίο στοιχείο είναι ο καλύτερος δυνατός συνδυασμός
        lista = sorted(zip(allvalues, allwords))
    #Εγώ θέλω συνήθως η λέξη να βρίσκεται τυχαία από διάστημα μέσα στο 40% των καλύτερων λέξεων
    #Όμως να υπάρχει 20% πιθανότητα να βρίσκεται στο άλλο διάστημα, με τις χειρότερες λέξεις
        n=random.randint(1,10)
        if n%4:
            thesi =random.randint(int(0.6*len(lista)),len(lista)-1)
            max_word = lista[thesi][1]
            return max_word
        else:
            thesi=random.randint(0,int(0.6*len(lista)))
            max_word = lista[thesi][1]
            return max_word


    def play(self, sak):
        msg = ""
        for i in self.letters:
            msg += i + ',' + str(value(i)) + ' - '
        print("Γράμματα στο σακουλάκι: ", len(sak.letters))
        print("Παίζει o Η/Υ.\n")
        print('Γράμματα Η/Υ: ' + msg)
        to_play = self.smartfail(sak)
        for l in to_play:
            self.letters.remove(l)
        self.restore_leters(sak)
        return to_play    
    
    
class Game():
    def __init__(self):
        self.words = {}
        self.sak = None
        self.scenario = "SMART-FAIL"
        self.human = Human()
        self.cpu = Computer()
        self.moves = 0
        self.best_word = ""
        try:
            with open("data.json", "r") as f:
                self.data = json.load(f)
        except:
            self.data = {}


    def setup(self):
        self.human = Human()
        self.cpu = Computer()
        self.cpu.level = self.scenario
        self.sak = SakClass()
        self.human.letters = self.sak.getletters(7)
        self.cpu.letters = self.sak.getletters(7)
        #self.data = {}
        self.moves = 0
        self.best_word = ""



    def run(self):
        self.setup()
        
        while True:
            word = self.human.play(self.sak)
            if word == 'q':
                break
            elif word == 'p':
                self.human.change_letters(self.sak)
                print("Άλλαξες όλα σου τα γράμματα.")
            else:
                self.human.score += value(word)
                self.moves += 1
                if value(word) > value(self.best_word):
                    self.best_word = word
                print("Αποδεκτή λέξη!\nΒαθμοί: ", value(word), " \tΣκόρ: ", self.human.score)
            
                
            if not self.human.letters:
                print("Τελείωσαν τα γράμματα από το σακουλάκι. Το παιχνίδι θα τελειώσει!")
                break
            input("Enter για Συνέχεια")

            word = self.cpu.play(self.sak)
            if not word:
                print("Ο Η/Υ δεν έχει κάποια διαθέσιμη λέξη. Το παιχνίδι θα τελειώσει.")
                break
            self.cpu.score += value(word)
            self.moves += 1
            if value(word) > value(self.best_word):
                self.best_word = word
            print("Λέξη Η/Υ: ", word, "\nΒαθμοί: ", value(word), " \tΣκόρ: ", self.cpu.score)
            if not self.cpu.letters:
                print("Τελείωσαν τα γράμματα από το σακουλάκι. Το παιχνίδι θα τελειώσει!")
                break
        self.end()

    def end(self):
        winner = ""
        print("-------ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ-------")
        print("Οι βαθμοί σου: ", self.human.score)
        print("Οι βαθμοί του Η/Υ:", self.cpu.score)
        if self.human.score >= self.cpu.score:
            print("Κέρδισες! :)")
            winner = "Παίκτης"
        else:
            print("'Εχασες!  :(")
            winner = "Η/Υ"
        print("------------------------------")
        id = len(self.data) + 1
        self.data[int(id)] = {
            "Score Η/Υ": self.cpu.score,
            "Score Παίκτη": self.human.score,
            "Νικιτής": winner,
            "Date": str(date.today()),
            "Καλύτερη λέξη": self.best_word,
            "Λέξεις που παίχτηκαν": self.moves
        }
        with open("data.json", "w") as f:
            json.dump(self.data, f)


    def menu(self):
        print('***SCRABBLE***')
        print('---------------')
        print('1: Σκόρ')
        print('2: Παιχνίδι')
        print('q: Έξοδος')
        print('---------------')
        print('Αν κατά τη διάρκεια του παιχνιδιού δεν μπορείς να σκεφτείς μια λέξη, πατάς p και αλλάζεις όλα τα γράμματα στο σακουλάκι σου')
        c = input()
        while c not in "123q":
            c = input("Παρακαλώ δώσε μια επιλογή από 1-3:")
        if c == 'q':
            exit(0)
        elif c == '1':
            self.show_score()
            self.menu()
        elif c == '2':
            self.run()

    

    def show_score(self):
        if not self.data:
            print("Δεν υπάρχουν προηγούμενα δεδομένα για προβολή.")
            return
        for game_id, game in sorted(self.data.items()):
            print('--------------------')
            print("Παρτίδα Νο:", game_id)
            for i,j in game.items():
                print(i, ":", j)
            print('--------------------')
            print()
        input("Enter για επιστροφή στο μενού...")