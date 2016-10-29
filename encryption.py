from random import randint
import random
import string
import sys
import getpass
import os
successful_decrypted_message = "<<<Successful file decrypt>>>"
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
    if a == '\n':
        return a
    if a == '\t':
        return a
    for i in range(0,ord(b)):
        if ord(a) == 126:
            a = chr(31)
        a = chr(ord(a)+1)
    return a
def decrypt(mess,key):
    demess = ''
    for i in range(0,len(mess)):
        demess += subChars(list(mess)[i],list(key)[i])
    return demess
def subChars(a,b):
    if a == '\n':
        return a
    if a == '\t':
        return a
    for i in range(0,ord(b)):
        if ord(a) == 32:
            a = chr(127)
        a = chr(ord(a)-1)
    return a
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
def rankey(size):
    return ''.join(random.choice(string.letters + string.digits + string.punctuation) for _ in range(size))
def help():
    print "Use: python .encryption.py -<opt> -<opt> -<opt> ... <args> <args> <args> ..."
    print "options:"
    print "encrypting message with key: -ek <message> <key>"
    print "encrypting message without key: -e  <message> (key will be in included in output)"
    print "decrypting: -d <message> <key>"
    print "encrypt file with key: -ef"
    print "decrypt file with a key: -df"
    print "To split a file: -s <file>    (result and key file generated)"
    print "To join a file: -j <Rfile> <Kfile2>"
    #print "encrypt/decrypt message with scrambling: -s"
    print "Example: python .encryption.py -ek <message> <key>"
    #print "Example N.2: python .encryption.py -d -s <message> <key> <scramble>"
    print "Help menu: -?"
def encryptFile(filename, key):
    fr = open(filename, 'r')
    lines = fr.readlines()
    fw = open(filename, 'w')
    location = random.randint(0,len(lines)-1)
    x = 0
    for l in lines:
        if x == location:
            fw.write(encrypt(successful_decrypted_message+l, key_to_len(key,len(successful_decrypted_message+l))))
        else:
            fw.write(encrypt(l,key_to_len(key,len(l))))
        x = x + 1
    fw.close()
def decryptFile(filename, key):
    fr = open(filename, 'r')
    lines = fr.readlines()
    success = 0
    decrypted_lines = []
    for l in lines:
        decrypted_mess = decrypt(l, key_to_len(key,len(l)))
        if successful_decrypted_message in decrypted_mess:
            decrypted_mess = decrypted_mess[len(successful_decrypted_message):]
            success = 1
        decrypted_lines.append(decrypted_mess)
    if success:
        fw = open(filename, 'w')
        for dl in decrypted_lines:
            fw.write(dl)
        fw.close()
    else:
        print 'Wrong Key.'
def split(filename):
    fr = open(filename, 'r')
    lines = fr.readlines()
    fw = open(filename, 'w')
    fw.close()
    os.remove(filename)
    result_lines = []
    key_lines = []
    for line in lines:
        key = rankey(len(line))
        result = encrypt(line, key)
        result_lines.append(result)
        key_lines.append(key)
    rf = open('R{}'.format(filename), 'w')
    for rl in result_lines:
        rf.write(rl)
    rf.close()
    kf = open('K{}'.format(filename), 'w')
    for kl in key_lines:
        kf.write('{}\n'.format(kl))
    kf.close()
    print 'R{} and K{} files created.'.format(filename,filename)
    print 'You will need them both to retrieve the original file.'
def join(rf, kf):
    rr = open(rf, 'r')
    rlines = rr.readlines()
    rr.close()
    kr = open(kf, 'r')
    klines = kr.readlines()
    kr.close()
    os.remove(rf)
    os.remove(kf)
    fw = open(rf[1:],'w')
    for i in range(0, len(rlines)):
        fw.write(decrypt(rlines[i], klines[i]))
    fw.close()
    print '{} file created.'.format(rf[1:])
args = sys.argv
if len(args) == 1:
    help()
elif args[1] == '-?':
    help()
elif args[1] == '-ek':
    if len(args) == 3:
        key = getpass.getpass()
        print encrypt(args[2], key_to_len(key, len(args[2])))
    else:
        m = raw_input('Message: ')
        key = getpass.getpass()
        print encrypt(m, key_to_len(key, len(m)))
elif args[1] == '-e':
    if len(args) == 3:
        key = rankey(len(args[2]))
        print encrypt(args[2], key)
        fw = open('key.txt', 'w')
        fw.write(key)
        fw.close()
        print 'Key written in key.txt'
    else:
        m = raw_input('Message: ')
        key = rankey(len(m))
        print encrypt(args[2], key)
        fw = open('key.txt', 'w')
        fw.write(key)
        fw.close()
        print 'Key written in key.txt'
elif args[1] == '-d':
    if len(args) == 3:
        key = getpass.getpass()
        print decrypt(args[2], key_to_len(key, len(args[2])))
    else:
        m = raw_input('Message: ')
        k = getpass.getpass()
        print decrypt(m, key_to_len(k, len(m)))
elif args[1] == '-ef':
    if len(args) == 3:
        key = getpass.getpass()
        print 'Confirm password:'
        ck = getpass.getpass()
        if key == ck:
            encryptFile(args[2],key)
        else:
            print 'Passwords must match'
    else:
        f = raw_input('Filename: ')
        k = getpass.getpass()
        print 'Confirm password:'
        ck = getpass.getpass()
        if k == ck:
            encryptFile(f,k)
        else:
            print 'Passwords must match'
elif args[1] == '-df':
    if len(args) == 3:
        key = getpass.getpass()
        decryptFile(args[2], key)
    else:
        f = raw_input('Filename: ')
        k = getpass.getpass()
        decryptFile(f, k)
elif args[1] == '-s':
    if len(args) == 3:
        split(args[2])
    else:
        filename = raw_input('filename: ')
        split(filename)
elif args[1] == '-j':
    if len(args) == 4:
        join(args[2], args[3])
    else:
        result_file = raw_input('result file: ')
        key_file = raw_input('key file: ')
        join(result_file,key_file)
else:
    help()

"""
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
"""
