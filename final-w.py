import os
import ast

###################################################FILE OPERATIONS################################################

def read_files(input_file, encoding='utf-8'):
    try:
        # Read from the input file
        with open(input_file, 'r', encoding=encoding) as f:
            content = f.read()

        print(f"Content has been read from {input_file}")
        return content

    except FileNotFoundError as e:
        raise ValueError(f"File not found: {e}")
    


def write_files(content , output_file, encoding='utf-8'):
    try:

        # Write to the output file
        with open(output_file, 'w', encoding=encoding )as f:
            f.write(content)

        print(f"Content has been written to {output_file}")

    except FileNotFoundError as e:
        raise ValueError(f"File not found: {e}")
    

def empty_files(output_file, encoding='utf-8'):
    try:

        # Write to the output file
        with open(output_file, 'a', encoding='utf-8' )as f:
            f.truncate(0)

        print(f"Content has been copied from {input_file} to {output_file}")

    except FileNotFoundError as e:
        raise ValueError(f"File not found: {e}")





#######################################################INDIVIDUAL TRANSLATORS#################################################



def print_command (python_code):
    flag =0
    python_code = python_code.strip()
    list = python_code.split('(')
    if list[0] == 'print':
        flag = 1
        return "System.out.println(\"" + python_code[7:-2] + "\");\n" , flag
    else: return 0 , flag



def assign_stmnt(python_code):
    flag =0    
    tree = ast.parse(python_code)
    java_code = ""

    for node in tree.body:
        if isinstance(node, ast.Assign):
            flag = 1
            # Translate assignment statement
            java_code += "int " + node.targets[0].id + " = " + ast.unparse(node.value) + ";\n"
            return java_code , flag
        elif isinstance(node, ast.Expr):
            flag =1
            # Translate mathematical expression
            java_code += "System.out.println(" + ast.unparse(node.value) + ");\n"
            return java_code , flag

        else: return 0 , flag


def if_stmnt(python_if_statement):
    try:
        # Parse the Python if statement
        tree = ast.parse(python_if_statement)
        if_stmt = tree.body[1]

        # Check if the input is a valid if statement
        if not isinstance(if_stmt, ast.If):
            raise ValueError("Invalid if statement")

        # Extract the condition and branches
        condition = ast.unparse(if_stmt.test)

        #true_branch = ast.unparse(if_stmt.body[0].value)
        true_branch = []
        for i in range(len(if_stmt.body[:])) :
            true_branch.append(ast.unparse(if_stmt.body[i].value))

        #false_branch = ast.unparse(if_stmt.orelse[0].value) if if_stmt.orelse else ""
        false_branch = []
        for i in range(len(if_stmt.orelse[:])) :
            false_branch.append(ast.unparse(if_stmt.orelse[i].value))


        # Translate to Java
        java_if_statement = "if (" + condition + ") {\n"

        for v in range(len(true_branch[:])) :
            dr = translate(true_branch[v])
            java_if_statement += "    " + str(dr[0])
            #java_if_statement += "    System.out.println(\"" + true_branch[v][7:-2] + "\");\n"

        if false_branch:
            java_if_statement += "} else {\n"
            for i in range(len(false_branch[:])) :
                yr = translate(false_branch[i])
                java_if_statement += "    " + str(yr[0])
                #java_if_statement += "    System.out.println(\"" + false_branch[i][7:-2] + "\");\n"
        java_if_statement += "}"

        return java_if_statement

    except SyntaxError as e:
        raise ValueError("Invalid Python syntax: " + str(e))


def while_loop(python_code, loop_var):
    # Parse the Python code to extract the condition and body
    tree = ast.parse(python_code)
    if isinstance(tree.body[0], ast.While):
        condition = ast.unparse(tree.body[0].test)

        w_true_branch = []
        for i in range(len(tree.body[0].body)) :
            w_true_branch.append(ast.unparse(tree.body[0].body[i]))

        #ast.unparse(tree.body[0].body[1])
    else:
        raise ValueError("Input is not a valid Python while loop")

    # Replace the loop variable in the condition and body
    condition = condition.replace(loop_var, 'i')
    for s in range(len(w_true_branch)) :
         w_true_branch[s] = w_true_branch[s].replace(loop_var, 'i')
   
         
    #w_true_branch = w_true_branch.replace(loop_var, 'i')

    # Translate the condition and body to Java
    java_condition = condition.replace('and', '&&').replace('or', '||').replace('not', '!')
    java_w_body = ''
    for v in range(len(w_true_branch)) :
            dr = translate(w_true_branch[v])
            if dr[1] == 1:
                 line = str(dr[0]).split('int')
                 java_w_body += "    " + str(line[1])
            else: 
                 gh = print_command(w_true_branch[v])
                 java_w_body += print_command(gh[0])
                 # java_w_body += str(w_true_branch[v].replace('print', 'System.out.println'))
                 #java_body = body.replace('print', 'System.out.println').replace('true', 'True').replace('false', 'False')

    # Generate the Java while loop
    java_code = f'while ({java_condition}) {{\n{java_w_body}\n}}'

    return java_code




#########################################################COLLECTIVE TRANSLATORS#######################


def translate_1 (python_code):
    p = print_command (python_code)
    if p[1] == 1:
        return p
    a = assign_stmnt(python_code)
    if a[1] == 1:
        return a
    if_stmnt(python_code)


def translate_2 (python_code):
    p = print_command (python_code)
    if p[1] == 1:
        return p
    a = assign_stmnt(python_code)
    if a[1] == 1:
        return a
    while_loop(python_code)



def maiin(python_code):
     x = translate_1(python_code)
     if(x):
         return 0;

     y = translate_2(python_code)

