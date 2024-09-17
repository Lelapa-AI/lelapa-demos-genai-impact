import os
import numpy as np
from data_processing import DataCollector, DataPreprocessor
from model import ActionModel
from predictor import RealTimePredictor
from translation import translation
from vulavula.common.error_handler import VulavulaError
import actions
import importlib
import asyncio

if __name__ == "__main__":
    # Define paths and parameters
    DATA_PATH = os.path.join(os.getcwd(), "data2")
    ACTIONSS = np.array(actions.ACTIONSS)
    # ACTIONS = np.array(ACTIONSS)
    NO_SEQUENCES = 30
    SEQUENCE_LENGTH = 30
    
    model_handler = ActionModel(ACTIONSS)
    model_handler.load_model(os.path.join(os.getcwd(), "action3.keras"))  # Load the model
    predictor = RealTimePredictor(model_handler.model, ACTIONSS)
    asyncio.run(predictor.predict_in_real_time()) 
