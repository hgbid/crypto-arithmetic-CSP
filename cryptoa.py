import copy

FAILURE = False
foundSol = 0
def isComplete(ans):
    for word in ans:
        for letter in word:
            if letter.isalpha():
                return False
    return True


def backtrack(ans, options, problem, iter):
    if isComplete(ans):
        global foundSol
        foundSol += 1
        printAnswer(ans, problem, foundSol)
        return True
    nextOptions = AC3(ans, options)
    csp = makeCSP(ans)
    var = MRV(csp)
    varOptions = LCV(nextOptions, var)
    for value in varOptions:
        if value != varOptions[0]: print(iter * 12 * " ", end="")
        print("let " + str(var) + " = " + str(value) + " >", end=" ")
        nextAns = updateAns(ans, var, value)
        nextOptions = updateOptions(options, var, value)
        if nextAns != FAILURE and nextOptions != FAILURE:
            optionsAfterAC3 = AC3(ans, nextOptions)
            if optionsAfterAC3 != FAILURE:
                backtrack(nextAns, optionsAfterAC3, problem, iter+1)
        print("FAILURE (" + var+")")
    return FAILURE


def noAlpha(expression):
    for letter in expression:
        if letter.isalpha():
            return False
    return True


def isValid(cps):
    for constraint in cps:
        if noAlpha(constraint):
            if not eval(constraint):
                return False
    return True

def updateAns(ans, var, value):
    # update 'ans' and check validation
    newAns = copy.copy(ans)
    for wordIndex in range(len(newAns)):
        for letterIndex in range(len(newAns[wordIndex])):
            if newAns[wordIndex][letterIndex] == var:
                newAns[wordIndex] = newAns[wordIndex].replace(var, str(value))
    cps = makeCSP(newAns)
    if not isValid(cps):
        return False
    return newAns

def AC3(ans, options):
    # add relevant vars to queue
    queue = []
    nextOptions = copy.deepcopy(options)
    cps = makeCSP(ans)
    for constraint in cps:
        for letter in constraint:
            if letter.isalpha() and letter not in queue:
                queue.append(letter)

    for var in queue:
        for option in nextOptions[var]:
            if not isValid(cps) and option in nextOptions[var]:
                nextOptions[var].remove(option)
                if len(nextOptions[var]) == 0:
                    return False
    return nextOptions

def updateOptions(options, var, value):
    newOptions = copy.deepcopy(options)
    # update options
    for key in newOptions:
        if value in newOptions[key]:
            newOptions[key].remove(value)
        if len(newOptions[key]) == 0:
            return False
    newOptions[var] = [value]

    for key in newOptions:
        if len(newOptions[key]) == 1:
            for key2 in newOptions:
                if newOptions[key] in newOptions[key2]:
                    newOptions[key2].remove(newOptions[key])
                    if len(newOptions[key2]) == 0:
                        return False

    return newOptions

def organizeProblem(fstWord, scdWord, trdWord):
    return ["0" * (len(trdWord) - len(fstWord)) + fstWord,
            "0" * (len(trdWord) - len(scdWord)) + scdWord,
            trdWord]


def MRV(cps):
    for constraint in cps:
        if constraint[2:4] == '==' and len(constraint) == 6 and constraint[0].isalpha():
            return constraint[0]

    letters = []
    for constraint in cps:
        letters += constraint
    countLetters = {}
    for letter in letters:
        if letter.isalpha():
            countLetters[letter] = letters.count(letter)
    return max(countLetters, key=countLetters.get)


def LCV(options, var):
    varOptions = copy.copy(options[var])
    varOptions.sort()
    return varOptions


def makeCSP(problem):
    fstWord, scdWord, trdWord = problem
    cps = [trdWord[-1] + "==(" + fstWord[-1] + "+" + scdWord[-1] + ")%10"]
    for index in range(len(trdWord) - 2, -1, -1):
        cps.append(trdWord[index] + "==(" + fstWord[index] + "+" + scdWord[index] +
                   "+(" + cps[len(cps) - 1][3:-3] + "//10))%10")
    if fstWord[0] == '0' and scdWord[0] == '0':
        cps.append(trdWord[0] + " == 1")
    cps.append(fstWord[findFirstIndex(fstWord)] + " != 0")
    cps.append(scdWord[findFirstIndex(scdWord)] + " != 0")
    cps.append(trdWord[0] + " != 0")
    return cps


def findFirstIndex(word):
    for index in range(0, len(word)):
        if word[index] != '0':
            return index
    return -1


def makeOptionList(problem):
    letters = problem[0] + problem[1] + problem[2]
    optionsList = {}
    for letter in letters:
        if letter.isalpha():
            optionsList[letter] = [i for i in range(0, 10)]
    return optionsList

def printAnswer(ans, problem, sol):
    unitedP = problem[0]+problem[1]+problem[2]
    unitedA = ans[0]+ans[1]+ans[2]
    ansDic = {}
    for index in range(0, len(unitedP)):
        if unitedP[index].isalpha():
            ansDic[unitedP[index]] = unitedA[index]
    ansDic = dict(sorted(ansDic.items()))
    print('\n'+"----------"*len(ansDic))
    print("Answer " + str(sol)+":", end="  ")
    for key in ansDic:
        print(key+" = " + ansDic[key], end="   ")
    print('\n'+"----------"*len(ansDic)+'\n')


if __name__ == '__main__':
    import sys
    fstWord, scdWord, trdWord = sys.argv[1], sys.argv[2], sys.argv[3]
    print("Problem: "+fstWord+" + " + scdWord + " = " + trdWord)

    problem = organizeProblem(fstWord, scdWord, trdWord)
    csp = makeCSP(problem)
    options = makeOptionList(problem)
    backtrack(problem, options, problem, 0)
    if not foundSol:
        print("There is no solution to the problem")
    else:
        print(str(foundSol)+" solutions have found")

