from markdown_it import MarkdownIt

def parse_markdown(input_file, output_file):
    md = MarkdownIt()

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = content.split('### Head1')[1:]

    output_content = ""

    for section in sections:
        section = section.strip()
        if section:
            tokens = md.parse(section)

            head_text = None
            paragraph_text = ""

            for token in tokens:
                print(token)
                if token.as_dict()['type'] == 'heading_open':
                    head_text = tokens[tokens.index(token) + 1].as_dict()['content'].strip()
                elif token.as_dict()['type'] == 'paragraph_open':
                    paragraph_text = tokens[tokens.index(token) + 1].as_dict()['content'].strip()

            if head_text is not None and paragraph_text:
                output_content += f"### Head1 {head_text}\n\n{paragraph_text}\n\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)

if __name__ == "__main__":
    input_file = "input.md"
    output_file = "output.md"
    parse_markdown(input_file, output_file)

