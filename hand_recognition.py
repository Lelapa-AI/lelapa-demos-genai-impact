"""
This script demonstrates the use of MediaPipe's Holistic model for detecting and
visualizing face, pose, and hand landmarks in real-time video streams. The 
script captures video from the default camera, processes each frame using the 
MediaPipe Holistic model, and displays the annotated video feed with detected 
landmarks.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt 
import time 
import mediapipe as mp
import os  

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

# Initialize MediaPipe Holistic model and drawing utilities
mp_holistic = mp.solutions.mediapipe.solutions.holistic
mp_drawing = mp.solutions.mediapipe.solutions.drawing_utils

Data_path = os.getcwd()
actions = np.array(["hello", "thanks", "IloveYou"])
no_sequence = 30
sequence_length = 30

for action in actions:
    for sequence in range(no_sequence):
        for frame_num in range(sequence_length):
            try:
                os.makedirs(os.path.join(Data_path,actions,str(sequence)))
            except:
                pass

def mediapipe_detection(image, model):
    """
    Processes an image with the specified MediaPipe model and returns the 
    processed image and results.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        model (mediapipe.python.solution_base.SolutionBase): The MediaPipe 
        model to use for processing.

    Returns:
        Tuple[numpy.ndarray, mediapipe.python.solution_base.SolutionOutputs]:
            - numpy.ndarray: The processed image in BGR format.
            - mediapipe.python.solution_base.SolutionOutputs: The results from 
            the model's processing.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB
    image.flags.writeable = False  # Make the image read-only
    results = model.process(image)  # Process the image with the model
    image.flags.writeable = True  # Make the image writable again
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert image back to BGR
    return image, results

def draw_landmarks(image, results):
    """
    Draws landmarks on the image using MediaPipe's drawing utilities.

    Parameters:
        image (numpy.ndarray): The image on which landmarks will be drawn.
        results (mediapipe.python.solution_base.SolutionOutputs): The results 
        containing landmarks.
    """
    # Draw face landmarks
    mp_drawing.draw_landmarks(
        image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
        mp_drawing.DrawingSpec(color=(80,213,90), thickness=1, circle_radius=1)
    )
    
    # Draw pose landmarks
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(53,56,38), thickness=1, circle_radius=4),
        mp_drawing.DrawingSpec(color=(100,245,78), thickness=1, circle_radius=2)
    )
    
    # Draw right hand landmarks
    mp_drawing.draw_landmarks(
        image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(100,64,90), thickness=1, circle_radius=4),
        mp_drawing.DrawingSpec(color=(150,80,75), thickness=1, circle_radius=2)
    )
    
    # Draw left hand landmarks
    mp_drawing.draw_landmarks(
        image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(150,245,75), thickness=1, circle_radius=4),
        mp_drawing.DrawingSpec(color=(220,76,56), thickness=1, circle_radius=2)
    )

def extract_keypoints(results):
    """
    Extracts and concatenates keypoints from the results into a single numpy 
    array.

    Parameters:
        results (mediapipe.python.solution_base.SolutionOutputs): The results 
        containing landmarks.

    Returns:
        numpy.ndarray: A flattened array of keypoints for pose, face, left hand,
        and right hand.
    """
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmarks]).flatten() if results.pose_landmarks else np.zeros(132)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmarks]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmarks]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    face = np.array([[res.x, res.y, res.z, res.visibility] for res in results.face_landmarks.landmarks]).flatten() if results.face_landmarks else np.zeros(1404)
    return np.concatenate([pose, face, lh, rh])

# Capture video from the default camera
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for action in actions:
        for sequence in range(no_sequence):
            for frame_num in range(sequence_length):
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)  # Flip the frame horizontally
                
                image, results = mediapipe_detection(frame, holistic)  # Process the frame
                draw_landmarks(image, results)  # Draw landmarks on the frame
                
                if frame_num == 0:
                    cv2.putText(image, "starting collection", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA )
                    cv2.putText(image, f"collecting frames for {action} video number {sequence}", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA )
                    cv2.imshow("opencv feed", image)
                    cv2.waitKey(2000)
                else:
                    cv2.putText(image, "starting collection", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA )
                    
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(Data_path, action, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)
                    cv2.imshow("feed", image)  # Show the image with landmarks
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()


label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequence):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(Data_path, action, str(sequence), f"{frame_num}.npy"))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

x = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.05)

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

res = [.7, 0.2, 0.1]
actions[np.argmax(res)]
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, Y_train, epochs=2000, callbacks=[tb_callback])

res = model.predict(X_test)