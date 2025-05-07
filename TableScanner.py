from google.cloud import vision
import io

class TableScanner:
    def filter_number_lines(self, lines):
        start_idx = None
        for idx, line in enumerate(lines):
            if '(' in line and ')' in line:
                start_idx = idx + 1  # skip the () line itself
                break

        if start_idx is not None:
            return lines[start_idx:]
        else:
            return []  # no valid data found
    
    def detect_single_image(self, image_path):
        client = vision.ImageAnnotatorClient()
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(response.error.message)

        # Collect lines with their Y center
        lines = []

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    words = []
                    ys = []

                    for word in paragraph.words:
                        text = ''.join([symbol.text for symbol in word.symbols])
                        words.append(text)

                        # Compute Y center
                        vertices = word.bounding_box.vertices
                        y_center = sum(v.y for v in vertices) / 4
                        ys.append(y_center)

                    line_text = ' '.join(words)
                    avg_y = sum(ys) / len(ys) if ys else 0
                    lines.append((avg_y, line_text))

        # Sort by Y position (top to bottom)
        lines.sort(key=lambda x: x[0])

        # Merge lines with similar Y position
        merged_lines = []
        threshold = 10  # tune this threshold if needed
        current_y = None
        current_line = ''

        for y, text in lines:
            if current_y is None:
                current_y = y
                current_line = text
            elif abs(y - current_y) <= threshold:
                current_line += ' ' + text
            else:
                merged_lines.append(current_line.strip())
                current_line = text
                current_y = y

        if current_line:
            merged_lines.append(current_line.strip())

        return self.filter_number_lines(merged_lines)
    
    def extract_document_text_from_image(self, image_path):
        """Extract structured text and bounding boxes from an image using Google Vision API."""
        client = vision.ImageAnnotatorClient()
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(f"Error occurred: {response.error.message}")

        return response.full_text_annotation, response.text_annotations
    
    def get_key_value_using_position(self, extracted_text, text_annotations, key):
        """Extract the value of the given key by finding the key's position and searching for its right-side value."""
        # Extract the key's bounding box and the overall text layout
        blocks = extracted_text.pages[0].blocks

        # Find the key's position (bounding box)
        key_position = None
        value = "Key not found"

        # Look for the key's bounding box in the text annotations
        for annotation in text_annotations:
            if key.lower() in annotation.description.lower():
                key_position = annotation.bounding_poly
                break

        if key_position:
            # Extract the X and Y coordinates of the key's bounding box
            key_x_max = key_position.vertices[2].x  # X coordinate of the rightmost point
            key_y_min = key_position.vertices[0].y  # Y coordinate of the topmost point
            key_y_max = key_position.vertices[2].y  # Y coordinate of the bottommost point

            closest_value = None
            min_distance = float('inf')

            # Iterate over the blocks of text to find the nearest one to the right of the key
            for block in blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_description = ''.join([symbol.text for symbol in word.symbols])
                        word_x_min = word.bounding_box.vertices[0].x
                        word_y_min = word.bounding_box.vertices[0].y
                        word_x_max = word.bounding_box.vertices[2].x
                        word_y_max = word.bounding_box.vertices[2].y

                        # Check if the word is to the right of the key and within a similar Y range
                        if word_x_min > key_x_max and key_y_min <= word_y_max <= key_y_max:
                            # Calculate horizontal distance between the key and the word
                            distance = word_x_min - key_x_max
                            if distance < min_distance:
                                closest_value = word_description
                                min_distance = distance

            if closest_value:
                value = closest_value

        return value
    
    def print_text_annotations(self, text_annotations):
        """Debug function to print the bounding boxes and text layout."""
        print("\nText Annotations (with Bounding Boxes):")
        for annotation in text_annotations:
            description = annotation.description
            vertices = annotation.bounding_poly.vertices
            print(f"Text: '{description}'")
            print("Bounding Box Coordinates:")
            for vertex in vertices:
                print(f"  ({vertex.x}, {vertex.y})")
            print("-" * 40)
            
    def reorganize_text_by_bounding_box(self, text_annotations):
        """Reorganize the text based on bounding box positions (Y first, X second)."""
        # Collect words with their bounding box information
        words_with_bounding_boxes = []

        for annotation in text_annotations:
            word_text = annotation.description
            bounding_box = annotation.bounding_poly.vertices
            # Extract Y and X coordinates from the bounding box
            x_min = bounding_box[0].x
            y_min = bounding_box[0].y
            x_max = bounding_box[2].x
            y_max = bounding_box[2].y
            words_with_bounding_boxes.append({
                'text': word_text,
                'x_min': x_min,
                'y_min': y_min,
                'x_max': x_max,
                'y_max': y_max
            })

        # Sort the words first by their Y-coordinate (vertical), then by X-coordinate (horizontal)
        sorted_words = sorted(words_with_bounding_boxes, key=lambda x: (x['y_min'], x['x_min']))

        # Join the sorted words into a single string to simulate the correct reading order
        organized_text = ' '.join([word['text'] for word in sorted_words])
        
        return organized_text
    
