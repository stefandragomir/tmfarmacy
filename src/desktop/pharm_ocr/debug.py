
import cv2
  
# read the image file
img = cv2.imread(r"d:\temp\raw\9.jpg", 2)
  
ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite(r"d:\temp\input\9.jpg", bw_img)  
