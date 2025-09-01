# https://www.lexilogos.com/keyboard/greek_ancient.htm

# TODO: complete "i:": "ϊ",

import curses
import sys
import os
from curses import wrapper


class GreekKeyboard:

    latin_to_greek_substrings = {
        "a": "α",
        "a=": "ᾳ",
        "a&": "ᾶ",
        "a'": "ά",
        "a''": "ὰ",
        "a'''": "ᾰ",
        "a''''": "ᾱ",
        "ha": "ἁ",
        "ha'": "ἅ",
        "ha''": "ἃ",
        "hha": "ἀ",
        "hha'": "ἄ",
        "hha''": "ἂ",

        "e": "ε",
        "e'": "έ",
        "e''": "ὲ",
        "he": "ἑ",
        "he'": "ἕ",
        "he''": "ἓ",
        "hhe": "ἐ",
        "hhe'": "ἔ",
        "hhe''": "ἒ",

        "i": "ι",
        "i&": "ῖ",
        "i'": "ί",
        "i''": "ὶ",
        "i'''": "ῐ",
        "i''''": "ῑ",
        "hi": "ἱ",
        "hi'": "ἵ",
        "hi''": "ἳ",
        "hhi": "ἰ",
        "hhi'": "ἴ",
        "hhi''": "ἲ",
        "i:": "ϊ",

        "j": "η",
        "j=": "ῃ",
        "j&": "ῆ",
        "j'": "ή",
        "j''": "ὴ",
        "j''''": "ή",
        "hj": "ἡ",
        "hj'": "ἥ",
        "hj''": "ἣ",
        "hhj": "ἠ",
        "hhj'": "ἤ",
        "hhj''": "ἢ",

        "o": "ο",
        "o'": "ό",
        "o''": "ὸ",
        "ho": "ὁ",
        "ho'": "ὅ",
        "ho''": "ὃ",
        "hho": "ὀ",
        "hho'": "ὄ",
        "hho''": "ὂ",

        "w": "ω",
        "w=": "ῳ",
        "w&": "ῶ",
        "w'": "ώ",
        "w''": "ὼ",
        "hw": "ὡ",
        "hw'": "ὥ",
        "hw''": "ὣ",
        "hhw": "ὠ",
        "hhw'": "ὤ",
        "hhw''": "ὢ",

        "u": "υ",
        "u&": "ῦ",
        "u'": "ύ",
        "u''": "ὺ",
        "u'''": "ῠ",
        "u''''": "ῡ",
        "hu": "ὑ",
        "hu'": "ὕ",
        "hu''": "ὓ",
        "hhu": "ὐ",
        "hhu'": "ὔ",
        "hhu''": "ὒ",
        "u:": "ϋ",

        "y": "υ",
        "y&": "ῦ",
        "y'": "ύ",
        "y''": "ὺ",
        "y'''": "ῠ",
        "y''''": "ῡ",
        "hy": "ὑ",
        "hy'": "ὕ",
        "hy''": "ὓ",
        "hhy": "ὐ",
        "hhy'": "ὔ",
        "hhy''": "ὒ",
        "y:": "ϋ",

        "b": "β",
        "b=": "ϐ",
        "g": "γ",
        "d": "δ",
        "z": "ζ",
        "th": "θ",
        "k": "κ",
        "k=": "ϰ",
        "l": "λ",
        "m": "μ",
        "n": "ν",
        "ks": "ξ",
        "cs": "ξ",
        "p": "π",
        "r": "ρ",
        "rh": "ῥ",
        "rhh": "ῤ",
        "s": "σ",
        "s ": "ς ",
        "t": "τ",
        "ph": "φ",
        "f=": "ϕ",
        "kh": "χ",
        "ch": "χ",
        "ps": "ψ",
        "c": "ϲ",

        ";": "·",
        "?": ";",
    }

    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        self.latin_to_greek_mappings = {}
        self.max_len_latin_to_greek_mappings = 0
        for latin, greek in self.latin_to_greek_substrings.items():
            latin_len = len(latin)
            if latin_len > self.max_len_latin_to_greek_mappings:
                self.max_len_latin_to_greek_mappings = latin_len
            if latin_len in self.latin_to_greek_mappings:
                self.latin_to_greek_mappings[latin_len][latin] = greek
                self.latin_to_greek_mappings[latin_len][latin.upper()] = greek.upper()
            else:
                self.latin_to_greek_mappings[latin_len] = {}
                self.latin_to_greek_mappings[latin_len][latin] = greek
                self.latin_to_greek_mappings[latin_len][latin.upper()] = greek.upper()

    def convert(self, substring: str) -> str:
        substring_length = len(substring)
        index = 0
        output_string = ''
        escape_mode = False
        while index < substring_length:
            if substring[index] == "\\":
                escape_mode = not escape_mode
                index += 1
                continue
            if escape_mode:
                for local_len in range(self.max_len_latin_to_greek_mappings, 0, -1):
                    try:
                        local_substring = substring[index:index + local_len]
                        mapping = self.latin_to_greek_mappings[local_len][local_substring]
                        output_string += mapping
                        index += local_len
                        break
                    except IndexError:
                        continue
                    except KeyError:
                        continue
                else:
                    output_string += substring[index]
                    index += 1
            else:
                output_string += substring[index]
                index += 1
        return output_string

    def converter(self, stdscr: curses.window):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        input_string = ''
        output_string = ''
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, 'Enter string', curses.A_STANDOUT)
            stdscr.addstr(2, 0, output_string, curses.color_pair(2))
            stdscr.addstr(4, 0, input_string, curses.color_pair(1))
            stdscr.refresh()
            key = stdscr.getch()
            if key == 27:
                return
            if key in (10, 13):
                with open(self.file_path, 'a') as f:
                    f.write(output_string + '\n')
                input_string = ''
                output_string = ''
            elif key in (curses.KEY_BACKSPACE, 127):
                if input_string != '':
                    input_string = input_string[:-1]
                output_string = self.convert(input_string)
            else:
                input_string += chr(key)
                output_string = self.convert(input_string)


if __name__ == '__main__':
    file_path = sys.argv[1]
    keyboard = GreekKeyboard(file_path)
    print(keyboard.convert("ajuysws "))
    print(keyboard.convert("a'juysws"))
    print(keyboard.convert("a''juysws"))
    print(keyboard.convert("a'''juysws"))
    print(keyboard.convert("a''''juysws"))
    print(keyboard.convert("a=a''a&i:y:"))
    wrapper(keyboard.converter)
