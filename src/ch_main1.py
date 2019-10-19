import cv2
import numpy as np
import random
import sys

img = cv2.imread('sudoku.jpg')

height, width, channels = img.shape

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
th3 = cv2.adaptiveThreshold(gray.copy(), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 35, 17)

edges = cv2.Canny(th3, 50, 150, apertureSize=3)
cv2.imwrite('houghlines1.jpg', edges)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 155)

prev_line = None


def coordinates(rho, theta):
    global x1, y1, x2, y2
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    return x1, x2, y1, y2


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


points = list()
for line in lines:
    for rho, theta in line:
        x1, x2, y1, y2 = coordinates(rho, theta)
        points.append(((x1, y1), (x2, y2)))
        # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

points.sort(key=lambda x: x[0][0] + x[1][0])

points_length = len(points)

res = list()


def get_diff(left, right):
    diff = 0
    diff += abs(left[0][0]) - abs(right[0][0])
    diff += abs(left[0][1]) - abs(right[0][1])
    diff += abs(left[1][0]) - abs(right[1][0])
    diff += abs(left[1][1]) - abs(right[1][1])
    return diff


for index, point in enumerate(points):
    prev_diff = None
    next_diff = None
    if index > 0:
        previous_ = points[index - 1]
        prev_diff = get_diff(point, previous_)
        prev_diff = abs(prev_diff)

    if index < (points_length - 1):
        next_ = points[index + 1]
        next_diff = get_diff(point, next_)
        next_diff = abs(next_diff)

    if next_diff is not None and prev_diff is not None:
        if next_diff >= 100 or prev_diff >= 100:
            res.append(point)

    elif next_diff is not None and prev_diff is None:
        if next_diff >= 1:
            res.append(point)

    elif prev_diff is not None and next_diff is None:
        if prev_diff >= 1:
            res.append(point)

    else:
        res.append(point)


intersected_points = list()
for l1 in res:
    for l2 in res:
        try:
            x, y = line_intersection(l1, l2)
            if width >= int(x) >= 0 and height >= int(y) >= 0:
                intersected_points.append((int(x), int(y)))

        except Exception:
            continue


for intersected_point in intersected_points:
    pass

#
# cv2.circle(img, (b_r[0], b_r[1]), 15,
#            (1, 255, 255), thickness=-1, lineType=1
#            )
#
# cv2.circle(img, (b_l[0], b_l[1]), 15,
#            (255, 255, 222), thickness=-1, lineType=1
#            )
#
# cv2.circle(img, (t_r[0], t_r[1]), 15,
#            (255, 22, 22), thickness=-1, lineType=1
#            )
#
# cv2.circle(img, (t_l[0], t_l[1]), 15,
#            (255, 255, 2), thickness=-1, lineType=1
#            )

for index, r in enumerate(res):
    cv2.line(img, r[0], r[1], (random.randint(23, 255), random.randint(123, 255), random.randint(0, 255)), 2)

for intersected_point in intersected_points:
    cv2.circle(img, (intersected_point[0], intersected_point[1]), 5,
               (random.randint(23, 255), random.randint(123, 255), random.randint(0, 255)), thickness=-1, lineType=1
               )

cv2.imwrite('houghlines3.jpg', img)
