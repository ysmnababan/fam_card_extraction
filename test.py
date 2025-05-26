# import cv2
# import TableLinesRemover as tlr
# import numpy as np

    
# img = cv2.imread("./output/sliced_upper_table/before_column_4.png")
# grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
# inverted_image = cv2.bitwise_not(thresholded_image)

# hor = np.array([[1,1,1]])
# vertical_lines_eroded_image = cv2.erode(inverted_image, hor, iterations=2)
# vertical_lines_eroded_image = cv2.dilate(vertical_lines_eroded_image, hor, iterations=3)

# cv2.imwrite("after.png", vertical_lines_eroded_image)

# # --- Find the bottom-most horizontal line ---
# # Sum each row's pixel values (lines will have high sums)
# row_sums = np.sum(vertical_lines_eroded_image == 255, axis=1)

# # Find all rows where there is a line (tweak threshold if needed)
# line_rows = np.where(row_sums > vertical_lines_eroded_image.shape[1] * 0.9)[0]  # More than 50% white pixels

# if len(line_rows) > 0:
#     bottom_line_y = line_rows.max()
    
#     # Optional: subtract a few pixels to crop just above the line
#     margin = 2
#     crop_y = max(0, bottom_line_y - margin)
    
#     # Crop the original image above the bottom line
#     cropped = img[:crop_y, :]
#     cv2.imwrite("cropped_above_bottom_line.png", cropped)
#     print(f"Cropped above bottom line at Y={crop_y}")
# else:
#     print("No horizontal lines found.")
    
    
# ==================================================================================================
# import TableScanner as ts
# import os 

# MOTHER_COLUMN_IMAGE_FILE_NAME_2018V = "column_8.png"

# LOWER_TABLE_DIR = "./output/sliced_lower_table/"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\app_credentials\kk-scanner-7a632fda35c3.json"

# table_scanner = ts.TableScanner()
# mother_names = table_scanner.detect_single_image(LOWER_TABLE_DIR+MOTHER_COLUMN_IMAGE_FILE_NAME_2018V)

# print(mother_names)
# ==================================================================================================
import cv2
import numpy as np

def visualize_line_rows(img, line_rows, color=(0, 0, 255), thickness=1):
    """
    Draws horizontal lines at the specified row indices (line_rows) on a copy of the image.
    
    Parameters:
    - img: Original image
    - line_rows: List of row indices (Y values)
    - color: BGR color of lines (default: red)
    - thickness: Thickness of drawn lines
    """
    img_copy = img.copy()
    for y in line_rows:
        cv2.line(img_copy, (0, y), (img.shape[1], y), color, thickness)
    return img_copy

def crop_above_nth_horizontal_line(img, n):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
    inverted_image = cv2.bitwise_not(thresholded_image)

    # Use a horizontal kernel to enhance horizontal lines
    hor = np.array([[1, 1, 1]])
    horizontal_lines_eroded = cv2.erode(inverted_image, hor, iterations=2)
    horizontal_lines_dilated = cv2.dilate(horizontal_lines_eroded, hor, iterations=3)
    cv2.imwrite("after.png", horizontal_lines_dilated)

    # Sum pixel values row-wise
    row_sums = np.sum(horizontal_lines_dilated == 255, axis=1)
    print("row sum:", row_sums)
    # Rows with "strong" white horizontal lines (adjust threshold if needed)
    line_rows = np.where(row_sums > horizontal_lines_dilated.shape[1] * 0.7)[0]
    print("line rows: ", line_rows)
    debug_img = visualize_line_rows(img, line_rows)
    cv2.imshow("Line Rows", debug_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if len(line_rows) >= n:
        nth_line_y = line_rows[n - 1]  # Indexing starts at 0

        # Optional margin to crop slightly below the line
        margin = 2
        crop_y = min(img.shape[0], nth_line_y + margin)

        cropped = img[crop_y:, :]
        print(f"Cropped above line {n} at Y={crop_y}")
        return cropped
    else:
        print(f"Only found {len(line_rows)} horizontal lines; cannot crop at line {n}.")
        return img


def crop_above_nth_horizontal_line_with_grouping(img, n, line_gap=10):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
    inverted_image = cv2.bitwise_not(thresholded_image)

    hor = np.array([[1, 1, 1,]])
    eroded = cv2.erode(inverted_image, hor, iterations=6)
    dilated = cv2.dilate(eroded, hor, iterations=3)

    row_sums = np.sum(dilated == 255, axis=1)
    line_rows = np.where(row_sums > dilated.shape[1] * 0.6)[0]

    print("Raw line rows:", line_rows)
    # debug_img = visualize_line_rows(img, line_rows)
    # cv2.imshow("Line Rows", debug_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
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

    print("Grouped horizontal line positions:", line_positions)

    if len(line_positions) >= n:
        nth_line_y = line_positions[n - 1]
        crop_y = min(img.shape[0], nth_line_y + 2)  # margin below line
        cropped = img[crop_y:, :]
        print(f"Cropped above line {n} at Y={crop_y}")
        return cropped
    else:
        print(f"Only found {len(line_positions)} lines, can't crop at line {n}")
        return img

def visualize_hough_lines(image, min_line_length=100, max_line_gap=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                            minLineLength=min_line_length, maxLineGap=max_line_gap)

    line_img = image.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Draw only almost-horizontal lines
            if abs(y2 - y1) < 10:
                cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return line_img, lines

def deskew_image_using_hough(image, angle_threshold=10, hough_threshold=200):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=hough_threshold)

    angles = []
    if lines is not None:
        for rho, theta in lines[:, 0]:
            angle_deg = np.rad2deg(theta)
            if angle_deg < angle_threshold or angle_deg > (180 - angle_threshold):
                angle = (theta - np.pi / 2)
                angles.append(angle)

    avg_angle_deg = 0
    if angles:
        avg_angle_rad = np.mean(angles)
        avg_angle_deg = np.rad2deg(avg_angle_rad)

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, avg_angle_deg, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated, avg_angle_deg

