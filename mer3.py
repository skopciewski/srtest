import markdown_it
from bs4 import BeautifulSoup, Comment
import sys
import os
import re

def list_md_files(directory):
    try:
        # Sprawdź, czy katalog istnieje
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Katalog '{directory}' nie istnieje.")

        # Uzyskaj listę plików w danym katalogu z rozszerzeniem .md
        md_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.md')]

        # Sprawdź, czy znaleziono pliki .md
        if md_files:
            return md_files
        else:
            raise ValueError(f"Brak plików .md w katalogu '{directory}'.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        sys.exit(1)


def find_bump(md_files):
    bumps = ["major", "minor", "patch"]
    parsed_bump = "patch"

    for md_file in md_files:
        # Wczytaj plik Markdown
        with open(md_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # Utwórz obiekt MarkdownIt
        md = markdown_it.MarkdownIt()

        # Skonwertuj Markdown na HTML
        html_content = md.render(markdown_content)

        # Stwórz obiekt BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        comment = soup.find(string=lambda text: isinstance(text, Comment))
        pattern = re.compile(r'- bump: (\w+)')
        match = pattern.findall(comment)
        try:
            index = bumps.index(match[0])
            current_index = bumps.index(parsed_bump)
            if index < current_index:
                parsed_bump = match[0]
        except ValueError:
            print(f'Invalid bump: {match}')

    return parsed_bump

def find_sections(md_files):
    sections = ['Notice', 'Added', 'Changed', 'Removed', 'Fixed']
    parsed_data = dict()

    for md_file in md_files:
        # Wczytaj plik Markdown
        with open(md_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # Utwórz obiekt MarkdownIt
        md = markdown_it.MarkdownIt()

        # Skonwertuj Markdown na HTML
        html_content = md.render(markdown_content)

        # Stwórz obiekt BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        for section in sections:
            if section not in parsed_data:
                parsed_data[section] = []

            selected_header = soup.find('h3', string=section)

            if selected_header is not None:
                current_element = selected_header.find_next()
                while current_element and current_element.name != 'h3':
                    if (current_element.name == 'p' or current_element.name == "li") and not current_element.find_all():
                        parsed_data[section].append(current_element)

                    current_element = current_element.find_next()

    return parsed_data

def write_merged_file(parsed_data, output_file):
    with open(output_file, 'w+', encoding='utf-8') as existing_file:
        for section, paragraphs in parsed_data.items():
            if section == "Notice":
                if paragraphs:
                    for p in paragraphs:
                        existing_file.write(f"{p.text}\n\n")
            else:
                if paragraphs:
                    existing_file.write(f"### {section}\n\n")
                    for p in paragraphs:
                        existing_file.write(f"- {p.text}\n")
                    existing_file.write("\n")

def write_bump_file(bump, output_file):
    with open(output_file, 'w+', encoding='utf-8') as existing_file:
        existing_file.write(f"{bump}")

def remove_old_files(md_files):
    for md_file in md_files:
        os.remove(md_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Użycie: python script.py <md_dir> output.md bump.txt")
    else:
        directory_name = sys.argv[1]
        md_files = list_md_files(directory_name)
        data = find_sections(md_files)
        output_file = sys.argv[2]
        write_merged_file(data, output_file)
        bump_file = sys.argv[3]
        bump = find_bump(md_files)
        write_bump_file(bump, bump_file)
        remove_old_files(md_files)

