import tensorflow as tf
import os
import numpy as np
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score

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
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0002)
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        return model

    def train_model(self, X_train, y_train, epochs=250):
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
