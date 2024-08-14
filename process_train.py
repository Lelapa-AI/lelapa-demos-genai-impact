import numpy as np
import tensorflow as tf
import os 

from sklearn.model_selection import train_test_split
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score

Data_path = "data"
actions = np.array(["hello", "thanks", "IloveYou"])

label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []

max_length = 2130
count = 0
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(Data_path, action))).astype(int):
        window = []
        for frame_num in range(30):
            path = os.path.join(Data_path, action, str(sequence), f"{frame_num}.npy")
            res = np.load(path)
            # if res.shape[0] == 2130:
            if res.shape[0] < max_length:
                # Pad the array
                padding = max_length - res.shape[0]
                res_padded = np.pad(res, (0, padding), mode='constant', constant_values=0)
            elif res.shape[0] > max_length:
                # Truncate the array
                res_padded = res[:max_length]
            else:
                res_padded = res
        window.append(res_padded)
        sequences.append(window)
        labels.append(label_map[action])
        
        
# print(np.array(sequences).shape)

x = np.array(sequences)
print(x.shape)
y = tf.keras.utils.to_categorical(labels).astype(int)
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.05)

log_dir = os.path.join('Logs')
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(64, return_sequences=True, activation='relu', input_shape=(30,2130)))
model.add(tf.keras.layers.LSTM(128, return_sequences=True, activation='relu'))
model.add(tf.keras.layers.LSTM(64, return_sequences=False, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(actions.shape[0], activation='softmax'))

res = [0.7, 0.2, 0.1]
actions[np.argmax(res)]
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=700, callbacks=[tb_callback])

res = model.predict(X_test)
model.save('action4.keras')

# res = model.predict(X_test)
# actions[np.argmax(res[4])]

# model.save('action.h5')


def matrix(X_test, y_test):
    yhat = model.predict(X_test)
    ytrue = np.argmax(y_test, axis=1).tolist()
    yhat = np.argmax(yhat, axis=1).tolist()
    multilabel_confusion_matrix(ytrue, yhat)