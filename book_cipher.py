#GLOBAL VARIABLES
import json
import os

HOW_MANY_BOOK = 3
LINE = 128
PAGE = 64
pages = {}
page_number=0
line_window = {}
line_number = 0
char_window = []

def clean_line(line):
    return line.strip().replace('-', '') + ' ' #space instead of newline

def process_books(*paths):
    for path in paths:
        read_book(path)
        print(pages[len(pages)])

def read_book(file_path):
    global char_window
    with open(file_path, 'r', encoding='utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)
    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()

def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def add_line():
    global char_window, line_number
    line_number += 1
    process_page(''.join(char_window), line_number)
    char_window.clear()

def process_page(line, line_num):
    global line_window, pages, page_number
    line_window[line_num] = line
    if len(line_window) == PAGE:
        add_page()

def add_page():
    global line_number, line_window, pages, page_number
    page_number += 1
    pages[page_number] = dict(line_window)
    line_window.clear()
    line_number = 0

def generate_code_book():
    global pages
    code_book = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book

def save(file_path, book):
    with open(file_path, 'w') as fp:
        #json.dump(book, fp, indent=4)
        json.dump(book, fp)

def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save(file_path, pages)
            return pages
        else:
            code_book = generate_code_book()
            save(file_path, code_book)
            return code_book
'''
process_books('./books/huck_finn.txt', './books/mysterious.txt', './books/outlaw.txt')
cb = generate_code_book()
print(cb['t'])
save('./code_books/book1.json', cb)
'''
cb = load('./code_books/book1.json')