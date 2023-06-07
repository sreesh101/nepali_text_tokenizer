import sys
import gzip
import os
import shutil
import re
from collections import Counter

# Your function start here

def checkVowels(word):
    vowels = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ए", "ऐ", "ओ", "औ", "ऋ", "ा", "ि", "ी" , "ु", "ू", "े", "ै", "ो", "ौ", "ं", "ँ", "ः"]
    check = False
    for vowel in vowels:
        if word.endswith(vowel):
            check = True
    return check

def checkOpen(word):
    vowels = ["क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह", "क्ष", "त्र", "ज्ञ"]
    check = False
    for vowel in vowels:
        if vowel in word:
            check = True
    return check

def checkConjuncts(word):
    check = False
    for conjunct in data_conjucts:
        if conjunct in word:
            check = True
    return check

def checkClosed(word):
    check = False
    for i in data_conjucts:
        if word.endswith(i):
            check = True
    return check

def checkLatin(word):
    check = False
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for i in alphabet:
        if i in word:
            check = True
    return check

def porterStemmerA(words: list[list[str]]):
    for section in words:
        i = section
        if not section == []:
            for word in section:
                j = word
                if word.endswith("ैरहेको"):
                    word = word[:-6]
                if word.endswith("मा") or word.endswith("ले"):
                    word = word[:-2]    
                if word.endswith("लाई"):
                    word = word[:-2]    
                if word.endswith("को") or word.endswith("का") or word.endswith("की") or word.endswith("कै"):
                    word = word[:-2] 
                if word.endswith("कै"):
                    word = word[:-2] 
                if word.endswith("ेको") or word.endswith("हरू"):
                    word = word[:-3] 
                section[section.index(j)] = word
        words[words.index(i)] = section
    return words

def porterStemmerB(words: list[list[str]]):
    for section in words:
        i = section
        if not section == []:
            for word in section:
                j = word
                if word.endswith("्"):
                    word = word[:-1]
                section[section.index(j)] = word
        words[words.index(i)] = section
    return words   

def porterStemmerC(words: list[list[str]]):
    for section in words:
        i = section
        if not section == []:
            for word in section:
                j = word
                if checkVowels(word):
                    word = word[:-1]
                section[section.index(j)] = word
        words[words.index(i)] = section
    return words   

def porterStemmerD(words: list[list[str]]):
    for section in words:
        i = section
        if not section == []:
            for word in section:
                j = word
                if checkLatin(word):
                    section.remove(j)
                else:
                    section[section.index(j)] = word
        words[words.index(i)] = section
    return words   
            
def tokenizer(words: list[list[str]]):
    final_ind = []
    for word in words:
        while (word.startswith("http") and ((word.endswith(".") or word.endswith(",")))):    #for links
            word = word[:-1]
        if word.startswith("http"):
            final_ind.append([word])
            continue
        word = word.lower()     #lowercase
        if (word.replace(".", "").replace(",", "").replace("+", "").replace("-", "")).isnumeric():     #numbers
            final_ind.append([word])
            continue
        word = word.replace("'", "")        #apostrophe
        word = word.replace(".", "")
        word = word.replace("।", "")
        if "-" in word:
            mid = word.split("-")
            mid.append(word.replace("-", ""))
            mid = tokenizer(mid)
            final_ind.append(mid)
            continue
        word = re.split("\!|\@|\#|\$|\%|\^|\;|\:|\||\&|\*|\(|\)|\/|\"|\"|\.|\,|\_|\?|\[|\]|\{|\|।}", word)
        final_ind.append(word)
    for i in final_ind:
        if isinstance(i[0], list):
            temp = []
            for j in i:
                for k in j:
                    temp.append(k)
            final_ind[final_ind.index(i)] = temp
    for i in final_ind:
        for j in i:
            if j == "" or j == '':
                final_ind[final_ind.index(i)].remove(j)
    return final_ind

