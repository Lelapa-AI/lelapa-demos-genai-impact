import cv2
import numpy as np
import asyncio
from utils import MediapipeUtils
import time
from translation import translation
from vulavula.common.error_handler import VulavulaError

class RealTimePredictor:
    def __init__(self, model, actions):
        self.model = model
        self.actions = actions
        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.5
        self.colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245), (192, 192, 192)]
        self.last_two_words_found = False
        self.word = []
        self.paused = False
    

    async def prob_viz(self, image, res, colors):
        output_frame = image.copy()
        for num, prob in enumerate(res):
            cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
            cv2.putText(output_frame, self.actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return output_frame

    async def countdown_thread(self):
        secs = 5
        while secs > 0:
            print(f"countdown {secs}")
            secs -= 1
            await asyncio.sleep(1)

    async def predict_in_real_time(self):
        cap = cv2.VideoCapture(0)
        utils = MediapipeUtils()

        while True:
            
            ret, frame = cap.read()
            if not ret:
                break
            
            image, results = utils.mediapipe_detection(frame)
            utils.draw_styled_landmarks(image, results)

            if self.paused == False:
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
                            self.word.append(self.sentence[-1])
                            key_word = self.sentence[-1]

                            try:
                                await translation(key_word)
                            except VulavulaError as e:
                                if '429' in str(e):
                                    print("API call limit exceeded. Please use a new API key or contact support.")
                                else:
                                    print(f"An error occurred: {e}")

                    self.paused = True
                    self.last_prediction_time = time.time()
                    await asyncio.gather(self.countdown_thread())
                    self.paused = False

                    if len(self.sentence) > 5:
                        self.sentence = self.sentence[-5:]

                    image = await self.prob_viz(image, res, self.colors)

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

    def get_word(self):
        return self.word
