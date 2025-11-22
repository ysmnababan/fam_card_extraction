import ImageProcessor as ip
import FamilyData as fd
import ExcelTemplateFiller as etf
import os 
import sys
import platform
from pathlib import Path
# === Config ===
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
DELETE_OUTPUT_FOLDER = "true"

# return path to credential file we should use (string)
def get_credentials_path(filename="secret.json"):
    # 1) honour existing env var if user set it (most flexible)
    env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if env and Path(env).exists():
        return env

    # 2) if running as a PyInstaller onefile executable, data is unpacked to _MEIPASS
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        p = Path(meipass) / filename
        if p.exists():
            return str(p)

    # 3) development defaults by platform
    if platform.system() == "Windows":
        # Windows dev default (you can change this)
        p = Path(r"C:\app_credentials") / filename
    else:
        # Linux dev default — prefer user config dir rather than root.
        # e.g. /home/you/.config/myapp/kk-scanner-...json
        p = Path.home() / ".config" / "kk_scanner" / filename

        # If you *really* want the root dir (not recommended), use:
        # p = Path("/") / filename

    return str(p) if p.exists() else None

if __name__ == '__main__':
    cred = get_credentials_path()
    if cred:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred
        print("Using credentials:", cred)
    else:
        print("No credentials found. Set GOOGLE_APPLICATION_CREDENTIALS or place the JSON in your config dir.")
    if os.path.exists(FINAL_PATH):
        os.remove(FINAL_PATH)
        print(f"Deleted file: {FINAL_PATH}")
        
    processor = ip.ImageProcessor(
        TARGET_IMAGE_PATH,
        TEMPLATE_IMAGE_PATH,
        OUTPUT_ALIGNED_PATH,
        CROP_OUTPUT_DIR,
        OPEN_EXPLORER,
        DELETE_OUTPUT_FOLDER
    )
    processor.run()
    processor.extract_table()
    processor.extract_header()
    processor.extract_footer()

    family = fd.FamilyData.from_json_file(JSON_OUTPUT_PATH)
    family.preprocess(PROCESSED_JSON_PATH)

    etf.populate_excel(input_json_path=PROCESSED_JSON_PATH, workbook_path=WORKBOOK_PATH, final_output_path=FINAL_PATH)