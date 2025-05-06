with open("script.txt", "r") as file:
    script = file.read()

logs = False
if script[0] == "!":
    logs = True

memory = {}

functions = {}
callStack = []

falseConditionalExecution = False

loopActive = []
times = []
j = []
k = []

print("output===========")
print("\n")

#Leitor de operações braquete
def operate(packet):
    if packet == "[vdd]":
        return(True)
    if packet == "[fake]":
        return(False)
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
                if isinstance(memory[obj[1:]], str):
                    text = '"'
                    text = text + memory[obj[1:]]
                    text = text + '"'
                    processed = processed.replace(obj, str(text))
                else:
                    processed = processed.replace(obj, str(memory[obj[1:]]))
                obj = ""
            j+=1
    processed = processed.replace("]", "")
    return(eval(processed))
def findBracket(i): #volta o valor do caractere depois do ultimo braquete de uma condicao. 
    i += 2
    bracketStack = ["{"]
    while bracketStack != []:
        if script[i] == "{":
            bracketStack.append("{")
        elif script[i] == "}":
            if bracketStack.pop() != "{":
                bracketStack.append("}")
                bracketStack.append("}")
        i += 1 
    return(i)
def actOnCondition(condition, i):
    result = operate(condition)
    if result is False:
        i = findBracket(i)
        #busca para else , elif e braquete solitario
        search = True
        keyword = ""
        while search is True:
            j = i
            j += 1
            while script[j] != " " and script[j] != "." and script[i] != "}":
                keyword = keyword + script[j]
                j += 1
            if keyword == "senrolar" or keyword == "oucpa":
                return(i, True)
            else:
                return(i, False)
    else:
        return(i+1, False)
        
#Leitor do código
currentWord = "" #Palavra atual
i = 0            #Ponteiro de Caractere
while i < len(script):
    if loopActive != []:
        pos = len(loopActive)-1
        if times[pos] == "while":
            # print(script[i:])
            # print(script[k[pos]])
            if i >= k[pos]:
                i = j[pos]
        else:
            if i >= k[pos]:
                i = j[pos]
                times[pos] -= 1
            if times[pos] == 0:
                del j[pos]
                del k[pos]
                del times[pos]
                del loopActive[pos]
    #print(loopActive, times, j ,k)
    if script[i] != " " and script[i] != "." and script[i] != "}":
        currentWord = currentWord + script[i]
    else:
        #print(",", i, "--->" , currentWord)
        #VARIAVEIS
        if currentWord == "queseja": #Estrutura DECLARE
            currentKey = ""
            currentValue = ""
            i += 2
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
        elif currentWord == "caso":  #estrutura IF
            i += 1
            condition = ""
            while script[i] != "{":
                condition = condition + (script[i])
                i += 1     
            action = actOnCondition(condition, i)
            falseConditionalExecution = action[1]
            i = action[0]
            currentWord = ""
        elif currentWord == "oucpa": #estrutura ELIF
            i += 1
            condition = ""
            while script[i] != "{":
                condition = condition + (script[i])
                i += 1
            if falseConditionalExecution == True:
                action = actOnCondition(condition, i)
                falseConditionalExecution = action[1]
                i = action[0]
                currentWord = ""
            else:
                i = findBracket(i)
                currentWord = ""
        elif currentWord == "senrolar": #estrutura else
            if falseConditionalExecution == False:
                i = findBracket(i)
                currentWord = ""
            else:
                i += 2
                falseConditionalExecution = False
                currentWord = ""
        
        #LOOPS
        elif currentWord == "para": #estrutura FOR
            i += 2
            subject = ""
            goal = ""
            if script[i] == "0":
                subject = 0
                i += 1
            else:
                i += 1
                while script[i] != " ":
                    subject = subject + script[i]
                    i += 1
            while script[i] != "@":
                i += 1
            i += 1
            while script[i] != "]":
                goal = goal + script[i]
                i += 1 
            if subject != 0:
                subject = memory[subject]
            goal = memory[goal]
            i += 1
            j.append(i+2)                      #lugar onde comeca o loop
            k.append(findBracket(i))          #lugar onde termina o loop
            times.append(abs(subject - goal)) #vezes
            loopActive.append(True)
        elif currentWord == "enquanto": #estrutura WHILE
            # print(j, k ,times, loopActive)
            start = i-8
            i += 1
            condition = ""
            while script[i] != "{":
                condition = condition + (script[i])
                i += 1
            if operate(condition) == True:
                if j == [] or j[::-1][0] != start:
                    j.append(start)
                    k.append(findBracket(i))
                    times.append("while")
                    loopActive.append(True)
                currentWord = ""
                i += 1
            else:
                position = len(loopActive)-1
                if j != []:
                    if j[::-1][0] == start:
                        del j[pos]
                        del k[pos]
                        del times[pos]
                        del loopActive[pos]
                i = findBracket(i)
                currentWord = ""

        #PRINT e INPUT
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
        elif currentWord == "receba":
            i += 1
            currentText = ""
            var = ""
            while script[i] != ",":
                currentText = currentText + script[i]
                if script[i] == "@":
                    i += 1
                    while script[i] != " ":
                        var = var + script[i]
                        i += 1
                        currentText = " "
                i += 1
            chatInput = input(currentText[1:])
            try:
                memory[var] = int(chatInput)
            except:
                memory[var] = chatInput
            currentWord = ""
            i+=1
        #FINALIZAR
        elif currentWord == "chegaporra": #Estrutura EXIT
            if logs is True:
                print("\n==================")
                print("já parei caralho.")
                print("==================")
                print("Logs==============")
                print("\n")
                print("MEMORIA-----------")
                print("mem: ", memory)
                print("\n")
                print("FUNÇÕES-----------")
                print("funções: ", functions)
                print("callstack: ", callStack)
                print("\n")
                print("CONDICIONAL-------")
                print("fCExec: ", falseConditionalExecution)
                print("\n")
                print("LOOPS-------------")
                print("Status: ",loopActive)
                print("Quantity: ", times) 
                print("PonteiroInicio:", j)
                print("PonteiroFim:", k)
            else:
                print("\n==================")
                print("já parei caralho.")
                print("==================")
            while True:
                pass
        elif currentWord == "dnvcaralho": #Estrutura RESTART
            memory = {}
            functions = {}
            callStack = []
            falseConditionalExecution = False
            loopActive = []
            times = []
            j = []
            k = []
            i = -1
            currentWord = ""
            print("\noutput===========\n")

        #COMENTÁRIOS
        elif currentWord == "/#c/": #Estrutura COMMENT
            comentário = ""
            while "/#c/" not in comentário:
                comentário = comentário + script[i]
                i += 1
            currentWord = ""
            i += 1

        else:
            i += 1
            currentWord = ""
    i += 1