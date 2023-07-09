import pyttsx3
import cv2
import threading
import mediapipe as mp
import numpy as np
import pyautogui
import subprocess
import os


# Initialize mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

# Define the points for the polygon
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]

counter_left_eye = 0
counter_right_eye = 0
counter_mouth = 0
is_mouth_open_counter = 0
mouth_text = ""
click_text = ""

windowName = "Handless Computer Control"

EYE_CLOSED_THRESHOLD = 6
MOUTH_OPEN_THRESHOLD = 38


flag_file = "first_run.txt"
intro_text = '''Welcome to the Handless Computer Control, please read the following:
- How to use the app:
  - To exit the app, press q.
  - Turn your face left, right, up, or down to control the mouse accordingly.
  - To left-click, shut your left eye.
  - To right-click, shut your right eye.
  - To drag, open your mouth and move your face in any direction.
  - To use the keyboard, hover on any key, and after 2 seconds, the key will be pressed.
  - You don't need to click on the key, just hover on it.
  - Both the mouse and keyboard apps will be opened after this message.
  - Enjoy!
- This message will auto close in a few seconds or press "Ok" to continue.
'''


if not os.path.exists(flag_file):
    def speak_intro():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # set the speed of the speech
        engine.say(intro_text)
        engine.runAndWait()

    threading.Thread(target=speak_intro).start()
    pyautogui.alert(intro_text, 'Welcome!', button='Ok', timeout=50000)

    # Create the flag file
    with open(flag_file, "w") as f:
        pass


def open_keyboard():
    subprocess.run(["keyboard.exe"])

threading.Thread(target=open_keyboard).start()


def ear_value(value):
    EYE_CLOSED_THRESHOLD = value


def mar_value(value):
    MOUTH_OPEN_THRESHOLD = value


cv2.namedWindow(windowName)
cv2.createTrackbar("Eyes Val", windowName, 6, 20, ear_value)
cv2.createTrackbar("Mouth Val", windowName, 38, 55, mar_value)


