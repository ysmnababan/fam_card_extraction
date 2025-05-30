import cv2
import numpy as np
import ScreenUtils as su
import ImageClickZoom as icz
import TableLinesRemover as tlr
import KKStructure as kk
import ParserHeader as ph
import ParserFooter as pf
from tkinter import Tk, filedialog
from pdf2image import convert_from_path
import os
import shutil
import sys
from helper import resource_path

JSON_TEMPLATE = resource_path("./templ/template.json")
OUTPUT_PATH = './output'
SLICED_UPPER_TABLE = '/sliced_upper_table'
SLICED_LOWER_TABLE = '/sliced_lower_table'
UNPROCESSED_KK_JSON = 'kk_data.json'
HEADER_SOURCE_IMG = "/horizontal_part_1.png"
FOOTER_SOURCE_IMG = "/horizontal_part_3.png"
BEFORE_2018V = "BEFORE_2018"
AFTER_2018V = "AFTER_2018"

class ImageProcessor:
    def __init__(self, target_path, template_path, output_aligned_path, crop_output_dir, open_window, delete_output):
        self.target_path = resource_path(target_path)
        self.template_path = resource_path(template_path)
        self.output_aligned_path = resource_path(output_aligned_path)
        self.crop_output_dir = crop_output_dir
        self.version = "after_2018"
        self.open_window = open_window
        self.converted_image_path = None  # path to converted PNG if PDF
        if os.path.exists(OUTPUT_PATH) and delete_output == "true":
            shutil.rmtree(OUTPUT_PATH)
            print(f"Deleted folder: {OUTPUT_PATH}")
        else:
            print(f"Folder does not exist: {OUTPUT_PATH}")
        # Recreate it
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    def extract_header(self):
        json_output_path = OUTPUT_PATH + "/" + UNPROCESSED_KK_JSON
        image_path = OUTPUT_PATH + HEADER_SOURCE_IMG
        ph.execute(image_path, json_output_path)

    def extract_footer(self):
        json_output_path = OUTPUT_PATH + "/" + UNPROCESSED_KK_JSON
        image_path = OUTPUT_PATH + FOOTER_SOURCE_IMG
        pf.execute(image_path=image_path, output_path=json_output_path)

    def extract_table(self):
        json_output_path = OUTPUT_PATH + "/" + UNPROCESSED_KK_JSON
        main_table = kk.KKStructure(self.version)
        main_table.execute(filename=json_output_path, template_filename=JSON_TEMPLATE)

    def select_file(self):
        root = Tk()
        root.withdraw()  # Hide tkinter window
        self.target_path = filedialog.askopenfilename(
            title="Select an image or PDF file",
            filetypes=[("Image and PDF files", "*.jpg *.jpeg *.png *.bmp *.pdf")]
        )
        if not self.target_path:
            print("No file selected.")
            sys.exit(1)
        else:
            print(f"Selected file: {self.target_path}")

    def convert_pdf_to_png(self, pdf_path):
        # Get the path of the current script
        current_dir = os.path.dirname(__file__)

        # Point to the 'bin' directory inside the 'poppler' folder
        poppler_path = os.path.join(current_dir, "poppler", "bin")
        print("Converting PDF to PNG...")
        pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)
        if not pages:
            print("PDF has no pages.")
            return None
        output_png = os.path.splitext(pdf_path)[0] + "_page1.png"
        pages[0].save(output_png, "PNG")
        print(f"Saved first page as: {output_png}")
        return output_png
    
    def run(self):
        template = cv2.imread(self.template_path)

        if self.open_window == "true":
            self.select_file()

        if self.target_path:
            file_ext = os.path.splitext(self.target_path)[1].lower()

            if file_ext == '.pdf':
                # convert PDF to PNG first
                self.converted_image_path = self.convert_pdf_to_png(self.target_path)
                img_path = self.converted_image_path
            else:
                img_path = self.target_path

            if img_path:
                target = cv2.imread(img_path)
                if target is None:
                    print("Failed to load the image.")
                    sys.exit(1)
                else:
                    print("Image loaded successfully.")
            else:
                print("No image to load.")
                sys.exit(1)
        else:
            print("Run cancelled: no file selected.")
            sys.exit(1)

        target = cv2.resize(target, (template.shape[1], template.shape[0]))
        h_img, w_img = target.shape[:2]

        screen_w, screen_h = su.ScreenUtils.get_screen_size()
        max_w = int(screen_w * 0.9)
        max_h = int(screen_h * 0.9)
        scale_w = max_w / w_img
        scale_h = max_h / h_img
        best_scale = min(scale_w, scale_h, 1.0)
        print(f"Initial scale set to: {best_scale:.2f}")

        clicker = icz.ImageClickZoom(target, scale_init=best_scale, screen_w=screen_w, screen_h=screen_h)
        clicked_points = clicker.show()

        if len(clicked_points) != 4:
            print("You must select exactly 4 points.")
            sys.exit(1)

        clicked_points = clicker.order_points_clockwise(clicked_points)

        target_pts = np.array(clicked_points, dtype='float32')
        template_pts = np.array([
            [117, 847],
            [6902, 847],
            [6902, 3468],
            [117, 3468]
        ], dtype='float32')

        M = cv2.getPerspectiveTransform(target_pts, template_pts)
        aligned_target = cv2.warpPerspective(target, M, (w_img, h_img))

        cv2.imwrite(self.output_aligned_path, aligned_target)
        print(f"Aligned image saved to: {self.output_aligned_path}")

        pts = np.array(clicked_points, dtype='float32').reshape(-1, 1, 2)
        transformed_points = cv2.perspectiveTransform(pts, M).reshape(-1, 2)

        print("Transformed points (in aligned image):")
        for pt in transformed_points:
            print(f"({pt[0]:.2f}, {pt[1]:.2f})")
        self.crop_transformed_image(transformed_points, aligned_target)
        self.chop_table_by_column()
        if (self.upper_column_num == 11 and self.lower_column_num == 10):
            self.version = AFTER_2018V
        elif (self.upper_column_num == 10 and self.lower_column_num == 9):
            self.version = BEFORE_2018V
        else :
            print("failed to crop table")
            sys.exit(1)
        print(self.version)    
        

    def chop_table_by_column(self):
        lines_remover = tlr.TableLinesRemover(self.upper_table)
        lines_remover.execute(OUTPUT_PATH + SLICED_UPPER_TABLE)
        self.upper_column_num = lines_remover.get_column()
        
        lines_remover = tlr.TableLinesRemover(self.lower_table)
        lines_remover.execute(OUTPUT_PATH+SLICED_LOWER_TABLE)
        self.lower_column_num = lines_remover.get_column()
        return

    def crop_upper_and_lower_space(self, img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
        inverted_image = cv2.bitwise_not(thresholded_image)

        hor = np.array([[1, 1, 1]])
        processed = cv2.erode(inverted_image, hor, iterations=1)
        processed = cv2.dilate(processed, hor, iterations=3)

        row_sums = np.sum(processed == 255, axis=1)
        
        # Find horizontal lines by thresholding how many white pixels per row
        line_rows = np.where(row_sums > processed.shape[1] * 0.25)[0]
        if len(line_rows) > 0:
            margin = 15
            top_line_y = max(line_rows.min() - margin, 0)  # Add small margin above
            bottom_line_y = min(line_rows.max() + margin, img.shape[0])  # Add small margin below

            cropped = img[top_line_y:bottom_line_y, :]
            print(f"Cropped image from Y={top_line_y} to Y={bottom_line_y}")
            return cropped
        else:
            print("No horizontal lines found.")
            return img

    def crop_in_middle(self, cropped):
        # Get height and calculate midpoint
        height = cropped.shape[0]
        midpoint = height // 2

        # Split into upper and lower halves
        self.upper_table = cropped[:midpoint, :]
        self.lower_table = cropped[midpoint:, :]

        # Save both halves
        cv2.imwrite(OUTPUT_PATH+"/upper_table.png", self.upper_table)
        cv2.imwrite(OUTPUT_PATH+"/lower_table.png", self.lower_table)
        
    def crop_transformed_image(self, transformed_points, aligned_target):
        y_values = transformed_points[:, 1]
        top_y = int(min(y_values))
        bottom_y = int(max(y_values))

        height, _ = aligned_target.shape[:2]
        PADDING = 30
        regions = [
            (0, top_y + PADDING),
            (top_y-100, bottom_y+100),
            (bottom_y, height)
        ]

        for i, (start_y, end_y) in enumerate(regions, start=1):
            cropped = aligned_target[start_y:end_y, :]
            cv2.imwrite(f"{OUTPUT_PATH}/horizontal_part_{i}.png", cropped)
            if i == 2:
                cropped = self.crop_upper_and_lower_space(cropped)
                self.crop_in_middle(cropped)