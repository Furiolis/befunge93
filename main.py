# Befunge Interpreter
import random


def interpret(code):
    pointer_row = 0
    pointer_char = -1
    order = 'RIGHT'
    string_mode = False
    skip = False
    output = ""
    stack = []
    code = code.split("\n")
    while True:
        if order == 'RIGHT':
            pointer_char += 1
        elif order == 'LEFT':
            pointer_char -= 1
        elif order == 'UP':
            pointer_row -= 1
        elif order == 'DOWN':
            pointer_row += 1

        try:
            instruction = code[pointer_row][pointer_char]
        except IndexError:
            continue

        # Trampoline: Skip next cell.
        if skip:
            skip = False
            continue

        # " Start string mode: push each character's ASCII value all the way up to the next ".
        if string_mode:
            if instruction == '"':
                string_mode = False
            else:
                stack.append(ord(instruction))

        # 0-9 Push this number onto the stack.
        elif instruction.isdigit():
            stack.append(int(instruction))

        # + Addition: Pop a and b, then push a+b.
        elif instruction == '+':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            stack.append(a + b)

        # - Subtraction: Pop a and b, then push b-a.
        elif instruction == '-':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            stack.append(b - a)

        # * Multiplication: Pop a and b, then push a*b.
        elif instruction == '*':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            stack.append(a * b)

        # / Integer division: Pop a and b, then push b/a, rounded down. If a is zero, push zero.
        elif instruction == '/':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            if a != 0:
                stack.append(b // a)
            else:
                stack.append(0)

        # % Modulo: Pop a and b, then push the b%a. If a is zero, push zero.
        elif instruction == '%':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            if a != 0:
                stack.append(b % a)
            else:
                stack.append(0)

        # ! Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
        elif instruction == '!':
            try:
                if stack.pop() == 0:
                    stack.append(1)
                else:
                    stack.append(0)
            except IndexError:
                stack.append(0)

        # ` (backtick) Greater than: Pop a and b, then push 1 if b>a, otherwise push zero.
        elif instruction == '`':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            if b > a:
                stack.append(1)
            else:
                stack.append(0)

        # > Start movig right.
        # < Start moving left.
        # ^ Start moving up.
        # v Start moving down.
        # ? Start moving in a random cardinal direction.
        # _ Pop a value; move right if value = 0, left otherwise.
        # | Pop a value; move down if value = 0, up otherwise.
        elif instruction == '>':
            order = 'RIGHT'
        elif instruction == '<':
            order = 'LEFT'
        elif instruction == '^':
            order = 'UP'
        elif instruction == 'v':
            order = 'DOWN'
        elif instruction == '?':
            order = random.choice(['RIGHT', 'LEFT', 'UP', 'DOWN'])
        elif instruction == '_':
            try:
                if stack.pop() == 0:
                    order = 'RIGHT'
                else:
                    order = 'LEFT'
            except IndexError:
                order = 'LEFT'
        elif instruction == '|':
            try:
                if stack.pop() == 0:
                    order = 'DOWN'
                else:
                    order = 'UP'
            except IndexError:
                order = 'UP'

        # " Start string mode: push each character's ASCII value all the way up to the next ".
        elif instruction == '"':
            if not string_mode:
                string_mode = True

        # : Duplicate value on top of the stack. If there is nothing on top of the stack, push a 0.
        elif instruction == ':':
            try:
                value = stack[-1]
                stack.append(value)
            except IndexError:
                stack.append(0)

        # \ Swap two values on top of the stack. If there is only one value,
        # pretend there is an extra 0 on bottom of the stack.
        elif instruction == '\\':
            try:
                a = stack.pop()
            except IndexError:
                a = 0
            try:
                b = stack.pop()
            except IndexError:
                b = 0
            stack.append(a)
            stack.append(b)

        # $ Pop value from the stack and discard it.
        elif instruction == '$':
            try:
                stack.pop()
            except IndexError:
                pass

        # . Pop value and output as an integer.
        elif instruction == '.':
            try:
                output += str(stack.pop())
            except IndexError:
                pass

        # , Pop value and output the ASCII character represented by the integer code that is stored in the value.
        elif instruction == ',':
            try:
                char = stack.pop()
                output += chr(char)
            except IndexError:
                pass

        # # Trampoline: Skip next cell.
        elif instruction == '#':
            skip = True

        # p A "put" call (a way to store a value for later use). Pop y, x and v,
        # then change the character at the position (x,y) in the program to the character with ASCII value v.
        elif instruction == 'p':
            try:
                y = stack.pop()
                x = stack.pop()
                v = stack.pop()
                line_to_change = list(code[y])
                line_to_change[x] = chr(v)
                code[y] = ''.join(line_to_change)
            except IndexError:
                pass

        # g A "get" call (a way to retrieve data in storage).
        # Pop y and x, then push ASCII value of the character at that position in the program.
        elif instruction == 'g':
            try:
                y = stack.pop()
                x = stack.pop()
                stack.append(ord(code[y][x]))
            except IndexError:
                stack.append(0)

        # @ End program.
        elif instruction == '@':
            break
    return output


def test_intepreter():
    codes_and_outputs = [
        ['>987v>.v\nv456<  :\n>321 ^ _@', '123456789'],
        ['>25*"!dlroW olleH":v\n                v:,_@\n                >  ^]', 'Hello World!\n'],
        ['08>:1-:v v *_$.@\n  ^    _$>\\:^', '40320'],
        ['01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@', '01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@'],
        ['2>:3g" "-!v\\  g30          <\n |!`"&":+1_:.:03p>03g+:"&"`|\n @               ^  p3\\" ":<\n2'
         ' 2345678901234567890123456789012345678', '23571113171923293137']]
    for code, output in codes_and_outputs:
        assert interpret(code) == output
