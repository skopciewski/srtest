import re
import yaml
import json
import sys

def extract_yaml_front_matter_and_sections(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Użyj wyrażenia regularnego do ekstrakcji fragmentu YAML front matter
        match = re.search(r'---\n(.*?\n)---', content, re.DOTALL)
        if match:
            yaml_data = match.group(1)
            try:
                data = yaml.safe_load(yaml_data)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML: {e}")
                return None
        else:
            print("Error: YAML front matter not found in the file.")
            return None

        # Użyj wyrażenia regularnego do wyszukiwania sekcji
        section_matches = re.finditer(r'###\s+(.*?)\n(.*?)(?=(?:###|\Z))', content, re.DOTALL)
        sections = [{"header": match.group(1), "content": match.group(2)} for match in section_matches]

        if not data:
            data = {}
        data["sections"] = sections

        return data

def main():
    if len(sys.argv) != 2:
        print("Usage: python parser.py <path_to_unreleased_file>")
        sys.exit(1)

    unreleased_file_path = sys.argv[1]

    parsed_data = extract_yaml_front_matter_and_sections(unreleased_file_path)
    if parsed_data:
        print(json.dumps(parsed_data, indent=2))

if __name__ == "__main__":
    main()

