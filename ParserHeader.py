import io
from google.cloud import vision
import re
import json
import os

first_keywords = ["No","Nama", "Kecamatan", "Alamat", "Kabupaten", "RT", "Kode", "Desa", "Provinsi","www","wwww","wwwww","REPUBLIK","BHINNEKA"]
last_keywords = ["No", "Keluarga", "Kecamatan", "Alamat", "Kota", "RW", "Pos", "Kelurahan", "Provinsi"]
def get_words_with_positions(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)

    words = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    bounding_box = word.bounding_box
                    # Use average of y for the word position
                    avg_y = sum(vertex.y for vertex in bounding_box.vertices) / 4
                    avg_x = sum(vertex.x for vertex in bounding_box.vertices) / 4
                    words.append((word_text, avg_x, avg_y))
    return words

def group_words_into_lines(words, y_threshold=20):
    # First, sort by y
    words.sort(key=lambda w: w[2])

    lines = []
    current_line = []
    last_y = None

    for word, x, y in words:
        if last_y is None:
            current_line.append((word, x))
            last_y = y
        elif abs(y - last_y) <= y_threshold:
            current_line.append((word, x))
            last_y = (last_y + y) / 2  # smooth the y a bit
        else:
            lines.append(current_line)
            current_line = [(word, x)]
            last_y = y
    if current_line:
        lines.append(current_line)
    return lines

def prefix_keywords_with_hash(text):
    for keyword in first_keywords:
        # Allow underscores between letters and match case-insensitively
        pattern = r'(?<!#)(?:_*)'.join(list(keyword))
        regex = re.compile(rf'(?<!#){pattern}', re.IGNORECASE)
        text = regex.sub(lambda m: '#' + m.group(), text)

    return text

def reconstructed_text(lines, space_threshold=100):
    result = ""
    for line in lines:
        # Sort words left to right
        line.sort(key=lambda w: w[1])

        output_line = ''
        last_x = None
        for word, x in line:
            if last_x is None:
                output_line += word
                last_x = x
            else:
                gap = x - last_x
                num_spaces = int(gap / space_threshold)
                if num_spaces > 0:
                    output_line += '_' * num_spaces
                else:
                    output_line += '_'
                output_line += word
                last_x = x + len(word) * 10  # Estimate next position
        result+= prefix_keywords_with_hash(output_line)
        # print(prefix_keywords_with_hash(output_line))
    print(result)
    return result

def extract_values(text):
    result = {}

    for keyword in last_keywords:
        # Match keyword, optional underscores/spaces, optional colon, then capture until #, newline, or end of text
        pattern = re.compile(rf'{keyword}[\s_]*:?([\s\S]*?)(?=#|\n|$)', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            value = matches[-1]  # Take the last match, assuming it's the most relevant one
            cleaned = re.sub(r'\s+', ' ', value.replace(':', '').replace('_', ' ')).strip()
            result[keyword.lower()] = cleaned

    return result

def extract_16_digit_number(text):
    """
    Extracts the first 16-digit number from the input text.

    Args:
        text (str): The input text to search in.

    Returns:
        str or None: The 16-digit number if found, else None.
    """
    match = re.search(r'(?<!\d)(\d{16})(?!\d)', text)
    return match.group(1) if match else ""

def save_to_json(data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # Add only new keys (don't overwrite existing keys)
    for key, value in data.items():
        # if key not in existing_data:
        existing_data[key] = value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def execute(image_path, output_path):
    words = get_words_with_positions(image_path)
    lines = group_words_into_lines(words)
    r_text = reconstructed_text(lines)
    extracted_val = extract_values(r_text)
    no = extract_16_digit_number(r_text)
    if not no == "" :
        print(no)
        extracted_val["no"] = no
    save_to_json(extracted_val,output_path)