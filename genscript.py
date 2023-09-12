import json
import regex as re
import random

# Setup request file path here
file_path = r'C:\Users\peat2\kbtg\test_json.txt'

# Function to save file as file_name and fufill content inside text file
def save_to_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

# Function to random the t[100000-999999] for reality
def generate_random_t1_inf():
    return f"t{random.randint(100000, 999999):6}.inf"

# Function to format JSON into expect result
def format_json(json_input):
    # JSON format
    formatted_json = json.dumps(json_input, indent=0, ensure_ascii=False)
    # Replace the tabs with spaces to remove tabbing
    formatted_json = formatted_json.replace('\t', '')
    # Add \r\n to eol before newline
    formatted_json = formatted_json.replace('\n', '\\r\\n\n')
    # Escape double quotes
    formatted_json = formatted_json.replace('"', r'\"')
    # Add double quotes to first and last except the first line
    lines = formatted_json.splitlines()

    formatted_json = lines[0] + '"\n'
    formatted_json += '\n'.join(f'\t"{line}"' for line in lines[2:])

    return formatted_json

# Function to edit the JSON request from input into LRE web_rest command
def edit_request_with_input(url, json_input, headers):
    # Format the JSON input with proper indentation
    formatted_json = format_json(json_input)

    # Generate random t1.inf
    t_inf = generate_random_t1_inf()

    request_string = (f'web_rest("POST: {url}",\n'
                        f'\t"URL={url}",\n'
                        f'\t"Method=POST",\n'
                        f'\t"EncType=raw",\n'
                        f'\t"Snapshot={t_inf}",\n'
                        f'\t"Body={formatted_json},\n'
                        f'\tHEADERS,\n'
                        f'\t{headers}')

    return request_string

# Function to find json request in .txt file
def find_json_in_txt_file(file_path):
    json_strings = []

    with open(file_path, 'r') as file:
        text = file.read()

        # Regex to find JSON objects
        json_pattern = r'\{(?:[^{}]|(?R))*\}'

        matches = re.findall(json_pattern, text, flags=re.DOTALL)

        json_strings.extend(matches)

    return json_strings

# Default part
if __name__ == "__main__":
    json_strings = find_json_in_txt_file(file_path)

    for i, json_str in enumerate(json_strings):
        # Input url
        input_url = input(f"Input request url {i + 1}: ")
        # input_url = "InTesting"

        # Escape double quotes in the JSON input
        # input_json = escape_quotes(input_json)

        # Remove newline at the end of JSON input
        # input_json = input_json.rstrip()

        # Format the JSON input with proper indentation
        try:
            paresd_json = json.loads(json_str)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format. Please provide valid JSON input.")
            continue
        input_headers = '''"Name=Content-Type", "Value=application/json", ENDHEADER,\n\tLAST);'''
        updated_request_string = edit_request_with_input(input_url, paresd_json, input_headers)

        if updated_request_string:
            save_to_file(f"output_{i + 1}.txt", updated_request_string)
            print(f"Request for JSON {i + 1} has been saved to 'output_{i + 1}.txt'.")
