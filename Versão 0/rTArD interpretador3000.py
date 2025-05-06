with open("script.txt", "r") as file:
    script = file.read()

memory = {}
functions = {}
callStack = []
conditionalStack = []

print("output===========")
print("\n")

#Leitor de operações braquete
def operate(packet):
    packet = packet.replace("[", "")
    processed = packet
    j=0
    while "@" in processed:
        obj = ""
        while j < len(packet):
            if packet[j] == "@":
                while packet[j] != " " and packet[j] != "]":
                    obj = obj + packet[j]
                    j+=1
                processed = processed.replace(obj, str(memory[obj[1:]]))
                obj = ""
            j+=1
    processed = processed.replace("]", "")
    return(eval(processed))
def findbracket(b):
    b += 2
    while script[b] != "}":
        if script[b] == "{":
            while script[b] != "}":
                b += 1
            b += 1
        b += 1
    return(b)
def evaluateconditional(b):
    currentConditional = ""
    conditionalResult = False
    while script[b] != "]":
        currentConditional = currentConditional + script[b]
        b += 1
    else:
        currentConditional = currentConditional + script[b]
        conditionalResult = (operate(currentConditional))
    if conditionalResult is False:
        b = findbracket(b)
        conditionalStack.append(False)
        b += 1
    else:
        conditionalStack.append(True)
        b += 2
    return(b)

#Leitor do código
currentWord = "" #Palavra atual
i = 0            #Ponteiro de Caractere
while i < len(script):
    if script[i] != " " and script[i] != "." and script[i] != "}":
        currentWord = currentWord + script[i]
        #print(i, currentWord) #mostra o ponteiro e a palavra.
    else:
        #print(i, currentWord)
        #VARIAVEIS
        if currentWord == "queseja": #Estrutura DECLARE
            currentKey = ""
            currentValue = ""
            i += 1
            while script[i] != " ":
                currentKey = currentKey + script[i]
                i += 1
            i += 1
            while script[i] != ",":
                currentValue = currentValue + script[i]
                i += 1

            if currentValue[0] == "$":
                currentValue = int(currentValue[1:])
            elif currentValue[0] == "#":
                currentValue = str(currentValue[1:])
            elif currentValue[0] == "[":
                currentValue = operate(currentValue)
            elif currentValue == "vdd":
                currentValue = True
            elif currentValue == "fake":
                currentValue = False

            memory[currentKey] = currentValue
            i += 1
            currentWord = ""
        
        #FUNÇÕES
        elif currentWord == "sejaisso": #estrutura DEF
            currentName = ""
            findOut = ""
            i += 1
            while script[i] != ",":
                currentName = currentName + script[i]
                i += 1
            functions[currentName] = i+2
            findOut = findOut + script[i]
            while "slktofora" not in findOut:
                findOut = findOut + script[i]
                i += 1
            i += 1
            currentWord = ""
        elif currentWord == "slktofora": #estrutura RETURN
            i = (callStack.pop()+1)
            currentWord = ""
        elif currentWord == "ligueja0800": #estrutura CALL
            i += 1
            objectiveName = ""
            while script[i] != ",":
                objectiveName = objectiveName + script[i]
                i += 1
            callStack.append(i)
            currentWord = ""
            if objectiveName in functions:
                i = functions[objectiveName] -1
            else:
                i += 1
        
        #CONDICIONAIS
        elif currentWord == "caso": #estrutura IF
            i += 1
            i = evaluateconditional(i)
            currentWord = ""        
        elif currentWord == "oucpa": #estrutura ELIF
            lastCond = conditionalStack.pop()
            if lastCond is True:
                conditionalStack.append(True)
                while script[i] != "{":
                    i += 1
                i = findbracket(i)
                currentWord = ""
                i += 1
            else:
                i = evaluateconditional(i)
                currentWord = ""        
        elif currentWord == "senrolar": #estrutura ELSE
            lastCond = conditionalStack.pop()
            if lastCond is True:
                i = findbracket(i)
                currentWord = ""
                i += 1
            else:
                currentWord = ""
                i += 2
        
        #PRINT
        elif currentWord == "deixeclaro": #estrutura PRINT
            i += 1
            currentText = ""
            mode = 0
            if script[i] == ",":
                print("")
            else:
                if script[i] == "@":
                    mode = 1
                    i+=1
                elif script[i] == "[":
                    mode = 2
                    i+=1
                    currentText = currentText + "["
                while script[i] != ",":
                    currentText = currentText + script[i]
                    i += 1
                if mode == 1:
                    if memory[currentText] is True:
                        print("vdd", end="")
                    elif memory[currentText] is False:
                        print("fake", end="")
                    else:
                        print(memory[currentText], end="")
                elif mode == 2:
                    result = operate(currentText)
                    if result is True:
                        print("vdd", end="")
                    elif result is False:
                        print("fake", end="")
                    else:
                        print(result, end="")
                else:
                    print(currentText, end="")
            currentWord = ""
            i += 1
        
        #FINALIZAR
        elif currentWord == "chegaporra": #Estrutura EXIT
            print("\n==================")
            print("já parei caralho.")
            print("==================")
            print("Logs==============")
            print("memoria:   ", memory)
            print("funcoes:   ", functions)
            print("callstack: ", callStack)
            print("conditionalstack:", conditionalStack)
            while True:
                pass
        else:
            i += 1
            currentWord = ""
    i += 1