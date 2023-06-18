import cv2
import numpy as np

# 이미지 로드
image = cv2.imread('sample.JPG')

# 이미지를 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이진화
_, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((3, 3), np.uint8)
dilation = cv2.dilate(thresh, kernel, iterations=2)
dilation = cv2.erode(dilation, kernel, iterations=3)
thresh = dilation
#cv2.imshow('dilation',dilation)
#cv2.waitKey(0)
# 윤곽선 찾기
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 바운딩 박스 추출
bounding_boxes = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    bounding_boxes.append((x, y, x + w, y + h))

# 추출된 바운딩 박스 그리기
for bbox in bounding_boxes:
    x1, y1, x2, y2 = bbox
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

# 결과 이미지 출력
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
