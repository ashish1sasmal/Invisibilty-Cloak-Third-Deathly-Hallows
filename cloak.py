import time
import cv2
import numpy as np
import imutils
from live_cam import live

# time.sleep(2)
count = 0
background = 0
for i in range(60):
	background  =live()
background = np.flip(background,axis=1)

while True:
	img = live()
	count+=1
	img = np.flip(img,axis=1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_red = np.array([0, 125, 50])
	upper_red = np.array([10, 255,255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red)

	lower_red = np.array([170, 120, 70])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv, lower_red, upper_red)

	mask1 = mask1 + mask2

	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

	mask2 = cv2.bitwise_not(mask1)
	res1 = cv2.bitwise_and(img, img, mask=mask2)

	res2 = cv2.bitwise_and(background, background, mask=mask1)

	finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
	finalOutput = imutils.resize(finalOutput,width=1280)
	cv2.imshow("magic", finalOutput)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
