import cv2

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)



video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
totx = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
toty = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"frame res: {totx}x{toty}")

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    count = 0

    # Sort faces based on x-coordinate
    faces = sorted(faces, key=lambda x: x[0])

    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4) # green
        red_square_size = min(w, h) // 3 #start red
        red_x = x + w // 2 - red_square_size // 2
        red_y = y + h // 2 - red_square_size // 2 + h//5
        cv2.rectangle(vid, (red_x, red_y), (red_x + red_square_size, red_y + red_square_size), (0, 0, 255), 2) # red
        # count number
        #print(f"w,h={w},{h}")
        xmin = red_x
        xmax = red_x + red_square_size
        ymin = red_y
        ymax = red_y + red_square_size
        print(f"x,y for AIM POINT={totx//2},{toty//2}")
        print(f"x range red: {xmin}-{xmax}")
        print(f"y range red: {ymin}-{ymax}")
        if totx//2 < xmax and totx//2 > xmin:
            print("x good")
            xgood = True
        else:
            xgood = False
        if toty//2 < ymax and toty//2 > ymin:
            print("y good")
            ygood = True
        else:
            ygood = False
        if ygood and xgood:
            print(f"Aim good for FACE: {count}")

        if 3*w/550 > 1:
            size = 4*w/550
        else:
            size = 1.0
        cv2.putText(vid, 'Face ' + str(count), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, size, (0, 255, 0), 2)


    cv2.line(vid, (totx // 2, 0), (totx // 2, toty), (255, 0, 0), 3)  # Blue line V
    cv2.line(vid, (0, toty // 2), (totx, toty // 2), (255, 0, 0), 3)  # Blue line H
    return faces

while True:
    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully
    faces = detect_bounding_box(
        video_frame
    )  # apply the function we created to the video frame
    cv2.imshow(
        "Face tracking", video_frame
    )  # display the processed frame in a window named "My Face Detection Project"
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
