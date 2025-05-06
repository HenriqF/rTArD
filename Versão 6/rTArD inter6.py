import time
import sys
import random
import traceback
sys.set_int_max_str_digits(999999999)
with open("script.txt", "r") as file:
    script = file.read()

def imprimir(thing, mode=1):
    if mode == 1:
        print(thing)
    else:
        print(thing, end="")
def reprimir(arg):
    return (input(arg))

def run(script):
    try:   
        #Inicial 1=======
        startt = time.time()
        logs = False
        runtime = False
        if script[0] == "?":
            runtime = True
        if script[0] == "!":
            logs = True
            if script[1] == "?":
                runtime = True 
        #Inicial 2========= VARIAVEIS
        memory = {}
        functions = {}
        callStack = []
        falseConditionalExecution = False
        loopActive = []
        times = []
        j = [] #stack de indexes onde comeca um loop
        k = [] #stack de indexes onde termina um loop
        #Inicial 3=========
        imprimir("output===========") #Inicial.
        imprimir("\n")

        def getvalue(var):#Obter o valor de uma variavel
            if var[-1] == ">":
                for i, char in enumerate(var):
                    if char == "<":
                        try:
                            index = int(var[i+1:-1])
                        except:
                            if var[i+1:-1][0] == "@":
                                index = int(getvalue(var[i+2:-1]))
                        list = var[:i]
                        return(memory[list][index])
            else:
                return(memory[var])

        def operate(packet):#Leitor de operações braquete
            if packet == "[vdd]":
                return(True)
            if packet == "[fake]":
                return(False)
            packet = packet.replace("[", "")
            processed = packet
            j=0
            while "@" in processed:
                obj = ""
                index = ""
                while j < len(packet):
                    if packet[j] == "@":
                        while packet[j] != " " and packet[j] != "]":
                            obj = obj + packet[j]
                            j+=1
                        value = getvalue(obj[1:])
                        if isinstance(value, str):
                            text = '"' + value + '"'
                            processed = processed.replace(obj, str(text))
                        else:
                            processed = processed.replace(obj, str(value))
                            
                        obj = ""
                    j+=1
            processed = processed[:-1]
            return(eval(processed))
        
        def findBracket(i):#Função que volta o index do caractere depois do ultimo braquete de uma condicao.
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
        
        def actOnCondition(condition, i):#Função para condicionais IF ELIF
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
        
        def declareLogs(logs, runtime):#Função para declarar logs e runtime pós código.
            mensagenslegaisdefim = ["já parei caralho.","Vai mandar na sua vó fdp","RAAAASPUTIA","SAI DA MINHA MENTE SAI DA MINHA MENTE SA",
                                    "192.132.20.1 ( ͡° ͜ʖ ͡°)","whos in paris?","You are not have being polite","voce tá delulu por acaso?","kys","BABY IM PRAYIN ON YOU TONITE"]
            escolha = random.choice(mensagenslegaisdefim)
            imprimir("\n==================")
            imprimir(escolha)
            imprimir("==================\n")
            if runtime is True:
                imprimir("Runtime-----------")
                imprimir(str(time.time()-startt)+ "s")
                imprimir(" ")
            if logs is True:
                imprimir("MEMORIA-----------")
                imprimir("mem: "+ str(memory))
                imprimir("\n")
                imprimir("FUNÇÕES-----------")
                imprimir("funções: "+ str(functions))
                imprimir("callstack: "+ str(callStack))
                imprimir("\n")
                imprimir("CONDICIONAL-------")
                imprimir("fCExec: "+ str(falseConditionalExecution))
                imprimir("\n")
                imprimir("LOOPS-------------")
                imprimir("Status: "+str(loopActive))
                imprimir("Quantity: "+ str(times)) 
                imprimir("StackIndexInicio:"+ str(j))
                imprimir("StackIndexFim:"+ str(k))
        
        #Leitor do código
        currentWord = ""
        i = 0 #Index do caractere a ser analisado
        while i < len(script):
            if loopActive != []:
                pos = len(loopActive)-1
                if times[pos] == "while":
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
            if script[i] != " " and script[i] != "." and script[i] != "}":
                currentWord = currentWord + script[i]
            else:
                #VARIAVEIS
                if currentWord == "queseja": #Estrutura DECLARE VAR
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
                    elif currentValue[0] == "<":
                        currentValue = currentValue[1:-1].split(";")
                        if currentValue == ['']:
                            currentValue = []
                        else:
                            for l in range(len(currentValue)):
                                try:
                                    currentValue[l] = int(currentValue[l])
                                except:
                                    pass
                    elif currentValue == "vdd":
                        currentValue = True
                    elif currentValue == "fake":
                        currentValue = False

                    if currentKey[-1] == ">":
                        for l, char in enumerate(currentKey):
                            if char == "<":
                                index = currentKey[l+1:-1]   
                                currentKey = currentKey[:l]
                                break
                        try:
                            index = int(index)
                            list = memory[currentKey]
                        except:
                            index = int(getvalue(index[1:]))
                        list = memory[currentKey]
                        list[index] = currentValue
                        currentValue = list
                        
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
                    interval = "["
                    while script[i] != "]":
                        interval = interval + script[i]
                        i += 1
                    interval = interval + "]"
                    interval = interval.replace('atÃ©', '-')
                    i += 1
                    j.append(i+2)                      #lugar onde comeca o loop
                    k.append(findBracket(i))          #lugar onde termina o loop
                    times.append(abs(operate(interval))) #vezes
                    loopActive.append(True)
                elif currentWord == "enquanto": #estrutura WHILE
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
                elif currentWord == "deixeclaro": #estrutura imprimir
                    i += 1
                    currentText = ""
                    mode = 0
                    if script[i] == ",":
                        imprimir("")
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
                                imprimir("vdd", 0)
                            elif memory[currentText] is False:
                                imprimir("fake", 0)
                            else:
                                imprimir(memory[currentText], 0)
                        elif mode == 2:
                            result = operate(currentText)
                            if result is True:
                                imprimir("vdd", 0)
                            elif result is False:
                                imprimir("fake", 0)
                            else:
                                imprimir(result, 0)
                        else:
                            imprimir(currentText, 0)
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
                    chatInput = reprimir(currentText[1:])
                    try:
                        memory[var] = int(chatInput)
                    except:
                        memory[var] = chatInput
                    currentWord = ""
                    i+=1
                #FINALIZAR
                elif currentWord == "chegaporra": #Estrutura EXIT
                    declareLogs(logs, runtime)
                    return()
                elif currentWord == "dnvcaralho": #Estrutura RESTART
                    declareLogs(logs, runtime)
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
                    startt = time.time()

                #COMENTÁRIOS
                elif currentWord == "/#c/": #Estrutura COMMENT
                    comentario = ""
                    while "/#c/" not in comentario:
                        comentario = comentario + script[i]
                        i += 1
                    currentWord = ""
                    i += 1

                else:
                    i += 1
                    currentWord = ""
            i += 1
    except Exception as error:
        print("\n")
        print(error, traceback.format_exc())
        imprimir("\nvtmnc prinaha aprende a me usar fdp")
        return()
run(script)
while True:
    pass