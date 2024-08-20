import cv2
import numpy as np
import os
import mediapipe as mp
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from translation import translation
import tensorflow as tf
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# from tensorflow.keras.callbacks import tf.keras.callbacks.TensorBoard
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from scipy import stats

to_categorical = tf.keras.utils.to_categorical

word = []
class MediapipeUtils:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def mediapipe_detection(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.holistic.process(image_rgb)
        image_rgb.flags.writeable = True
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        return image_bgr, results

    def draw_landmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION)
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

    def draw_styled_landmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION,
                                        self.mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                        self.mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1))
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                        self.mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2))
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                        self.mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2))
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                        self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

class DataCollector:
    def __init__(self, data_path, actions, no_sequences, sequence_length):
        self.data_path = data_path
        self.actions = actions
        self.no_sequences = no_sequences
        self.sequence_length = sequence_length

    def setup_folders(self):
        for action in self.actions:
            dirmax = np.max(np.array(os.listdir(os.path.join(self.data_path, action))).astype(int), initial=0)
            for sequence in range(1, self.no_sequences + 1):
                try:
                    os.makedirs(os.path.join(self.data_path, action, str(dirmax + sequence)))
                except FileExistsError:
                    pass

    def collect_data(self):
        cap = cv2.VideoCapture(0)
        utils = MediapipeUtils()

        for action in self.actions:
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
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
        return np.concatenate([pose, face, lh, rh])

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

class ActionModel:
    def __init__(self, actions):
        self.actions = actions
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662)))
        model.add(tf.keras.layers.LSTM(128, return_sequences=True, activation='relu'))
        model.add(tf.keras.layers.LSTM(64, return_sequences=False, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(len(self.actions), activation='softmax'))
        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        return model

    def train_model(self, X_train, y_train, epochs=700):
        log_dir = os.path.join('Logs')
        tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
        self.model.fit(X_train, y_train, epochs=epochs, callbacks=[tb_callback])

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = tf.keras.models.load_model(path)

    def evaluate_model(self, X_test, y_test):
        yhat = self.model.predict(X_test)
        ytrue = np.argmax(y_test, axis=1).tolist()
        yhat = np.argmax(yhat, axis=1).tolist()
        print(multilabel_confusion_matrix(ytrue, yhat))
        print(accuracy_score(ytrue, yhat))

class RealTimePredictor:
    def __init__(self, model, actions):
        self.model = model
        self.actions = actions
        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.5
        self.colors = [(245,117,16), (117,245,16), (16,117,245)]
        self.last_two_words_found = False
    def prob_viz(self, image, res, colors):
        output_frame = image.copy()
        for num, prob in enumerate(res):
            cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
            cv2.putText(output_frame, self.actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return output_frame

    def predict_in_real_time(self):
        cap = cv2.VideoCapture(0)
        utils = MediapipeUtils()

        while cap.isOpened():
            ret, frame = cap.read()
            image, results = utils.mediapipe_detection(frame)
            utils.draw_styled_landmarks(image, results)

            keypoints = self.extract_keypoints(results)
            self.sequence.append(keypoints)
            self.sequence = self.sequence[-30:]

            if len(self.sequence) == 30:
                res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
                print(self.actions[np.argmax(res)])
                self.predictions.append(np.argmax(res))

                if np.unique(self.predictions[-10:])[0] == np.argmax(res):
                    if res[np.argmax(res)] > self.threshold:
                        if len(self.sentence) > 0:
                            if self.actions[np.argmax(res)] != self.sentence[-1]:
                                self.sentence.append(self.actions[np.argmax(res)])
                        else:
                            self.sentence.append(self.actions[np.argmax(res)])
                            # if self.sentence == 2:
                            #     word.append(self.sentence[-2])
                            #     # return self.sentence[-1]
                            #     break
                if len(self.sentence) == 2:
                    word.append(self.sentence[-1])
                    self.last_two_words_found = True
                    
                if len(self.sentence) > 5:
                    self.sentence = self.sentence[-5:]
                if self.last_two_words_found:
                    break

                image = self.prob_viz(image, res, self.colors)

            cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
            cv2.putText(image, ' '.join(self.sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('OpenCV Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
        return np.concatenate([pose, face, lh, rh])

if __name__ == "__main__":
    # Define paths and parameters
    DATA_PATH = "/home/wtc/Desktop/Lelapa/lelapa-demos-genai-impact/data2"
    ACTIONS = np.array(['hello', 'thanks', 'iloveyou'])
    NO_SEQUENCES = 30
    SEQUENCE_LENGTH = 30

    # # Data Collection
    # collector = DataCollector(DATA_PATH, ACTIONS, NO_SEQUENCES, SEQUENCE_LENGTH)
    # collector.setup_folders()
    # collector.collect_data()

    # # Data Preprocessing
    # preprocessor = DataPreprocessor(DATA_PATH, ACTIONS, SEQUENCE_LENGTH)
    # X_train, X_test, y_train, y_test = preprocessor.preprocess_data()

    # # Model Training
    # model_handler = ActionModel(ACTIONS)
    # model_handler.train_model(X_train, y_train)
    # model_handler.save_model('action10.keras')

    # Model Evaluation
    # model_handler.evaluate_model(X_test, y_test)
    
    model_handler = ActionModel(ACTIONS)
    model_handler.load_model('/home/wtc/Desktop/Lelapa/lelapa-demos-genai-impact/action10.keras')  # Load the model

    # Real-Time Prediction
    predictor = RealTimePredictor(model_handler.model, ACTIONS)
    predictor.predict_in_real_time()
    translation(word[0])
