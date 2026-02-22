from copy import deepcopy


def error():
    print("SHOOT")
    print(0/0)

def evaluator(equation:list , KEY_SYMBOLS:list): #Does equations badly
    """
    Docstring for evaluator
    
    :param equation: Its a list hopefully 
    """
    i = len(equation)-1
    while i >=0: #Start with indices these are funky what can I say something something left associativity or is it right?
        if equation[i] == "^":
            equation[i] = equation[i-1] ^ equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        i -=1

    i = 0
    while i < len(equation):
        if equation[i] == "*":
            equation[i] = equation[i-1] * equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "/": #The elifs are just for efficiency they are not required from a logical point of view as you will always be on a number (I hope)
            equation[i] = equation[i-1] / equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "//":
            equation[i] = equation[i-1] // equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "%":
            equation[i] = equation[i-1] % equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        i+= 1 
    
    i = 0
    while i < len(equation):
        if equation[i] == "+":
            equation[i] = equation[i-1] + equation[i+1]
            equation.pop(i+1)
            equation.pop(i-1)
            i -= 1
        elif equation[i] == "-":
            if i == 0:
                equation[i] = -equation[i+1]
                equation.pop(i+1)
            else:
                equation[i] = equation[i-1] - equation[i+1]
                equation.pop(i+1)
                equation.pop(i-1)
                i -= 1
        i+= 1 
    return(equation)

def indent_count(line):
    indent_count = 0
    i = 0
    while i < len(line):
        if line[i] == " ":
            indent_count += 1
        else:
            return(indent_count)
        i+=1
    return(indent_count)

def tokeniser(line): #Something something tokens
    """
    Docstring for tokeniser
    
    :param line: Description
    :param KEY_SYMBOLS: Description
    :param NUMS: Description
    :param CHARACTERS: Description
    """
    working_part = ""
    working_part_type = ""
    string = False
    tokenised = []
    for i in range(len(line)):
            if line[i] in KEY_SYMBOLS and not string and working_part_type != "symbol":
                if len(working_part) != 0:
                    tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
                if i != len(line)-1:
                    if line[i]+line[i+1] not in KEY_SYMBOLS:
                        tokenised.append((line[i],"symbol"))
                    else:
                        working_part = line[i]
                        working_part_type = "symbol"
                else:
                    working_part = line[i]
                    working_part_type = "symbol"
            elif line[i] in KEY_SYMBOLS and working_part_type == "symbol":
                working_part = working_part + line[i] 
                tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
            elif len(working_part) == 0 and line[i] in NUMS:
                working_part = line[i]
                working_part_type = "int"
            elif working_part_type == "int" and line[i] in NUMS:
                working_part = working_part + line[i]
            elif working_part_type!= "string" and line[i] == " ":
                if len(working_part) != 0:
                    tokenised.append((working_part,working_part_type))
                working_part = "" 
                working_part_type = ""
            elif len(working_part) == 0 and line[i].upper() in CHARACTERS and working_part_type !="string":
                 working_part = line[i]
                 working_part_type = "var"
            elif working_part_type == "var" and (line[i] in NUMS or line[i].upper() in CHARACTERS):
                working_part = working_part + line[i] 
            elif len(working_part) == 0 and line[i] == "'":
                working_part_type = "string"
                working_part = ""
            elif working_part_type== "string" and line[i] != "'":
                working_part = working_part +line[i]
            elif working_part_type== "string" and line[i] == "'":
                tokenised.append((working_part,working_part_type))
                working_part = ""
                working_part_type = ""

    if len(working_part) != 0:
        tokenised.append((working_part,working_part_type))
        working_part = "" 
        working_part_type = ""
    for i in range(len(tokenised)):
        if tokenised[i][0] in KEY_WORDS:
            tokenised[i]= (tokenised[i][0],"key word")
        if tokenised[i][1] == "int":
            tokenised[i] = (int(tokenised[i][0]), "int")
    if len(tokenised) == 1:
        return(tokenised[0])
    return(tokenised)
                 
