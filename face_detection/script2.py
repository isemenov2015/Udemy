import cv2
import glob

image_list = glob.glob('*.jpg')

for img_file in image_list:
    img = cv2.imread(img_file, 1)
    resized_image = cv2.resize(img, (100, 100))
    cv2.imwrite("_" + img_file, resized_image)
    cv2.imshow("Image", resized_image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
