import os
import numpy as np

Data_path = "data"
actions = np.array(["hello", "thanks", "IloveYou"])
no_sequence = 30
sequence_length = 30

def create_paths():
    for action in actions:
        for sequence in range(no_sequence):
            try:
                # Create the path for each action and sequence
                path = os.path.join(Data_path, action, str(sequence))
                os.makedirs(path, exist_ok=True)  # Create directories, ignore if they already exist
                print(f"Created path: {path}")
            except Exception as e:
                # Print the exception for debugging purposes
                print(f"Error creating path {path}: {e}")

create_paths()
