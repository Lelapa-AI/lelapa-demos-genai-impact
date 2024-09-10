# lelapa-demos-genai-impact
Real-Time Action Prediction
This project uses a machine learning model to recognize actions from real-time video input. It integrates OpenCV for video capture, Mediapipe for feature extraction, and a custom model to predict actions based on hand and body movements. It also includes a translation feature to convert recognized actions into text using an external API.

Real-time action recognition from video feed
Visualization of action probabilities
Translation of recognized actions to text
Handles API errors and rate limits
Installation
Clone this repository:

bash
Copy code
git clone <git@github.com:Lelapa-AI/lelapa-demos-genai-impact.git>
Navigate to the project directory:

bash
Copy code
cd <into the project directory>
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Ensure you have the following packages installed:

opencv-python
numpy
mediapipe
translation (replace with the actual package or API wrapper you are using)
Any other dependencies listed in requirements.txt
Usage
Prepare the Model: Ensure you have a trained model saved as action4.keras. You can train your model by following the steps in the if __name__ == "__main__": block in the code.

Run the Predictor: Execute the main script to start real-time action prediction:

bash
Copy code
python main.py
Interactive Features:

Press q to quit the application.
Code Overview
RealTimePredictor Class
__init__: Initializes the predictor with a model and action list.
prob_viz: Visualizes action probabilities on the frame.
countdown_thread: Manages a countdown timer during pauses.
predict_in_real_time: Main loop for real-time prediction and display.
extract_keypoints: Extracts and formats keypoints from Mediapipe results.
get_word: Retrieves the last predicted action.
Data Collection and Model Training
Data collection, preprocessing, and model training sections are commented out but can be activated as needed.
