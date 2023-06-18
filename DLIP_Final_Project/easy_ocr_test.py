import easyocr
import os

# EasyOCR setting
reader = easyocr.Reader(['ko'])  # set the korean

# image path
image_folder = 'C:/Users/ririk/Desktop/DLIP_Final_Project/easyocr_test_image'

# path
image_paths = [os.path.join(image_folder, f'image{i}.jpg') for i in range(1, 51)]

# result
for image_path in image_paths:
    result = reader.readtext(image_path)
    print(f"=== Results for {image_path} ===")
    for text in result:
        print(text)
    print()
