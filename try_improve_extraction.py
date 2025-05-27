import TableScanner as ts 
import os
LOWER_TABLE_DIR = "./output/sliced_lower_table/"
UPPER_TABLE_DIR = "./output/sliced_upper_table/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\app_credentials\kk-scanner-7a632fda35c3.json"

table_scanner = ts.TableScanner()
out = table_scanner.detect_single_image(LOWER_TABLE_DIR+"column_1.png", 3)
print(out)