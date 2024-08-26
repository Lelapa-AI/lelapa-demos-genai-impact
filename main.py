import os
import numpy as np
from data_processing import DataCollector, DataPreprocessor
from model import ActionModel
from predictor import RealTimePredictor
from translation import translation

if __name__ == "__main__":
    # Define paths and parameters
    DATA_PATH = os.path.join(os.getcwd(), "data")
    ACTIONS = np.array(['hello', 'thanks', 'iloveyou'])
    NO_SEQUENCES = 30
    SEQUENCE_LENGTH = 30

    # Data Collection
    collector = DataCollector(DATA_PATH, ACTIONS, NO_SEQUENCES, SEQUENCE_LENGTH,   
                              new_actions=[])
    collector.setup_folders()
    collector.collect_data()

    # Data Preprocessing
    preprocessor = DataPreprocessor(DATA_PATH, ACTIONS, SEQUENCE_LENGTH)
    X_train, X_test, y_train, y_test = preprocessor.preprocess_data()

    # Model Training
    model_handler = ActionModel(ACTIONS)
    model_handler.train_model(X_train, y_train)
    model_handler.save_model('action10.keras')

    # Model Evaluation
    model_handler.evaluate_model(X_test, y_test)
    
    model_handler = ActionModel(ACTIONS)
    model_handler.load_model(os.path.join(os.getcwd(), "action1.keras"))  # Load the model

    # Real-Time Prediction
    predictor = RealTimePredictor(model_handler.model, ACTIONS)
    predictor.predict_in_real_time()
    word = predictor.get_word()
    translation(word[0])