def deskew_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Correct angle logic
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    print(f"[Deskew] Rotation angle: {angle:.2f}")
    return rotated


def deskew_using_min_area_rect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find coordinates of all white pixels (since we're using binary inverted)
    coords = np.column_stack(np.where(binary > 0))

    if coords.shape[0] == 0:
        print("No foreground pixels detected for skew correction.")
        return image, 0

    rect = cv2.minAreaRect(coords)
    angle = rect[-1]

    # Convert angle to range [-90, 0)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    print(f"[INFO] Detected skew angle: {angle:.2f} degrees")

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated, angle

def deskew_projection_method(image):
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

def crop_above_table_header(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
    inverted_image = cv2.bitwise_not(thresholded_image)

    hor = np.array([[1, 1, 1,]])
    processed = cv2.erode(inverted_image, hor, iterations=2)
    processed = cv2.dilate(processed, hor, iterations=3)

    row_sums = np.sum(processed == 255, axis=1)
    
    # Find horizontal lines by thresholding how many white pixels per row
    line_rows = np.where(row_sums > processed.shape[1] * 0.6)[0]
    debug_img = visualize_line_rows(img, line_rows)
    cv2.imshow("Line Rows", debug_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if len(line_rows) > 0:
        top_line_y = line_rows.min()
        margin = -12  # Optional: include a few pixels above
        crop_y = min(img.shape[0], top_line_y + margin)
        if crop_y <0 :
            crop_y = 0
        cropped = img[crop_y:, :]
        print(f"Cropped below top horizontal line at Y={img.shape[0]}->{top_line_y}")
        return cropped
    else:
        print("No horizontal lines found.")
        return img

def crop_above_table_header_hough(img, angle_tolerance=10):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=10
    )

    if lines is None:
        print("No lines detected")
        return img

    # Filter near-horizontal lines
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) < angle_tolerance:  # near horizontal
            horizontal_lines.append((y1 + y2) // 2)

    if not horizontal_lines:
        print("No horizontal lines found.")
        return img

    top_line_y = min(horizontal_lines)
    margin = -12  # adjust as needed
    crop_y = max(0, top_line_y + margin)

    cropped = img[crop_y:, :]
    print(f"Cropped below top horizontal line at Y={crop_y}")

    # Debug visualization (optional)
    debug_img = img.copy()
    for y in horizontal_lines:
        cv2.line(debug_img, (0, y), (img.shape[1], y), (0, 0, 255), 1)
    cv2.imshow("Detected Horizontal Lines", debug_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return cropped    
img = cv2.imread("./output/sliced_lower_table/before_column_8.png")

deskewed, angle = deskew_projection_method(img)
cv2.imwrite("deskewed.png", deskewed)

above_crop = crop_above_table_header(deskewed)
print(f"Image deskewed by {angle:.2f} degrees")
cv2.imwrite("above_crop.png", above_crop)

output_img = crop_above_nth_horizontal_line_with_grouping(above_crop, 3)
cv2.imwrite("cropped.png", output_img)

# Step 1: Deskew
# deskewed_img = deskew_image(img)

# Step 2: Visualize horizontal lines
# visualized_img, hough_lines = visualize_hough_lines(deskewed_img)

# Show result
# cv2.imshow("Deskewed + Hough Lines", visualized_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# from pathlib import Path
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # Load the uploaded image
# # image_path = Path("/mnt/data/d68f4bb3-7d14-4f8c-8917-82255526532e.png")
# # image = cv2.imread(str(image_path))
# image = cv2.imread("./output/sliced_upper_table/column_1.png")

# deskewed, angle = deskew_projection_method(image)
# print(f"Image deskewed by {angle:.2f} degrees")

# cv2.imshow("Deskewed Image", deskewed)
# cv2.waitKey(0)
# cv2.destroyAllWindows()