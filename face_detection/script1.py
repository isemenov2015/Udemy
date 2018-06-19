import cv2

img = cv2.imread('galaxy.jpg', 0)

print(type(img))
print(img.shape)

coef = .8
resized_image = cv2.resize(img, (int(img.shape[0] * coef), int(img.shape[1] * coef)))
cv2.imshow("Image", resized_image)
cv2.imwrite("Galaxy_resized.jpg", resized_image)
cv2.waitKey(5000)
cv2.destroyAllWindows()