while cap.isOpened():
    success, image = cap.read()

    # Flip the image horizontally for a later selfie-view display
    # Also convert the color space from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False
    
    # Get the result
    results = face_mesh.process(image)
    
    # To improve performance
    image.flags.writeable = True
    
    # Convert the color space from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])  
            
            # Get the landmark points for the left eye, right eye, and lips
            left_eye_points = [results.multi_face_landmarks[0].landmark[i] for i in LEFT_EYE]
            right_eye_points = [results.multi_face_landmarks[0].landmark[i] for i in RIGHT_EYE]
            lips_points = [results.multi_face_landmarks[0].landmark[i] for i in LIPS]

            # Convert the landmark points to pixel coordinates
            h, w, c = image.shape
            left_eye_pixels = np.array([(int(p.x * w), int(p.y * h)) for p in left_eye_points], dtype=np.int32)
            right_eye_pixels = np.array([(int(p.x * w), int(p.y * h)) for p in right_eye_points], dtype=np.int32)
            lips_pixels = np.array([(int(p.x * w), int(p.y * h)) for p in lips_points], dtype=np.int32)

            # Draw the polygon on the image
            cv2.polylines(image, [left_eye_pixels], True, (0, 255, 0), 2)
            cv2.polylines(image, [right_eye_pixels], True, (0, 255, 0), 2)
            cv2.polylines(image, [lips_pixels], True, (0, 255, 0), 2)

            # Draw landmarks for eyes and lips
            cv2.circle(image, tuple(right_eye_pixels[4]), 3, (0, 0, 255), -1)
            cv2.circle(image, tuple(right_eye_pixels[12]), 3, (0, 0, 255), -1)
            cv2.circle(image, tuple(left_eye_pixels[4]), 3, (0, 0, 255), -1)
            cv2.circle(image, tuple(left_eye_pixels[12]), 3, (0, 0, 255), -1)
            cv2.circle(image, tuple(lips_pixels[25]), 3, (0, 0, 255), -1)
            cv2.circle(image, tuple(lips_pixels[16]), 3, (0, 0, 255), -1)


            # Calculate the distance between the top and bottom left eye points
            top_left_eye = right_eye_pixels[4]  # Top left eye landmark index
            bottom_left_eye = right_eye_pixels[12]  # Bottom left eye landmark index
            left_eye_distance = np.linalg.norm(top_left_eye - bottom_left_eye)  # Euclidean distance

            # Calculate the distance between the top and bottom right eye points
            top_right_eye = left_eye_pixels[4]  # Top right eye landmark index
            bottom_right_eye = left_eye_pixels[12]  # Bottom right eye landmark index
            right_eye_distance = np.linalg.norm(top_right_eye - bottom_right_eye)  # Euclidean distance

            # Calculate the distance between the top and bottom lip points
            top_lip = lips_pixels[25]  # Top lip landmark index
            bottom_lip = lips_pixels[16]  # Bottom lip landmark index
            mouth_open_distance = np.linalg.norm(bottom_lip - top_lip)  # Euclidean distance

            # Set a threshold value to determine the mouth-opening gesture
            
            # Convert it to the NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)

            # Convert it to the NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = 1 * img_w

            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            # The Distance Matrix
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360

            # print(y)

            # See where the user's head tilting
            if y < -8:
                text = "Looking Left"
                pyautogui.move(-15, 0)
            elif y > 8:
                text = "Looking Right"
                pyautogui.move(15, 0)
            elif x < -8:
                text = "Looking Down"
                pyautogui.move(0, 15)
            elif x > 8:
                text = "Looking Up"
                pyautogui.move(0, -15)
            else:
                text = "Forward"
                # Check if the left eye is closed
                if left_eye_distance < EYE_CLOSED_THRESHOLD:
                    # Increment the counter
                    counter_left_eye += 1

                    # Check if the counter has reached the threshold value
                    if counter_left_eye == 25:
                        # Perform a left click
                        pyautogui.click()
                        click_text = "Left Click"
                        pyttsx3.speak("Left Click")

                        # Reset the counter
                        counter_left_eye = 0
                else:
                    # Reset the counter
                    counter_left_eye = 0

                # Check if the right eye is closed
                if right_eye_distance < EYE_CLOSED_THRESHOLD:
                    # Increment the counter
                    counter_right_eye += 1

                    # Check if the counter has reached the threshold value
                    if counter_right_eye == 25:
                        # Perform a right click
                        pyautogui.click(button='right')
                        click_text = "Right Click"
                        pyttsx3.speak("Right Click")

                        # Reset the counter
                        counter_right_eye = 0
                else:
                    # Reset the counter
                    counter_right_eye = 0

                # Check if the mouth is open
                if mouth_open_distance > MOUTH_OPEN_THRESHOLD:
                    # Increment the counter
                    counter_mouth += 1

                    # Check if the counter has reached the threshold value
                    if counter_mouth == 45:
                        is_mouth_open_counter += 1
                        if is_mouth_open_counter % 2 != 0:
                            # Perform a drag
                            mouth_text = "Dragging"
                            pyautogui.mouseDown()
                            pyttsx3.speak("Dragging")
                        elif is_mouth_open_counter % 2 == 0:
                            pyautogui.mouseUp()
                            mouth_text = "Not Dragging"
                            pyttsx3.speak("Not Dragging")

                        # Reset the counter
                        counter_mouth = 0
                else:
                    # Reset the counter
                    counter_mouth = 0

            # Display the nose direction
            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
            
            cv2.line(image, p1, p2, (255, 0, 0), 2)

            # Add the text on the image
            cv2.putText(image, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, mouth_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, click_text, (20, 91), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow(windowName, image)


    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
cap.release()
os.system("taskkill /f /im  keyboard.exe")
