from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os 

Data_path = "data"
actions = np.array(["hello", "thanks", "IloveYou"])

label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in range(30):
        window = []
        for frame_num in range(30):
            res = np.load(os.path.join(Data_path, action, str(sequence), f"{frame_num}.npy"))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

x = np.array(sequences)
y = tf.keras.utils.to_categorical(labels).astype(int)
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.05)

log_dir = os.path.join('Logs')
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(64, return_sequences=True, activation='relu', input_shape=(30,1662)))
model.add(tf.keras.layers.LSTM(128, return_sequences=True, activation='relu'))
model.add(tf.keras.layers.LSTM(64, return_sequences=False, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(actions.shape[0], activation='softmax'))

res = [.7, 0.2, 0.1]
actions[np.argmax(res)]
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, Y_train, epochs=2000, callbacks=[tb_callback])

res = model.predict(X_test)
model.save('action.h5')