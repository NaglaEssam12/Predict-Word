import re

from tkinter import *

trigramArray = []
countTrigramArray = []

substringArray = []
countSubstringArray = []

probabilityArray = []

sortedResult = []

def readFile(fileName):
    dataFile = open(fileName, encoding="utf-8")

    fileContent = dataFile.readlines()
    dataFile.close()

    return fileContent

def trigram(fileContent):
    arr = []

    for i in fileContent:
        # If the line is not empty
        if len(i) > 1:
            # Remove these symbols if found in each line
            i = re.split(';|,|\*|؟|\s', i)
            i = " ".join(i)

            # Break sentence in the token, remove empty tokens
            tokens = [token for token in i.split(" ") if token != ""]

            # Use the zip function to help us generate n-grams
            ngrams = zip(*[tokens[k:] for k in range(3)])

            # Concatentate the tokens into ngrams and return
            trigrams1 = [" ".join(ngram) for ngram in ngrams]

            # Append all trigrams of each line to one array
            for k in trigrams1:
                k = "".join(k)
                arr.append(k)

            # To determine the end of line
            last = arr[-1]
            last = last.split(' ')
            newLast = last[1] + " " + last[2] + " " + "."
            arr.append(newLast)

    return arr

def calculateTrigramsCount(arr):
    for i in arr:
        # To avoid the repeated trigrams
        if(i not in trigramArray):
            count = arr.count(i)
            trigramArray.append(i)
            countTrigramArray.append(count)

def calculateSubstringCount():
    counter = 0
    for i in trigramArray:
        tmp = i.split(' ')
        substring = tmp[0] + " " + tmp[1]

        # To avoid the repeated substring
        if substring not in substringArray:
            substringArray.append(substring)

            for j in trigramArray:
                # Count the substring
                if substring in j:
                   index = trigramArray.index(j)
                   counter += countTrigramArray[index]

            countSubstringArray.append(counter)
            counter = 0

def calculateProbabilities():
    for i in trigramArray:
        tmp = i.split(' ')

        # Get substring of the trigram i
        substring = tmp[0] + " " + tmp[1]
        index = substringArray.index(substring)

        # Get the count of the substring
        substringCount = countSubstringArray[index]
        index = trigramArray.index(i)

        # Get the count of the trigram that contains the substring
        threeWordsCount = countTrigramArray[index]

        # Calculate the probabaility
        probability = threeWordsCount / substringCount
        probabilityArray.append(probability)

def nextWordsPredictions(word):
    result = []
    probs = []
    sortedProbs = []
    sortedResult = []

    for i in trigramArray:
        tmp = i.split(' ')
        # Get the first two words in the trigrams array
        firstTwoWords = tmp[0] + " " + tmp[1]

        # Check if the entered words matches with the first two words in the trigrams array
        if word == firstTwoWords:
            result.append(i)
            index = trigramArray.index(i)
            probs.append(probabilityArray[index])
            sortedProbs.append(probabilityArray[index])

    # Sort the probability array according to highest probabilities
    sortedProbs.sort(reverse=True)
    for i in sortedProbs:
        index = probs.index(i)

        # To avoid repeating
        probs[index] = -1
        sortedResult.append(result[index])

    return sortedResult

# Main
fileName = 'dataFile.txt'
# fileName = 'smallTest.txt'

fileContent = readFile(fileName)

arr = trigram(fileContent)

calculateTrigramsCount(arr)
calculateSubstringCount()

calculateProbabilities()


# GUI
def checkkey(event):
    # Get words from the gui
    value = event.widget.get()
    sortedResult = nextWordsPredictions(value)
    data = sortedResult[:10]
    update(data)


def update(data):
    # Clear previous data
    lb.delete(0, 'end')

    # Put new data
    for item in data:
        lb.insert('end', item)


# Driver code

root = Tk()
root.geometry("400x300")

# Creating text box
e = Entry(root, width=50)

e.pack()
e.bind('<KeyRelease>', checkkey)

# Creating list box
lb = Listbox(root, width=50)
lb.pack()

root.mainloop()