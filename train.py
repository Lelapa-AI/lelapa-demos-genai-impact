
import os
import numpy as np
from data_processing import DataCollector, DataPreprocessor
from model import ActionModel
import actions
import importlib

DATA_PATH = os.path.join(os.getcwd(), "data2")
ACTIONSS = np.array(actions.ACTIONSS)
# ACTIONS = np.array(ACTIONSS)
NO_SEQUENCES = 30
SEQUENCE_LENGTH = 30

DataCollector.new_act(os.path.join(os.getcwd(), "actions.py"), "ACTIONSS")
# Data Collection
importlib.reload(actions)
ACTIONSS = np.array(actions.ACTIONSS)
collector = DataCollector(DATA_PATH, ACTIONSS, NO_SEQUENCES, SEQUENCE_LENGTH)
collector.setup_folders()
collector.collect_data()

# Data Preprocessing
preprocessor = DataPreprocessor(DATA_PATH, ACTIONSS, SEQUENCE_LENGTH)
X_train, X_test, y_train, y_test = preprocessor.preprocess_data()

# Model Training
model_handler = ActionModel(ACTIONSS)
model_handler.train_model(X_train, y_train)
model_handler.save_model('action4.keras')

# Model Evaluation
model_handler.evaluate_model(X_test, y_test)