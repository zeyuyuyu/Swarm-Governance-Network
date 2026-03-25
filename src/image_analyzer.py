import cv2
import numpy as np
from deepface import DeepFace
from tensorflow.keras.models import load_model
from scipy.spatial import distance

class ImageAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_model = load_model('models/emotion_model.h5')
        self.facial_landmarks = None
    
    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces

    def analyze_emotion(self, image):
        try:
            analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            return analysis[0]['emotion']
        except Exception as e:
            print(f'Error analyzing emotion: {str(e)}')
            return None

    def calculate_emotion_intensity(self, face_region):
        """Calculate emotion intensity based on facial muscle activation"""
        landmarks = self._get_facial_landmarks(face_region)
        if landmarks is None:
            return 0.0
        
        # Calculate key distances between facial landmarks
        eye_dist = self._calculate_eye_distance(landmarks)
        mouth_dist = self._calculate_mouth_distance(landmarks)
        brow_dist = self._calculate_brow_distance(landmarks)
        
        # Compute intensity score (0-1) based on facial feature movements
        intensity = (eye_dist + mouth_dist + brow_dist) / 3.0
        return min(max(intensity, 0.0), 1.0)

    def _get_facial_landmarks(self, face_img):
        """Extract 68 facial landmarks using dlib"""
        try:
            face_img = cv2.resize(face_img, (224, 224))
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
            
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            
            if len(faces) > 0:
                landmarks = predictor(gray, faces[0])
                return np.array([[p.x, p.y] for p in landmarks.parts()])
            return None
        except Exception as e:
            print(f'Error detecting landmarks: {str(e)}')
            return None

    def _calculate_eye_distance(self, landmarks):
        """Calculate normalized eye openness"""
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]
        
        left_dist = distance.euclidean(left_eye[1], left_eye[5])
        right_dist = distance.euclidean(right_eye[1], right_eye[5])
        
        return (left_dist + right_dist) / 2.0

    def _calculate_mouth_distance(self, landmarks):
        """Calculate normalized mouth openness"""
        mouth = landmarks[48:68]
        height = distance.euclidean(mouth[3], mouth[9])
        width = distance.euclidean(mouth[0], mouth[6])
        return height / width

    def _calculate_brow_distance(self, landmarks):
        """Calculate normalized brow movement"""
        left_brow = landmarks[17:22]
        right_brow = landmarks[22:27]
        
        left_dist = distance.euclidean(left_brow[0], left_brow[-1])
        right_dist = distance.euclidean(right_brow[0], right_brow[-1])
        
        return (left_dist + right_dist) / 2.0

    def get_emotion_analysis(self, image):
        """Complete emotion analysis with intensity"""
        faces = self.detect_faces(image)
        results = []
        
        for (x, y, w, h) in faces:
            face_region = image[y:y+h, x:x+w]
            emotions = self.analyze_emotion(face_region)
            intensity = self.calculate_emotion_intensity(face_region)
            
            if emotions:
                result = {
                    'emotions': emotions,
                    'intensity': intensity,
                    'position': {'x': x, 'y': y, 'width': w, 'height': h}
                }
                results.append(result)
        
        return results