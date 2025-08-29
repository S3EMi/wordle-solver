storedArray = []

def readWordList():
    with open("words.txt", "rt") as f:
        for line in f:
            word = line.strip()
            storedArray.append(word)
            print("Added ", word, " to array\n")

def writeToSorted():
    storedArray.sort()
    with open("sorted.txt", "a") as f:
        for i in storedArray:
            f.write(i)
            f.write("\n")
            print("Added ", i, " to sorted file.\n")

readWordList()    
writeToSorted()