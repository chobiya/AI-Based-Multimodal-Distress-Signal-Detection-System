import cv2
import mediapipe as mp
import webbrowser

# Emergency trigger flag
triggered = False

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

print("📸 Show your open palm to trigger SOS")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to access webcam.")
        break

    image = cv2.flip(image, 1)  # mirror image
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get y-position of landmarks for fingers
            finger_tips_ids = [8, 12, 16, 20]
            fingers_up = 0

            for tip_id in finger_tips_ids:
                if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                    fingers_up += 1

            # Thumb check
            if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
                fingers_up += 1

            if fingers_up == 5 and not triggered:
                print("🖐 Open palm detected! Triggering SOS...")
                webbrowser.open("https://www.google.com/maps")
                triggered = True

    cv2.imshow('Gesture Detection - SOS', image)

    if cv2.waitKey(5) & 0xFF == 27:  # press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()