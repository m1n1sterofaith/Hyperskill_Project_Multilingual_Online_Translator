import requests
import argparse
from bs4 import BeautifulSoup
from http import HTTPStatus

def write_translation_to_file(lang, trans_word, example, trans_phrase, file_path):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{lang} Translations:\n")
            file.write(f"{trans_word}\n")
            file.write(f"{lang} Example:\n")
            file.write(f"{example}\n")
            file.write(f"{trans_phrase}\n\n")
        file.close()
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def lookup_word(lang1, lang2, word, translation):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://context.reverso.net/translation/' + translation + '/' + word

    r = requests.get(url, headers=headers)

    if r.status_code == 404:
        print(f'Sorry, unable to find {word}')
        exit()

    if r.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(r.content, 'html.parser')

        trans_list = [x.get_text().strip() for x in soup.find_all("span", class_=lambda x: x and 'display-term' in x)]
        print(lang1, lang2, word, sep=' ')
        print(trans_list)
        translated_word = trans_list[0]


        from_usage_text = [x.get_text().strip() for x in soup.find_all("div", class_=lambda x: x and 'src' in x)]
        to_usage_text = [x.get_text().strip() for x in soup.find_all("div", class_=lambda x: x and 'trg' in x)]

        example_text = from_usage_text[0]
        translated_text = to_usage_text[0]
        print(example_text)
        print(translated_text)

        return translated_word,example_text, translated_text

    else:
        print('Something wrong with your internet connection')
        exit()

language_list = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
                 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']

parser = argparse.ArgumentParser()
parser.add_argument("from_language",
                    help="The language of the word that you want to translate",
                    default='English')
parser.add_argument("to_language",
                    help="The language in which you want the word to be translated",)
parser.add_argument("word",
                    help="The word that you want to translate")
args = parser.parse_args()


file_path = f'{args.word}.txt'

if args.to_language != 'all':
    try:
        from_lang = language_list.index(args.from_language)
    except ValueError:
        try:
            from_lang = language_list.index(args.from_language.lower())
        except ValueError:
            print(f"Sorry, the program doesn't support {args.from_language}")
            exit()
    try:
        to_lang = language_list.index(args.to_language)
    except ValueError:
        try:
            to_lang = language_list.index(args.to_language.lower())
        except ValueError:
            print(f"Sorry, the program doesn't support {args.to_language}")
            exit()

    translation = args.from_language.lower() + '-' + args.to_language.lower()
    trans_word, example, trans_phrase = lookup_word(args.from_language, args.to_language, args.word, translation)
    write_translation_to_file(args.to_language, trans_word, example, trans_phrase, file_path)
    print(trans_word, example, trans_phrase, sep='\n\n')

else:
    for i in range(0, len(language_list)):
        if language_list[i] == args.from_language:
            i += 1
            continue
        translation = args.from_language.lower() + '-' + language_list[i].lower()
        trans_word, example, trans_phrase = lookup_word(args.from_language, args.to_language, args.word, translation)
        write_translation_to_file(language_list[i], trans_word, example, trans_phrase, file_path)
        i += 1

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        print(line, end='')
