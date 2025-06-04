import os
import ImageProcessor as ip
import cv2

TARGET_IMAGE_PATH = './img/kk1.jpeg'
TEMPLATE_IMAGE_PATH = './templ/kk_template.png'
OUTPUT_ALIGNED_PATH = './output/aligned_target.png'
CROP_OUTPUT_DIR = 'cropped_cells'
JSON_OUTPUT_PATH = "./output/kk_data.json"
PROCESSED_JSON_PATH = "./output/processed_data.json"
WORKBOOK_PATH = "./templ/template.xlsx"
# FINAL_PATH = "final.xlsx"
FINAL_PATH = ""
OPEN_EXPLORER = "true"
DELETE_OUTPUT_FOLDER = "false"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\app_credentials\kk-scanner-7a632fda35c3.json"

processor = ip.ImageProcessor(
        TARGET_IMAGE_PATH,
        TEMPLATE_IMAGE_PATH,
        OUTPUT_ALIGNED_PATH,
        CROP_OUTPUT_DIR,
        OPEN_EXPLORER,
        DELETE_OUTPUT_FOLDER
    )
img= cv2.imread("./output/horizontal_part_2.png")
cropped = processor.crop_upper_and_lower_space(img)
cv2.imwrite("testing.png", cropped)
