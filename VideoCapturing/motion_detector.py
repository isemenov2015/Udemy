import cv2, time
from datetime import datetime
import pandas as pd

first_frame = None
status_list = []
times = []
df = pd.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray, (21, 21), 0)
    status = 0
    if first_frame is None:
        first_frame = gray1
        continue

    delta_frame = cv2.absdiff(first_frame, gray1)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_list.append(status)

    status_list = status_list[-2:] #drop unnecessary extra frames

    if len(status_list) > 1 and ((status_list[-1] == 1 and status_list[-2] == 0) or (status_list[-1] == 0 and status_list[-2] == 1)):
        times.append(datetime.now())
    cv2.imshow("Capturing", gray1)
    cv2.imshow("Delta image", delta_frame)
    cv2.imshow("Thresholded image", thresh_frame)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
#print(status_list)
#print(times)
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index = True)
df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()
