from random import randint
class Scramble_unit:
    first = 0
    second = 0
    def __init__(self, first,second):
        self.first = first
        self.second = second
class Scramble_patt:
    locations = {}
    counter = 0
    def __init__(self):
        self.locations = {}
        self.counter = 0
    def add(self, scrambleUnit):
        self.locations[self.counter] = scrambleUnit
        self.counter = self.counter + 1
def scramble(message, pattern):
    result = list(message)
    for i in range(0,len(pattern.locations)):
        scrambleUnit = pattern.locations[i]
        t = result[scrambleUnit.first]
        result[scrambleUnit.first] = result[scrambleUnit.second]
        result[scrambleUnit.second] = t
    return "".join(result)
def descramble(message,pattern):
    result = list(message)
    for i in range(len(pattern.locations)-1,-1,-1):
        scrambleUnit = pattern.locations[i]
        t = result[scrambleUnit.first]
        result[scrambleUnit.first] = result[scrambleUnit.second]
        result[scrambleUnit.second] = t
    return "".join(result)
def randomSP(limit):
    sp = Scramble_patt()
    for i in range(0,randint(1,limit)):
        su = Scramble_unit((randint(1,limit)-1), (randint(1,limit)-1))
        sp.add(su)
    return sp
def printsu(scramunit):
    print '({},{})'.format(scramunit.first,scramunit.second)
def key_to_len(key, length):
    good_len_key = ''
    x = 0
    for i in range(0,length):
        if x == len(key):
            x = 0
        good_len_key += list(key)[x]
        x = x + 1
    return good_len_key
def encrypt(mess,key):
    enmess = ''
    for i in range(0,len(mess)):
        enmess += addChars(list(mess)[i],list(key)[i])
    return enmess
def addChars(a,b):
    for i in range(0,ord(b)):
        if ord(a) == 126:
            a = chr(32)
        a = chr(ord(a)+1)
    return a
def decrypt(mess,key):
    demess = ''
    for i in range(0,len(mess)):
        demess += subChars(list(mess)[i],list(key)[i])
    return demess
def subChars(a,b):
    for i in range(0,ord(b)):
        if ord(a) == 33:
            a = chr(127)
        a = chr(ord(a)-1)
    return a
run = 1
print 'Enter e for encryption, d for decryption, and q to quit'
def format_scram_patt(scram_patt):
    s = ''
    for i in range(0,len(scram_patt.locations)):
        su = scram_patt.locations[i]
        s += '{},{},'.format(su.first,su.second)
    return s
def deformat_scram_patt(form_scram_patt):
    scram_patt = Scramble_patt()
    i = 0
    scram_patt_list = form_scram_patt.split(',')
    while i < len(scram_patt_list):
        first = int(scram_patt_list[i])
        i = i + 1
        second = int(scram_patt_list[i])
        i = i + 1
        scram_patt.add(Scramble_unit(first,second))
    return scram_patt
while run:
    command = raw_input('Command>> ')
    if command == 'q':
        run = 0
    elif command == 'e':
        mess = raw_input('Enter message to encrypt: ')
        key = raw_input('Enter an encryption key: ')
        scram_patt = randomSP(len(mess))
        scram_mess = scramble(mess,scram_patt)
        enmess = encrypt(scram_mess,key_to_len(key,len(mess)))
        result = enmess
        result += '|{}'.format(format_scram_patt(scram_patt))
        print result
    elif command == 'd':
        enmess = raw_input('Enter message to decrypt: ')
        key = raw_input('Enter an encryption key: ')
        scram_start = enmess.rfind('|')
        scram_formatted = enmess[scram_start:]
        scram_form = scram_formatted[1:len(scram_formatted)-1]
        scram_patt = deformat_scram_patt(scram_form)
        final_enmess = enmess[:scram_start]
        demess = decrypt(final_enmess, key_to_len(key, len(final_enmess)))
        descram = descramble(demess, scram_patt)
        print descram
    else:
        print 'invalid command'