def equation(line):
    equation = []
    for x in range(0, len(line)):
        if line[x][1] == "int":
            equation.append(int(line[x][0]))
        if line[x][1] == "symbol":
            equation.append(line[x][0])
        if line[x][1] == "var":
            if line[x][0] in variables:
                equation.append(variables[line[x][0]])
            else:
                error()
        if line[x][1] == "string":
            equation.append(str([line[x][0]]))
    result = evaluator(equation, KEY_SYMBOLS)
    if len(result) > 1:
        error()
    else:
        result = result[0]
    return(result)

def truth_statement(line):
    return(1)

def expression(line):
    i = 0
    open_bracket = False
    brackets = []
    hit_list = []
    bracket_debt = 0
    while i < len(line):
        if line[i] == ("(", "symbol") and not open_bracket:
            open_bracket = True
            brackets = []
            line.pop(i)
            continue
        if line[i] == ("(", "symbol"):
            bracket_debt -= 1

        if open_bracket and not (line[i] == (")", "symbol") and bracket_debt==0):
            brackets.append(line[i])
            hit_list.append(i)
        if open_bracket and line[i] == (")", "symbol") and bracket_debt == 0:
            line[i] = tokeniser(str(expression(deepcopy(brackets))))
            open_bracket = False
            for x in range(len(hit_list)-1, -1,-1):
                line.pop(hit_list[x])
                bracket_debt = 0 
            hit_list = []
            i = 0 
            continue

        if line[i] == (")", "symbol"):
            bracket_debt += 1
        i+=1 
    chunks = []
    parts = []
    for i in range(len(line)):
        if (line[i][0] in COMPARISONS ) and line[i][1] == "symbol":
            chunks.append(tokeniser(str(equation((parts)))))
            chunks.append(line[i])
            parts = []
        else:
            parts.append(line[i])
    chunks.append(tokeniser(str(equation((parts)))))
    if len(chunks) == 1:
        if chunks[0][1] == "int":
            return(int(chunks[0][0]))
        return(chunks[0][0])
    if len(chunks) == 3:
        if chunks[0][0] == chunks[2][0] and chunks[1][0] == "==":
            return(True)
        elif chunks[0][0] > chunks[2][0] and chunks[1][0] == ">":
            return(True)
        elif chunks[0][0] < chunks[2][0] and chunks[1][0] == "<":
            return(True)
        else:
            return(False)
    


KEY_SYMBOLS = ["=", "+", "*", "^", "/", ")", "(", "%", "//", "-", ",", "==", ">", "<"]
COMPARISONS = ["==", ">", "<"]
NUMS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]
CHARACTERS = "QWERTYUIOPASDFGHJKLZXCVBNM_"
KEY_WORDS = ["print", "while"]

file = open("program.txt", "r")

program = file.readlines()

file.close()

tokenised = []
indentations = []
for i in range(len(program)):
    program[i] = program[i].replace("\n", "")
    tokenised.append(tokeniser(program[i])) # type: ignore
    indentations.append(indent_count(program[i]))
indentations.append(0)

variables = {}
line_stack = [(0,0)]
i = 0 
while i< len(tokenised):
    line = tokenised[i]
    if len(line) == 0:
        continue
    if line[0][1] == "var":
            if line[1][0] == "=":
                result = expression(line[2:])
                variables.update({line[0][0]: result})
            
    if line[0][1] == "key word":
        if line[0][0]== "print":
            if line[1] == ("(", "symbol") and line[-1] == (")", "symbol"):
                running_expression = []
                output = []
                for x in range(2,len(line)-1):
                    if line[x] == (",", "symbol"):
                        output.append(expression(running_expression))
                        running_expression = []
                    else:
                        running_expression.append(line[x])
                if len(running_expression) != 0:
                    output.append(expression(running_expression))
                print(output[0])
        if line[0][0] == "while":
                looped = False
                if expression(line[1:]):
                    looped = True
                    if line_stack[-1][0]!= indentations[i]+4:
                        line_stack.append((indentations[i]+4,i ))
                elif line_stack[-1][0]== indentations[i]+4:
                    #i-=1
                    line_stack.pop(-1)
                if not looped:
                    line_index = i +1
                    for x in range(line_index, len(indentations)):
                        if indentations[x] >= indentations[line_index]:
                            i+=1
                        else:
                            break
    i+=1
    if len(line_stack) > 1:
        if indentations[i] != line_stack[-1][0]:
            i = line_stack[-1][1]
            
                    
print(variables)
