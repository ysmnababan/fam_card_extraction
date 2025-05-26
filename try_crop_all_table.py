import cv2
import numpy as np
OUTPUT_PATH = './output2'
# WHOLE_TABLE = 

def visualize_line_rows(img, line_rows, color=(0, 0, 255), thickness=1, scale=1.0):
    """
    Draws horizontal lines at the specified row indices (line_rows) on a copy of the image,
    and resizes the image by the given scale factor.
    
    Parameters:
    - img: Original image (numpy array)
    - line_rows: List of row indices (Y values)
    - color: BGR color of lines (default: red)
    - thickness: Thickness of drawn lines
    - scale: Scale factor to resize the image (default: 1.0, i.e., no resizing)
    
    Returns:
    - img_copy: Annotated and resized image
    """
    img_copy = img.copy()
    for y in line_rows:
        cv2.line(img_copy, (0, y), (img.shape[1], y), color, thickness)
    
    if scale != 1.0:
        new_width = int(img_copy.shape[1] * scale)
        new_height = int(img_copy.shape[0] * scale)
        img_copy = cv2.resize(img_copy, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return img_copy

def crop_transformed_image(transformed_points, aligned_target):
    y_values = transformed_points[:, 1]
    top_y = int(min(y_values))
    bottom_y = int(max(y_values))
    mid_y = (top_y + bottom_y) // 2

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
        
def crop_upper_and_lower_space(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
    inverted_image = cv2.bitwise_not(thresholded_image)

    hor = np.array([[1, 1, 1]])
    processed = cv2.erode(inverted_image, hor, iterations=1)
    processed = cv2.dilate(processed, hor, iterations=3)

    row_sums = np.sum(processed == 255, axis=1)
    
    # Find horizontal lines by thresholding how many white pixels per row
    line_rows = np.where(row_sums > processed.shape[1] * 0.25)[0]

    debug_img = visualize_line_rows(img, line_rows, scale=0.20)
    cv2.imshow("Line Rows", debug_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # Group nearby line rows (e.g., within 10px)
    # grouped_lines = []
    # current_group = []

    # for y in line_rows:
    #     if not current_group or y - current_group[-1] <= line_gap:
    #         current_group.append(y)
    #     else:
    #         grouped_lines.append(current_group)
    #         current_group = [y]

    # if current_group:
    #     grouped_lines.append(current_group)

    # # Get the Y position of each unique line group (e.g., middle of the group)
    # line_positions = [group[len(group) // 2] for group in grouped_lines]
    # line_rows = line_positions
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

def crop_in_middle(cropped):
    # Get height and calculate midpoint
    height = cropped.shape[0]
    midpoint = height // 2

    # Split into upper and lower halves
    upper_table = cropped[:midpoint, :]
    lower_table = cropped[midpoint:, :]

    # Save both halves
    cv2.imwrite(OUTPUT_PATH+"/upper_table.png", upper_table)
    cv2.imwrite(OUTPUT_PATH+"/lower_table.png", lower_table)
    
img = cv2.imread("./output/aligned_target.png")
transformed_points = [
    (117.0, 847.0),
    (6902.0, 847.0),
    (6902.0, 3468.0),
    (117.0, 3468.0),
]
transformed_points = np.array(transformed_points)
crop_transformed_image(transformed_points, img)
img = cv2.imread("./output2/horizontal_part_2.png")
cropped = crop_upper_and_lower_space(img)
cv2.imwrite("above_crop.png", cropped)
crop_in_middle(cropped)