from typing import Dict, List, Union


def find_longest_string(s: List[str]) -> int:
    return max(len(st) for st in s)


def align_text(s: str, l: int, t: str = 'center') -> str:
    ldiff = l - len(s)
    if ldiff > 0:
        if t == 'center':
            return ' '*(ldiff >> 1) + s + ' '*(ldiff >> 1) + (' ' if ldiff % 2 else '')
        elif t == 'left':
            return s + ' '*ldiff
        elif t == 'right':
            return ' '*ldiff + s
    else:
        return s


def boxed_text(s: List[str]) -> str:
    mw = find_longest_string(s)
    result = '\u250c' + '\u2500'*mw + '\u2510\n'
    for line in s:
        result += '\u2502' + line + '\u2502\n'
    return result + '\u2514' + '\u2500'*mw + '\u2518'


def display_menu(title: str, choices: Dict[str, str]) -> str:
    lines = [title] + ['{}: {}'.format(ct, dt) for ct, dt in choices.items()]
    mw = find_longest_string(lines)
    lines = [align_text(title, mw)] + [align_text(lt, mw, 'left') for lt in lines[1:]]
    prompt = boxed_text(lines)
    while True:
        print(prompt)
        c = input('Choice: ').lower()
        if c in list(map(str.lower, choices)):
            return c


def display_enumerated_menu(title: str, choices: List[str]):
    choice_dict = {}
    for ci, c in enumerate(choices):
        choice_dict[str(ci)] = c
    return int(display_menu(title, choice_dict))


def ask_yes_no(question: str) -> bool:
    while True:
        r = input('{} (y/n) '.format(question)).lower()
        if r == 'y' or r == 'yes':
            return True
        elif r == 'n' or r == 'no':
            return False
        print('Sorry, I didn\'t understand that, please try again...')


class Display:
    def __init__(self, title: str, choices: List[str]):
        self.title = title
        self.choices = choices
        self.omap = {}
        for c in self.choices:
            self.omap[c.lower()] = False

    def __getitem__(self, item):
        return self.omap[item.lower()]

    def __setitem__(self, key, value):
        if key not in self.choices:
            self.choices.append(key)
        self.omap[key.lower()] = value

    def process(self) -> Union[object, bool]:
        dchoices = {}
        for ci, c in enumerate(self.choices):
            dchoices[str(ci + 1)] = c
        c = display_menu(self.title, dchoices)
        return self.omap[dchoices[c].lower()]
