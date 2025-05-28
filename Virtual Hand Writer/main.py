import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class VirtualWriter:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Virtual Hand Writer")
        
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Create canvas and drawing variables
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='black')
        self.canvas.pack(pady=20)
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        
        # Drawing parameters
        self.drawing = False
        self.prev_x = None
        self.prev_y = None
        
        # Buttons
        self.clear_button = tk.Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(pady=10)
        
        # Start the application
        self.update()
        self.root.mainloop()
    
    def clear_canvas(self):
        self.canvas.delete("all")
    
    def update(self):
        # Read frame from webcam
        success, frame = self.cap.read()
        if success:
            # Flip the frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process hand landmarks
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get index finger tip coordinates
                    index_finger_tip = hand_landmarks.landmark[8]
                    x = int(index_finger_tip.x * 800)
                    y = int(index_finger_tip.y * 600)
                    
                    # Get middle finger tip coordinates
                    middle_finger_tip = hand_landmarks.landmark[12]
                    
                    # Check if index finger is raised and middle finger is down (drawing mode)
                    if index_finger_tip.y < hand_landmarks.landmark[6].y and \
                       middle_finger_tip.y > hand_landmarks.landmark[10].y:
                        if not self.drawing:
                            self.drawing = True
                            self.prev_x = x
                            self.prev_y = y
                        else:
                            self.canvas.create_line(
                                self.prev_x, self.prev_y, x, y,
                                fill='white', width=2
                            )
                            self.prev_x = x
                            self.prev_y = y
                    else:
                        self.drawing = False
        
        # Schedule the next update
        self.root.after(10, self.update)
    
    def __del__(self):
        self.cap.release()

if __name__ == "__main__":
    app = VirtualWriter()