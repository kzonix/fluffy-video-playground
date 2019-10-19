import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('sudoku.jpg')
print(type(img))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th1 = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY_INV)
th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY_INV, 35, 7)
th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY_INV, 35, 7)

titles = ['Original Image', 'Global Thresholding (v = 127)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [gray, th1, th2, th3]

for i in range(4):
    cur_image = images[i]
    gray32 = np.float32(cur_image)
    dst = cv2.cornerHarris(gray32, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)
    gray32[dst > 0.01 * dst.max()] = [0, 0, 255]

    image = gray32.astype(np.uint8)
    status = cv2.imwrite(f'./{titles[i]}.jpg', image)
    plt.subplot(2, 2, i + 1), plt.imshow(gray32, 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
