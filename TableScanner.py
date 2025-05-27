from google.cloud import vision
import io
import cv2
import numpy as np
import os
from collections import defaultdict

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

    def crop_above_nth_horizontal_line_with_grouping(self, img, n=3, line_gap=10):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
        inverted_image = cv2.bitwise_not(thresholded_image)

        hor = np.array([[1, 1, 1, 1, 1]])
        eroded = cv2.erode(inverted_image, hor, iterations=7)
        dilated = cv2.dilate(eroded, hor, iterations=3)

        row_sums = np.sum(dilated == 255, axis=1)
        line_rows = np.where(row_sums > dilated.shape[1] * 0.7)[0]

        # print("Raw line rows:", line_rows)
        # Group nearby line rows (e.g., within 10px)
        grouped_lines = []
        current_group = []

        for y in line_rows:
            if not current_group or y - current_group[-1] <= line_gap:
                current_group.append(y)
            else:
                grouped_lines.append(current_group)
                current_group = [y]

        if current_group:
            grouped_lines.append(current_group)

        # Get the Y position of each unique line group (e.g., middle of the group)
        line_positions = [group[len(group) // 2] for group in grouped_lines]

        # print("Grouped horizontal line positions:", line_positions)

        if len(line_positions) >= n:
            nth_line_y = line_positions[n - 1]
            crop_y = min(img.shape[0], nth_line_y + 2)  # margin below line
            cropped = img[crop_y:, :]
            print(f"Cropped above line {n} at Y={crop_y}")
            return cropped
        else:
            print(f"Only found {len(line_positions)} lines, can't crop at line {n}")
            return img

    def deskew_projection_method(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Edge detection
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)

        # Detect lines
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)

        if lines is None:
            print("No lines detected for skew correction.")
            return image, 0

        angles = []

        for line in lines:
            rho, theta = line[0]
            angle = (theta * 180 / np.pi) - 90
            if -45 < angle < 45:  # focus on near-horizontal lines
                angles.append(angle)

        if len(angles) == 0:
            return image, 0

        avg_angle = np.mean(angles)
        print(f"[INFO] Detected skew angle: {avg_angle:.2f} degrees")

        # Rotate image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated, avg_angle
    
    def load_image_as_vision_request(self, image_path):
        client = vision.ImageAnnotatorClient()
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return client.document_text_detection(image=image)
    
    def extract_lines_from_annotation(self, response, y_tolerance=10):
        """Group words into lines based on their Y positions."""
        if not response.full_text_annotation.pages:
            return []

        word_positions = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        text = ''.join([symbol.text for symbol in word.symbols])
                        vertices = word.bounding_box.vertices
                        y_min = min(v.y for v in vertices if v.y is not None)
                        y_max = max(v.y for v in vertices if v.y is not None)
                        y_center = (y_min + y_max) / 2
                        word_positions.append((y_center, text, min(v.x for v in vertices)))

        # Group words by their Y coordinate into lines
        lines_dict = defaultdict(list)
        for y_center, text, x in word_positions:
            matched = False
            for key in lines_dict:
                if abs(key - y_center) <= y_tolerance:
                    lines_dict[key].append((x, text))
                    matched = True
                    break
            if not matched:
                lines_dict[y_center].append((x, text))

        # Sort lines top-to-bottom and words left-to-right
        sorted_lines = []
        for key in sorted(lines_dict.keys()):
            words = sorted(lines_dict[key], key=lambda x: x[0])
            line = ' '.join([w for _, w in words])
            sorted_lines.append(line)

        return sorted_lines
    def extract_lines_from_annotation_v2(self, response):
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
        return merged_lines
    
    def detect_single_image(self, image_path, n=3):
        directory = os.path.dirname(image_path)   # './output/sliced_lower_table'
        filename = os.path.basename(image_path)   # 'column_2.png'

        # preprocess
        image = cv2.imread(image_path)
        deskewed, angle = self.deskew_projection_method(image)
        print(f"Image deskewed by {angle:.2f} degrees")
        cropped_image = self.crop_above_nth_horizontal_line_with_grouping(img=deskewed,n=n)
        cropped_image_path = directory + "/header_cropped_" + filename
        cv2.imwrite(cropped_image_path, cropped_image)

        response = self.load_image_as_vision_request(cropped_image_path)
        return self.extract_lines_from_annotation(response)