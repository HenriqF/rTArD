import time
import sys
import tkinter as tk

#criar a janela
#########################################
janela = tk.Tk()
janela.geometry('1250x950')
janela.title("rTaRD v.5500")
#########################################
sys.set_int_max_str_digits(999999999)

def run(script):
    try:
        startt = time.time()
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

        #funcoes de print e input, para o programa leitor
        def imprimir(thing, mode=1):
            if mode == 1:
                output.config(state=tk.NORMAL)
                output.insert(tk.END, str(thing) + "\n")
                janela.update()
            else:
                output.config(state=tk.NORMAL)
                output.insert(tk.END, str(thing))
                janela.update()

        def reprimir(arg):
            output.config(state=tk.NORMAL)
            output.insert(tk.END, str(arg))
            mensagem = ""
            while "\n\n" not in mensagem:
                mensagem = scriptinput.get("1.0", tk.END)
                janela.update()
            output.config(state=tk.NORMAL)
            output.insert(tk.END, str(mensagem[:-1]))
            scriptinput.config(state=tk.NORMAL)
            scriptinput.delete("1.0", tk.END)
            janela.update()
            return(mensagem[:-1])

        imprimir("output===========")
        imprimir("\n")

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
                    # imprimir(script[i:])
                    # imprimir(script[k[pos]])
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
            #imprimir(loopActive, times, j ,k)
            if script[i] != " " and script[i] != "." and script[i] != "}":
                currentWord = currentWord + script[i]
            else:
                #imprimir(",", i, "--->" , currentWord)
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
                    # imprimir(j, k ,times, loopActive)
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

                #imprimir e INPUT
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
                    if logs is True:
                        imprimir("\n==================")
                        imprimir("já parei caralho.")
                        imprimir("==================")
                        imprimir("RUNTIME-----------")
                        imprimir(str(time.time()-startt)+"s")
                        imprimir("==================")
                        imprimir("Logs==============")
                        imprimir("\n")
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
                        imprimir("Status: "+ str(loopActive))
                        imprimir("Quantity: "+ str(times)) 
                        imprimir("PonteiroInicio:"+ str(j))
                        imprimir("PonteiroFim:"+ str(k))
                    else:
                        imprimir("\n==================")
                        imprimir("já parei caralho.")
                        imprimir("==================")
                    return()
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
                    imprimir("\noutput===========", 1)
                    imprimir("RUNTIME-----------", 1)
                    imprimir(str(time.time()-startt)+"s", 1)
                    imprimir("==================\n", 1)
                    startt = time.time()
                    

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
        pass
    except:
        output.config(state=tk.NORMAL)

        output.insert(tk.END, str("\nvtmnc prinaha aprende a me usar fdp") + "\n")
        return()

def pegar():
    codigo = input.get("1.0", tk.END).strip()
    if codigo != "":
        run(codigo)

def limpar():
    output.config(state=tk.NORMAL)
    output.delete("1.0", tk.END)
    scriptinput.config(state=tk.NORMAL)
    scriptinput.delete("1.0", tk.END)

#Decoracao
textoinput = tk.Label(janela, text="Coloca a porra do codigo aqui:")
textoinput.grid(row=0, column=1, padx=10, pady=10)
textoinput2 = tk.Label(janela, text="Retorno:")
textoinput2.grid(row=0, column=2, padx=10, pady=10)
#input,output
output = tk.Text(janela, height=50, width=75, state=tk.DISABLED)
output.grid(row=1, column=2, padx=10, pady=10)

scriptinput = tk.Text(janela, height=2, width=75)
scriptinput.grid(row=2, column=2, padx=10, pady=10)

input = tk.Text(janela, height=50, width=75)
input.grid(row=1, column=1, padx=10, pady=10)
#botao
botao = tk.Button(janela, text="Fazer o código correr", command=pegar, width=80, height=2)
botao.grid(row=2, column=1)

limpar = tk.Button(janela, text="Limpar o bglh", command=limpar, width=80, height=2)
limpar.grid(row=3, column=1)

janela.mainloop()