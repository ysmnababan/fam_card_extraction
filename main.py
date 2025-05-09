import ImageProcessor as ip
import FamilyData as fd
import ExcelTemplateFiller as etf
import os 
# === Config ===
TARGET_IMAGE_PATH = './img/kk1.jpeg'
TEMPLATE_IMAGE_PATH = './templ/kk_template.png'
OUTPUT_ALIGNED_PATH = './output/aligned_target.png'
CROP_OUTPUT_DIR = 'cropped_cells'
JSON_OUTPUT_PATH = "./output/kk_data.json"
PROCESSED_JSON_PATH = "./output/processed_data.json"
WORKBOOK_PATH = "./templ/template.xlsx"
FINAL_PATH = "final.xlsx"
OPEN_EXPLORER = "true"
DELETE_OUTPUT_FOLDER = "false"


if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\app_credentials\kk-scanner-7a632fda35c3.json"
    if os.path.exists(FINAL_PATH):
        os.remove(FINAL_PATH)
        print(f"Deleted file: {FINAL_PATH}")
    else:
        print(f"File does not exist: {FINAL_PATH}")
        
    processor = ip.ImageProcessor(
        TARGET_IMAGE_PATH,
        TEMPLATE_IMAGE_PATH,
        OUTPUT_ALIGNED_PATH,
        CROP_OUTPUT_DIR,
        OPEN_EXPLORER,
        DELETE_OUTPUT_FOLDER
    )
    # processor.run()
    # processor.extract_table()
    # processor.extract_header()
    processor.extract_footer()

    # family = fd.FamilyData.from_json_file(JSON_OUTPUT_PATH)
    # family.preprocess(PROCESSED_JSON_PATH)

    # etf.populate_excel(input_json_path=PROCESSED_JSON_PATH, workbook_path=WORKBOOK_PATH, final_output_path=FINAL_PATH)