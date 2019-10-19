import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('sudoku.jpg', 0)
img = cv2.medianBlur(img, 1)

ret, th1 = cv2.threshold(img.copy(), 75, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img.copy(), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 35, 7)
th3 = cv2.adaptiveThreshold(img.copy(), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 35, 7)

titles = ['Original Image', 'Global Thresholding (v = 127)',
          'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

contours, hierarchy = cv2.findContours(th3.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
th3c = cv2.drawContours(th3.copy(), contours, -1, (23, 255, 23), 3)

images = [img, th1, th2, th3c]

for i in range(4):
    status = cv2.imwrite(f'./{titles[i]}.jpg', images[i])
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
