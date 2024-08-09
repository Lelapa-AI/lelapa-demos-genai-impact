import os 
import numpy as np 

Data_path = "data"
actions = np.array(["hello", "thanks", "IloveYou"])
no_sequence = 30
sequence_length = 30

def path_creation():
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
                
                
                
def keypoints_extraction():
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for action in actions:
        for sequence in range(30):
            for frame_num in range(30):
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)  # Flip the frame horizontally
                
                image, results = mediapipe_detection(frame, holistic)  # Process the frame
                draw_landmarks(image, results)  # Draw landmarks on the frame
                
                if frame_num == 0:
                    cv2.putText(image, "starting collection", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA )
                    cv2.putText(image, f"collecting frames for {action} video number {sequence}", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA )
                    cv2.imshow("opencv feed", image)
                    cv2.waitKey(2000)
                else:
                    cv2.putText(image, "starting collection", (120,200),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA )
                    
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(Data_path, action, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)
                    cv2.imshow("feed", image)  # Show the image with landmarks
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()