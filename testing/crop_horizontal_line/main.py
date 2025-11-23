
from google.cloud import vision
import io
import cv2
import numpy as np
import os
from collections import defaultdict

FULL_NAME_COLUMN_IMAGE_FILE_NAME = "column_1.png"
NIK_COLUMN_IMAGE_FILE_NAME = "column_2.png"
SEXES_COLUMN_IMAGE_FILE_NAME = "column_3.png"
BIRTHPLACE_COLUMN_IMAGE_FILE_NAME = "column_4.png"
BIRTHDATE_COLUMN_IMAGE_FILE_NAME =  "column_5.png"
RELIGION_COLUMN_IMAGE_FILE_NAME = "column_6.png"
EDUCATION_COLUMN_IMAGE_FILE_NAME = "column_7.png"
PROFESION_COLUMN_IMAGE_FILE_NAME ="column_8.png"

MARRIAGE_STAT_COLUMN_IMAGE_FILE_NAME = "column_1.png"
MARRIAGE_DATE_COLUMN_IMAGE_FILE_NAME = "column_2.png"
MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME = "column_3.png"
CITIZEN_COLUMN_IMAGE_FILE_NAME = "column_4.png"
PASPOR_NO_COLUMN_IMAGE_FILE_NAME = "column_5.png"
KITAS_NO_COLUMN_IMAGE_FILE_NAME = "column_6.png"
FATHER_COLUMN_IMAGE_FILE_NAME = "column_7.png"
MOTHER_COLUMN_IMAGE_FILE_NAME = "column_8.png"

MARRIAGE_REL_COLUMN_IMAGE_FILE_NAME_2018V = "column_2.png"
CITIZEN_COLUMN_IMAGE_FILE_NAME_2018V = "column_3.png"
PASPOR_NO_COLUMN_IMAGE_FILE_NAME_2018V = "column_4.png"
KITAS_NO_COLUMN_IMAGE_FILE_NAME_2018V = "column_5.png"
FATHER_COLUMN_IMAGE_FILE_NAME_2018V = "column_6.png"
MOTHER_COLUMN_IMAGE_FILE_NAME_2018V = "column_7.png"

LOWER_TABLE_DIR = "./"
UPPER_TABLE_DIR = "./"

def crop_above_nth_horizontal_line_with_grouping(img, n=3, line_gap=10):
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
    
p = LOWER_TABLE_DIR+FATHER_COLUMN_IMAGE_FILE_NAME
directory = os.path.dirname(p)   # './output/sliced_lower_table'
filename = os.path.basename(p)   # 'column_2.png'

# preprocess
image = cv2.imread(p)
cropped_image = crop_above_nth_horizontal_line_with_grouping(img=image,n=4)
cropped_image_path = directory + "/header_cropped_" + filename
cv2.imwrite(cropped_image_path, cropped_image)