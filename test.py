import cv2
import TableLinesRemover as tlr
import numpy as np

    
img = cv2.imread("./output/sliced_upper_table/before_column_4.png")
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresholded_image = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)[1]
inverted_image = cv2.bitwise_not(thresholded_image)

hor = np.array([[1,1,1]])
vertical_lines_eroded_image = cv2.erode(inverted_image, hor, iterations=2)
vertical_lines_eroded_image = cv2.dilate(vertical_lines_eroded_image, hor, iterations=3)

cv2.imwrite("after.png", vertical_lines_eroded_image)

# --- Find the bottom-most horizontal line ---
# Sum each row's pixel values (lines will have high sums)
row_sums = np.sum(vertical_lines_eroded_image == 255, axis=1)

# Find all rows where there is a line (tweak threshold if needed)
line_rows = np.where(row_sums > vertical_lines_eroded_image.shape[1] * 0.9)[0]  # More than 50% white pixels

if len(line_rows) > 0:
    bottom_line_y = line_rows.max()
    
    # Optional: subtract a few pixels to crop just above the line
    margin = 2
    crop_y = max(0, bottom_line_y - margin)
    
    # Crop the original image above the bottom line
    cropped = img[:crop_y, :]
    cv2.imwrite("cropped_above_bottom_line.png", cropped)
    print(f"Cropped above bottom line at Y={crop_y}")
else:
    print("No horizontal lines found.")