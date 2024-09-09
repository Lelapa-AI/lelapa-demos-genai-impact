import os
import numpy as np
from data_processing import DataCollector, DataPreprocessor
from model import ActionModel
from predictor import RealTimePredictor
from translation import translation
from vulavula.common.error_handler import VulavulaError
import actions
import importlib

if __name__ == "__main__":
    # Define paths and parameters
    DATA_PATH = os.path.join(os.getcwd(), "data2")
    ACTIONSS = np.array(actions.ACTIONSS)
    # ACTIONS = np.array(ACTIONSS)
    NO_SEQUENCES = 30
    SEQUENCE_LENGTH = 30
    
    determine_action = input("Are you training the model (Yes/No)").lower().strip()
    if determine_action[0] == "y":
        
        # DataCollector.new_act(os.path.join(os.getcwd(), "actions.py"), "ACTIONSS")
        # # Data Collection
        # importlib.reload(actions)
        # ACTIONSS = np.array(actions.ACTIONSS)
        # collector = DataCollector(DATA_PATH, ACTIONSS, NO_SEQUENCES, SEQUENCE_LENGTH)
        # collector.setup_folders()
        # collector.collect_data()

        # Data Preprocessing
        preprocessor = DataPreprocessor(DATA_PATH, ACTIONSS, SEQUENCE_LENGTH)
        X_train, X_test, y_train, y_test = preprocessor.preprocess_data()

        # Model Training
        model_handler = ActionModel(ACTIONSS)
        model_handler.train_model(X_train, y_train)
        model_handler.save_model('action4.keras')

        # Model Evaluation
        model_handler.evaluate_model(X_test, y_test)
    
    else:
        #Real-time prediction
        model_handler = ActionModel(ACTIONSS)
        model_handler.load_model(os.path.join(os.getcwd(), "action4.keras"))  # Load the model
        predictor = RealTimePredictor(model_handler.model, ACTIONSS)
        predictor.predict_in_real_time()
        word = predictor.get_word()

        try:
            translation(word[0])
        except VulavulaError as e:
            if '429' in str(e):
                print("API call limit exceeded. Please use a new API key or contact support to upgrade your plan.")
            else:
                print(f"An error occurred: {e}")