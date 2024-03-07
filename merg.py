import re

def merge_sections(output_file, *input_files):
    merged_content = {}

    for input_file in input_files:
        with open(input_file, 'r') as file:
            content = file.read()
            sections = re.split(r'^###\s', content, flags=re.MULTILINE)[1:]

            for section in sections:
                header, *section_content_lines = section.split('\n', 1)
                header = header.strip()
                section_content = '\n'.join(section_content_lines).strip()

                if header not in merged_content:
                    merged_content[header] = []

                # Usuń niepotrzebne białe znaki i dodaj paragraf do listy nienumerowanej
                cleaned_content = re.sub(r'\s+', ' ', section_content)
                cleaned_content = cleaned_content.replace('\n', ' ')

                if cleaned_content:  # Dodaj do listy tylko jeśli treść nie jest pusta
                    merged_content[header].append(f"- {cleaned_content}")

    with open(output_file, 'w') as file:
        for header, section_contents in merged_content.items():
            file.write(f"### {header}\n")
            file.write('\n'.join(section_contents))
            file.write('\n\n')


if __name__ == "__main__":
    output_filename = "merged_sections.md"
    input_filenames = ["test.md", "test11.md", "test111.md"]  # Dodaj wszystkie pliki Markdown tutaj

    merge_sections(output_filename, *input_filenames)
    print(f"Sekcje połączone i zapisane w {output_filename}.")