def textFileProcess(inputZipFile, outputFileName, tokenType, stopList, stemming, stopword_lst):
    data = gzip.open(os.path.join(sys.path[0], inputZipFile), 'rt', encoding='utf-8')
    info = data.read()
    data.close()
    words = info.split()
    original = info.split()
    for i in original:
        original[original.index(i)] = i.replace('\x00', '')
    for i in original:
        original[original.index(i)] = i.replace('0ustar00', '')
    words = original.copy()
    if tokenType == "fancy":
        words = tokenizer(words)
    else:
        for word in words:
            words[words.index(word)] = [word]
    if stopList == "yesStop":
        for word in words:
            for i in word:
                if i in stopword_lst:
                    word.remove(i)
    if stemming == "porterStem":
        words = porterStemmerA(words)
        words = porterStemmerB(words)
        words = porterStemmerC(words)
        words = porterStemmerC(words)
        words = porterStemmerD(words)
    for word in words:
        for i in word:
            if i == '' or i == "":
                word.remove(i)
    tracker = []
    unique_tracker = []
    plot_x = []
    plot_y = []
    printing = open(os.path.join(sys.path[0], outputFileName + "_token_list.txt"), 'w', encoding="utf-8")
    heaps = open(os.path.join(sys.path[0], outputFileName + "_heap.txt"), 'w', encoding="utf-8")
    stats = open(os.path.join(sys.path[0], outputFileName + "_statistics.txt"), 'w', encoding="utf-8")
    for i in range(0, len(original)):
        printing.write(original[i].rstrip() + " ")
        if i is not []:
            for j in words[i]:
                printing.write(j + " ")
                tracker.append(j)
                if j not in unique_tracker:
                    unique_tracker.append(j)
                if len(tracker) % 10 == 0:
                    heaps.write(str(len(tracker)) + " " + str(len(unique_tracker)) + "\n")
                    plot_y.append(len(unique_tracker))
                    plot_x.append(len(tracker))
            printing.write("\n")
    #for Stats stuff
    count = list((sorted((Counter(tracker)).items(), key = lambda item : item[1])))
    count.reverse()
    max = int(count[0][1])
    stat_tracker = []
    for i in range(0, max):
        stat_tracker.append([])
    for i in count:
        stat_tracker[int(i[1]) - 1].append(i)
    for i in range(0, len(stat_tracker) - 1):
        stat_tracker[i] = (sorted(stat_tracker[i]))
    stats.write(str(len(tracker)) + "\n" + str(len(unique_tracker)) + "\n")
    hundred_counter = 0
    stat_tracker.reverse()
    for i in stat_tracker:
        for j in i:
            if hundred_counter < 100:
                stats.write(str(j[0]) + " " + str(j[1]) + "\n")
                hundred_counter = hundred_counter + 1
    printing.close()
    heaps.write(str(len(tracker)) + " " + str(len(unique_tracker)))
    heaps.close()
    stats.close()

if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "nepali_literature_manipur.tar.gz"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "output"
    tokenize_type = sys.argv[3] if argv_len >= 4 else "fancy"
    stoplist_type = sys.argv[4] if argv_len >= 5 else "yesStop"
    stemming_type = sys.argv[5] if argv_len >= 6 else "porterStem"
    temp = open(os.path.join(sys.path[0], "conjuncts_data.txt"), 'rt', encoding='utf-8')
    data_conjucts = temp.read()
    temp.close
    data_conjucts = data_conjucts.split()
    for i in data_conjucts:
        if i.isnumeric():
            data_conjucts.remove(i)
    stopword_lst = stopword_lst = ["र", "त", "नी", "पो", "है", "ल", "अनी", "त्यो", "अँ", "रे", "नै", "पनी", "के", "नि", "कि", "उ", "हरू", "मा", "को", "सँग", "यो",
                                     "लाई", "लागी", "नाई", "ऊ", "पनि", "भने", "हुन्", "हो", "छन्", "भए", "छ", "यस", "भए", "सन", "भएर", ""]
    textFileProcess(inputFile, outputFilePrefix, tokenize_type, stoplist_type, stemming_type, stopword_lst)
