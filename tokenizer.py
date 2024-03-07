#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль призначено для синтаксичного розбору виразу по частинах.

Вираз може мати вигляд:
(abc + 123.5)*d2-3/(x+y)
Вираз може містити:
    - змінні - ідентифікатори
    - константи - дійсні або цілі числа без знаку
    - знаки операцій: +, -, *, /
    - дужки: (, )

Функція `get_tokens` за заданим виразом має повертати послідовність
лексем -- токенів.

Кожний токен (див. class Token) -- це пара: (<тип токену>, <значення токену>)
"""

# типи токенів
TOKEN_TYPE = (
    "variable",
    "constant",
    "operation",
    "equal",
    "left_paren",
    "right_paren",
    "other",
)

# словник фіксованих токенів, що складаються з одного символа
TOKEN_TYPES = {
    "+": "operation",
    "-": "operation",
    "*": "operation",
    "/": "operation",
    "(": "left_paren",
    ")": "right_paren",
    "=": "equal",
}


class Token:

    def __init__(self, type, value):
        assert type in TOKEN_TYPE, 'недопустимий тип токена'
        self.type = type
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return self.type == __value.type and self.value == __value.value

    def __repr__(self):
        return f"Token(type='{self.type}', value='{self.value}')"


def get_tokens(string):
    """Функція за рядком повертає список токенів типу Token.

    :param string: рядок
    :return: список токенів
    """
    tokens = []
    while string:
        token, string = _get_next_token(string)
        if token:
            tokens.append(token)
    return tokens


def _get_next_token(string):
    """Функція повертає наступний токен та залишок рядка.

    :param string: рядок
    :return:
        next_token: наступний токен, якщо є, або None
        string: залишок рядка
    """
    for func in [
        _get_left_paren,
        _get_right_paren,
        _get_operator,
        _get_equal,
        _get_constant,
        _get_variable,
        _get_other
        ]:
            res = func(string)
            if res is not None:
                return res


def _get_left_paren(string):
    """Функція за рядком повертає ліву дужку (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: дужка типу Token('left_paren', '(')
        string: залишок рядка
    """
    if string[0] == "(":
        string = string[1:]
        return Token('left_paren', '('), string
    else:
        pass


def _get_right_paren(string):
    """Функція за рядком повертає праву дужку (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: дужка типу Token('right_paren', '(')
        string: залишок рядка
    """
    if string[0] == ")":
        string = string[1:]
        return Token('right_paren', ')'), string
    else:
        pass


def _get_operator(string):
    """Функція за рядком повертає оператор (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: оператор типу Token('operation', ...)
        string: залишок рядка
    """
    if string[0] == '+':
        string = string[1:]
        return Token('operation', '+'), string
    elif string[0] == '-':
        string = string[1:]
        return Token('operation', '-'), string
    elif string[0] == '*':
        string = string[1:]
        return Token('operation', '*'), string
    elif string[0] == '/':
        string = string[1:]
        return Token('operation', '/'), string
    else:
        pass


def _get_equal(string):
    """Функція за рядком повертає присвоєння '=' (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: оператор типу Token('equal', ...)
        string: залишок рядка
    """
    if string[0] == '=':
        string = string[1:]
        return Token('equal', '='), string
    else:
        pass


def _get_constant(string):
    """Функція за рядком повертає константу (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: константа типу Token('constant', ...) або None
        string: залишок рядка
    """
    if string[0].isdigit():
        i = 0
        point_count = 0
        while i < len(string):
            if string[i].isdigit():
                i += 1
            elif string[i] == '.' and point_count < 1:
                point_count += 1
                i += 1
            else:
                break
        return Token('constant', string[0:i]), string[i:]
    else:
        pass

def _get_variable(string):
    """Функція за рядком повертає змінну (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: змінна типу Token('constant', ...) або None
        string: залишок рядка
    """
    if string[0].isidentifier():
        i = 0
        while i < len(string):
            if string[i].isidentifier() or string[i].isdigit():
                i += 1
            else:
                break
        return Token('variable', string[0:i]), string[i:]
    else:
        pass

def _get_other(string):
    """Функція за рядком повертає об'єкт типу other (якщо є) та залишок рядка.

    :param string: рядок
    :return:
        next_token: константа типу Token('other', ...) або None
        string: залишок рядка
    """
    if string[0] == " ":
        string = string[1:]
        return None, string
    elif string[0] in "+-*/=()" or string[0].isdigit() or string[0].isidentifier():
        return None, string
    else:
        i = 0
        while i < len(string) and string[i] not in "+-*/=() " and not string[i].isdigit() and not string[i].isidentifier():
            i += 1
        else:
            return Token('other', string[0:i]), string[i:]


if __name__ == "__main__":

    needed = [
        Token(type='left_paren', value='('),
        Token(type='left_paren', value='('),
        Token(type='left_paren', value='('),
        Token(type='variable', value='ab1_'),
        Token(type='operation', value='-'),
        Token(type='constant', value='345.56'),
        Token(type='right_paren', value=')'),
        Token(type='left_paren', value='('),
        Token(type='operation', value='*'),
        Token(type='operation', value='/'),
        Token(type='other', value='.'),
        Token(type='constant', value='2'),
        Token(type='other', value='{'),
        Token(type='variable', value='_cde23')
    ]

    success = (x := get_tokens("(((ab1_ - 345.56)(*/.2{_cde23")) == needed
    if not success:
        if len(x) != len(needed):
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x):
            if exp != real:
                print(f'Expected: {exp}, got {real}')

    needed = [
        Token(type='variable', value='x'),
        Token(type='equal', value='='),
        Token(type='left_paren', value='('),
        Token(type='variable', value='a'),
        Token(type='operation', value='+'),
        Token(type='variable', value='b'),
        Token(type='right_paren', value=')')
    ]

    success = success and (x := get_tokens("x = (a + b)")) == needed
    if not success:
        if len(x) != len(needed):
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x):
            if exp != real:
                print(f'Expected: {exp}, got {real}')

    needed = [
        Token(type='variable', value='x'),
        Token(type='equal', value='='),
        Token(type='left_paren', value='('),
        Token(type='variable', value='_a_s12'),
        Token(type='operation', value='+'),
        Token(type='constant', value='12.12321'),
        Token(type='right_paren', value=')'),
        Token(type='operation', value='*'),
        Token(type='left_paren', value='('),
        Token(type='constant', value='123'),
        Token(type='variable', value='_asd'),
        Token(type='other', value='.'),
        Token(type='operation', value='-'),
        Token(type='constant', value='3.'),
        Token(type='right_paren', value=')'),
    ]

    success = success and (x := get_tokens("x = (_a_s12 + 12.12321)*(123 _asd. - 3.)")) == needed
    if not success:
        if len(x) != len(needed):
            print(f'wrong amount of tokens. Expected: {len(needed)}, got: {len(x)}')
        for exp, real in zip(needed, x):
            if exp != real:
                print(f'Expected: {exp}, got {real}')

    print("Success =", success)