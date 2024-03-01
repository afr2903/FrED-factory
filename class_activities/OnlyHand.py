import cv2
import mediapipe as mp

#Config camara
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.7) as hands:
    
    while True:
        ret, frame = cap.read()
        #Obtain the dimension of the video
        height, width, _ = frame.shape
        if ret == False:
            break
            
        height, width, _ = frame.shape
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks is not None:
        
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS, 
                       mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                       mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),)
                
                print(hand.landmark[mp_hands.HandLandmark.THUMB_TIP])

                x1 = int(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
                y1 = int(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)
                x2 = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                y2 = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                dist = ((x2-x1)**2 + (y2-y1)**2)**0.5
                if dist < 50:
                    
        
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
            
cap.release()
cv2.destroyAllWindows()