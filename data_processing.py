import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import tensorflow as tf
from utils import MediapipeUtils
to_categorical = tf.keras.utils.to_categorical


class DataCollector:
    
    def __init__(self, data_path, actions, no_sequences, sequence_length):
        self.data_path = data_path
        self.actions = actions
        self.no_sequences = no_sequences
        self.sequence_length = sequence_length
        self.new_actions = []

    def setup_folders(self):
        for action in self.actions:
            
            if os.path.exists(os.path.join(self.data_path, f"{action}")):
                continue
            else:
                self.new_actions.append(action)
                for sequence in range(1, self.no_sequences + 1):
                    try:
                        # os.makedirs(os.path.join(self.data_path, action, str(sequence)))
                        # dirmax = np.max(np.array(os.listdir(os.path.join(self.data_path,
                        # action))).astype(int), initial=0)
                        os.makedirs(os.path.join(self.data_path, action, str(sequence)))
                    except FileExistsError:
                        pass

    def collect_data(self):
        cap = cv2.VideoCapture(0)
        utils = MediapipeUtils()

        for action in self.new_actions:
            for sequence in range(1, self.no_sequences + 1):
                for frame_num in range(self.sequence_length):
                    ret, frame = cap.read()
                    image, results = utils.mediapipe_detection(frame)
                    utils.draw_styled_landmarks(image, results)

                    if frame_num == 0:
                        cv2.putText(image, 'STARTING COLLECTION', (120, 200),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                        cv2.putText(image, f'Collecting frames for {action} Video Number {sequence}', (15, 12),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imshow('OpenCV Feed', image)
                        cv2.waitKey(500)
                    else:
                        cv2.putText(image, f'Collecting frames for {action} Video Number {sequence}', (15, 12),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        cv2.imshow('OpenCV Feed', image)

                    keypoints = self.extract_keypoints(results)
                    npy_path = os.path.join(self.data_path, action, str(sequence), f'{frame_num}.npy')
                    np.save(npy_path, keypoints)

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

        cap.release()
        cv2.destroyAllWindows()

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] \
            for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
        return np.concatenate([pose, face, lh, rh])

    def new_act(file_path, list_name):
        new_elements = input("What are you trying to train : ").lower().strip()
        with open(file_path, 'r') as file:
            lines = file.readlines()

        modified = False
        for i, line in enumerate(lines):
            line = line.strip()
            if line[:8] == "ACTIONSS":
                lines[i] = line[:-1] + ", " + "'" + f"{new_elements}" + "'" + "]\n"
                modified = True
                break
         
        if modified:
            with open(file_path, 'w') as file:
                file.writelines(lines)
            print(f"List '{list_name}' modified successfully in {file_path}.")

        else:
            raise ValueError(f"List '{list_name}' not found in {file_path}.")
        
class DataPreprocessor:
    def __init__(self, data_path, actions, sequence_length):
        self.data_path = data_path
        self.actions = actions
        self.sequence_length = sequence_length

    def preprocess_data(self):
        label_map = {label: num for num, label in enumerate(self.actions)}
        sequences, labels = [], []

        for action in self.actions:
            for sequence in np.array(os.listdir(os.path.join(self.data_path, action))).astype(int):
                window = []
                for frame_num in range(self.sequence_length):
                    res = np.load(os.path.join(self.data_path, action, str(sequence), f"{frame_num}.npy"))
                    window.append(res)
                sequences.append(window)
                labels.append(label_map[action])

        X = np.array(sequences)
        y = to_categorical(labels).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

        return X_train, X_test, y_train, y_test

