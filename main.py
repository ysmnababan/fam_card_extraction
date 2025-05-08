import ImageProcessor as ip

# === Config ===
TARGET_IMAGE_PATH = './img/kk1.jpeg'
TEMPLATE_IMAGE_PATH = './templ/kk_template.png'
OUTPUT_ALIGNED_PATH = './output/aligned_target.png'
CROP_OUTPUT_DIR = 'cropped_cells'

if __name__ == '__main__':
    processor = ip.ImageProcessor(
        TARGET_IMAGE_PATH,
        TEMPLATE_IMAGE_PATH,
        OUTPUT_ALIGNED_PATH,
        CROP_OUTPUT_DIR
    )
    # processor.run()
    processor.extract_table()
    processor.extract_header()
    processor.extract_footer()