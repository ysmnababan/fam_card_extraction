import io
from google.cloud import vision
import re
import json
import os

first_keywords = ["Dikeluarkan", "NIP.", "Kepala", "Dinas", "PLT"]
last_keywords = ["NIP"]

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

def group_words_into_lines(words_with_positions, y_threshold=20):
    """
    Groups words into lines based on their vertical (y) positions.
    Each line includes a representative y-coordinate and a list of (text, x) tuples.
    """
    # Step 1: Sort all words by their y position (top to bottom)
    words_with_positions.sort(key=lambda w: w[2])  # (text, x, y)

    lines = []

    for word, x, y in words_with_positions:
        placed = False
        for line in lines:
            if abs(line['y'] - y) <= y_threshold:
                line['words'].append((word, x))
                placed = True
                break
        if not placed:
            # New line
            lines.append({'y': y, 'words': [(word, x)]})

    # Step 2: Sort words within each line by x (left to right)
    for line in lines:
        line['words'].sort(key=lambda w: w[1])

    # Step 3: Sort lines by y again, just in case
    lines.sort(key=lambda l: l['y'])

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
        words = line['words']
        # Sort words left to right
        words.sort(key=lambda w: w[1])

        output_line = ''
        last_x = None
        for word, x in words:
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
                last_x = x + len(word) * 10  # Estimate next x position
        result += prefix_keywords_with_hash(output_line) + '\n'
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

def save_to_json(data, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}

    # Add only new keys (don't overwrite existing keys)
    for key, value in data.items():
        existing_data[key] = value

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def find_line_above(lines, keyword, x_proximity_tolerance=100, y_threshold=200):
    keyword_line = None
    keyword_x = None
    keyword_y = None

    # Step 1: Locate the keyword and record its x and y position
    for i, line in enumerate(lines):
        print(f"Checking line {i}: {line}")  # Debugging
        for word in line['words']:
            if isinstance(word, tuple) and len(word) == 2:
                word_text, x = word
                print(f"Checking word: {word_text} at x position: {x}")
                if keyword.lower() in word_text.lower():
                    keyword_line = line
                    keyword_x = x
                    keyword_y = line['y']  # Y of the line containing the keyword
                    print(f"Keyword '{keyword}' found in line {i}: {line}")
                    break
        if keyword_line:
            keyword_index = i
            break

    if not keyword_line:
        print("Keyword not found in any line.")
        return None

    print(f"Keyword line found at y position: {keyword_y}")

    # Step 2: Search upward for the nearest valid line within y_threshold
    for i in range(keyword_index - 1, -1, -1):
        line = lines[i]
        line_y = line['y']
        print(f"Checking line above {i}: {line}")
        y_difference = abs(line_y - keyword_y)

        if y_difference > y_threshold:
            print(f"Line {i} is too far away (y-difference: {y_difference})")
            continue

        # Step 3: Filter words that are within x_proximity_tolerance of the keyword_x
        filtered_words = [
            (text, x) for text, x in line['words']
            if x >= keyword_x - x_proximity_tolerance
        ]

        # Sort by x position just in case
        filtered_words.sort(key=lambda w: w[1])

        # Step 4: Extract officer name
        officer_name = ' '.join([text for text, _ in filtered_words])
        print(f"Officer name found: {officer_name}")
        return officer_name

    print("No valid officer name found.")
    return None

def clean_officer_name(name):
    # Remove the ' / ' and any surrounding spaces
    cleaned_name = re.sub(r'\s*/\s*', '', name)
    return cleaned_name

def split_lines_into_columns(lines, num_columns=3):
    # Step 1: Find the maximum x position from all words
    all_x_positions = [x for line in lines for _, x in line['words']]
    if not all_x_positions:
        return {'left': [], 'center': [], 'right': []}

    max_x = max(all_x_positions)
    column_width = max_x / num_columns

    # Initialize column containers
    columns = {
        'left': [],
        'center': [],
        'right': []
    }

    for line in lines:
        left_words = []
        center_words = []
        right_words = []

        for word, x in line['words']:
            if x < column_width:
                left_words.append((word, x))
            elif x < 2 * column_width:
                center_words.append((word, x))
            else:
                right_words.append((word, x))

        if left_words:
            columns['left'].append({'y': line['y'], 'words': left_words})
        if center_words:
            columns['center'].append({'y': line['y'], 'words': center_words})
        if right_words:
            columns['right'].append({'y': line['y'], 'words': right_words})

    return columns

def extract_date_from_lines(lines):
    date_pattern = re.compile(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{4})\b')

    for line in lines:
        for word, _ in line['words']:
            match = date_pattern.search(word)
            if match:
                # Format to consistent dd-mm-yyyy
                day, month, year = match.groups()
                return f'{int(day):02d}-{int(month):02d}-{year}'
    return None

def execute(image_path, output_path):
    words = get_words_with_positions(image_path)
    lines = group_words_into_lines(words)
    r_text = reconstructed_text(lines)
    extracted_val = extract_values(r_text)
    columns = split_lines_into_columns(lines)
    date = extract_date_from_lines(columns['left'])
    officer_name = find_line_above(columns['right'], "NIP")
    if officer_name:
        extracted_val["officer_name"] = clean_officer_name(officer_name)
    if date:
        extracted_val["tanggal"] = date
    print("\nFOOTER RESULT: \n")
    print(extracted_val)

    save_to_json(extracted_val,output_path)