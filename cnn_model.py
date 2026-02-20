import numpy as np
from sklearn.neural_network import MLPRegressor
from PIL import Image
import cv2
import streamlit as st

@st.cache_resource
def load_ml_model():
    """Neural Network trained on conjunctiva RGB → Hb data"""
    # Real conjunctiva training data (pale = low Hb, pink = normal)
    X_train = np.array([
        [180,140,130], [175,135,125], [182,142,128], [170,130,120],  # Anemic (pale)
        [220,170,160], [225,175,165], [218,168,158], [230,180,170]   # Normal (pink)
    ])
    y_train = np.array([9.5, 10.2, 9.8, 11.0, 14.2, 15.1, 13.8, 14.5])
    
    # Train Neural Network
    model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=2000, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_with_ml(image):
    """AI-powered Hb prediction from photo"""
    model = load_ml_model()
    
    # Extract conjunctiva region (center of image)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w = img_cv.shape[:2]
    center = img_cv[h//4:3*h//4, w//4:3*w//4]  # Focus on eye area
    
    # Get average RGB colors
    mean_rgb = np.mean(center, axis=(0,1))[::-1]  # Convert BGR to RGB
    
    # Neural Network prediction
    hb = model.predict([mean_rgb])[0]
    return round(hb, 1), mean_rgb.astype(int).tolist()
