import cv2
import numpy as np

# 1st image processing
# This process cuts the outline of the image.

# Read image
image = cv2.imread('C:/Users/ririk/Desktop/DLIP_Final_Project/test_image/TEST20.JPG')

# Structuring element kernel, a rectangle (3x3) is created ---①
k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# Apply erosion operation ---②
image_copy = cv2.erode(image, k)

# Canny edges
edges_1st = cv2.Canny(image_copy, 0, 250)

cv2.imshow("OutlineImage", edges_1st)
cv2.waitKey(0)


# Detect contours 
contours, _ = cv2.findContours(edges_1st, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Cut outline
    max_contour = max(contours, key=cv2.contourArea)

    # Calculate positions of the outline box
    x, y, w, h = cv2.boundingRect(max_contour)

    # Cut for outline
    cropped_image = image[y:y + h, x:x + w]

    # Print image
    cv2.imshow("OutlineImage", cropped_image)
    cv2.waitKey(0)

else:
    print("Contour not found.")



# ---------------------------------------------------------------------
# 2nd image processing
# This process cuts the image for word boxes.

# Canny edge detection for edges
edges_2nd = cv2.Canny(cropped_image, 50, 150)

# Detect lines using HoughLinesP
lines = cv2.HoughLinesP(edges_2nd, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

if lines is not None:
    for i in range(lines.shape[0]):
        pt1 = (lines[i][0][0], lines[i][0][1])  # starting point coordinates x, y
        pt2 = (lines[i][0][2], lines[i][0][3])  # ending point coordinates, always 0 in the middle
        cv2.line(cropped_image, pt1, pt2, (255, 255, 255), 6, cv2.LINE_AA)

cv2.imshow("A", cropped_image)
cv2.waitKey(0)

# Split the image into a 9x4 grid
print(cropped_image.shape)
height, width, _ = cropped_image.shape
cell_height = height // 8
cell_width = width // 1

for row in range(8):
    for col in range(1):
        # Calculate the top-left and bottom-right coordinates of the image to be split
        top_left = (col * cell_width, row * cell_height)
        bottom_right = ((col + 1) * cell_width, (row + 1) * cell_height)

        # Split the image
        cell_image = cropped_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        
        # Resize cropped images for the model's format.
        #cell_image = cv2.resize(cell_image, dsize=(420, 36), interpolation=cv2.INTER_LINEAR)
        #cell_image = cv2.resize(cell_image, dsize=(420,36), interpolation=cv2.INTER_AREA)
        cell_image = cv2.resize(cell_image, (420, 36))

        # Save the split image
        cv2.imwrite(f"cropped_img/cell_{row}_{col}.jpg", cell_image)

        # Display the split image
        cv2.imshow(f"Cell {row}-{col}", cell_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
