import ImageProcessor as ip
import FamilyData as fd
# === Config ===
TARGET_IMAGE_PATH = './img/kk1.jpeg'
TEMPLATE_IMAGE_PATH = './templ/kk_template.png'
OUTPUT_ALIGNED_PATH = './output/aligned_target.png'
CROP_OUTPUT_DIR = 'cropped_cells'
JSON_OUTPUT_PATH = "./output/kk_data.json"
PROCESSED_JSON_PATH = "./output/processed_data.json"
if __name__ == '__main__':
    processor = ip.ImageProcessor(
        TARGET_IMAGE_PATH,
        TEMPLATE_IMAGE_PATH,
        OUTPUT_ALIGNED_PATH,
        CROP_OUTPUT_DIR
    )
    # processor.run()
    # processor.extract_table()
    # processor.extract_header()
    # processor.extract_footer()

    family = fd.FamilyData.from_json_file(JSON_OUTPUT_PATH)
    family.preprocess(PROCESSED_JSON_PATH)
    family.print_all()