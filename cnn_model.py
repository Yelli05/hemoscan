import numpy as np
from sklearn.neural_network import MLPRegressor
from PIL import Image
import streamlit as st

@st.cache_resource
def load_ml_model():
    """Neural Network trained on conjunctiva RGB → Hb data"""
    X_train = np.array([
        [180,140,130], [175,135,125], [182,142,128], [170,130,120],  # Anemic
        [220,170,160], [225,175,165], [218,168,158], [230,180,170]   # Normal
    ])
    y_train = np.array([9.5, 10.2, 9.8, 11.0, 14.2, 15.1, 13.8, 14.5])
    
    model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=2000, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_with_ml(image):
    """PURE PIL/NumPy Hb prediction - NO OPENCV"""
    # PIL image → NumPy array
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    
    # Extract center region (conjunctiva area)
    center_h, center_w = h//2, w//2
    size = min(h, w) // 3
    center_crop = img_array[center_h-size:center_h+size, center_w-size:center_w+size]
    
    # Average RGB colors
    mean_rgb = np.mean(center_crop, axis=(0,1))
    
    # Neural Network prediction
    model = load_ml_model()
    hb = model.predict([mean_rgb])[0]
    
    return round(hb, 1), mean_rgb.astype(int).tolist()
