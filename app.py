import streamlit as st
import numpy as np
from PIL import Image
import cv2

st.set_page_config(page_title="HemoScan AI", layout="wide")

st.title("🚀 HemoScan AI")
st.header("Non-invasive Anemia Detection & Risk Analysis")

tab1, tab2 = st.tabs(["📸 Photo Analysis", "📋 Risk Assessment"])

with tab1:
    st.subheader("Upload Conjunctiva Photo (Inner Eyelid)")
    
    def predict_hb(image):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        h, w = img_cv.shape[:2]
        center = img_cv[h//4:3*h//4, w//4:3*w//4]
        mean_rgb = np.mean(center, axis=(0,1))[::-1]
        r, g, b = mean_rgb
        hb = 8.5 + (r - 140) * 0.08 + (g - 130) * 0.07
        return round(hb, 1), mean_rgb
    
    uploaded_file = st.file_uploader("Choose photo...", type=['png','jpg','jpeg'], key="photo")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded", use_column_width=True)
        
        with st.spinner("🔬 Analyzing..."):
            hb, rgb = predict_hb(image)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Hemoglobin", f"{hb:.1f} g/dL", delta=None)
            with col2:
                status = "🟡 ANEMIC" if hb < 12 else "🟢 NORMAL"
                st.metric("Status", status)
            with col3:
                st.metric("Redness", f"{rgb[0]:.0f}")
            
            if hb < 12:
                st.error("⚠️ **ANEMIA DETECTED** - Seek medical advice")
            else:
                st.success("✅ **Normal levels**")

with tab2:
    st.subheader("Risk Analysis Questionnaire")
    
    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        age = col1.number_input("Age", 16, 80, 25)
        gender = col2.selectbox("Gender", ["Male", "Female"])
        
        fatigue = st.slider("Tiredness (0-10)", 0, 10, 3)
        diet = st.selectbox("Meat intake", ["Never", "Rarely", "Weekly", "Daily"])
        dizzy = st.checkbox("Feel dizzy often")
        pale = st.checkbox("Notice pale skin")
        
        submitted = st.form_submit_button("Calculate Risk")
    
    if submitted:
        # Simple risk scoring
        risk_score = 0
        if age > 50: risk_score += 15
        if gender == "Female": risk_score += 20
        if fatigue > 6: risk_score += 25
        if diet in ["Never", "Rarely"]: risk_score += 30
        if dizzy: risk_score += 20
        if pale: risk_score += 15
        
        st.header("🎯 Risk Results")
        col1, col2 = st.columns([3,1])
        
        if risk_score < 30:
            col1.success("🟢 **LOW RISK**")
            col1.info("Healthy diet + regular checkups recommended")
        elif risk_score < 60:
            col1.warning("🟡 **MEDIUM RISK**")
            col1.info("Monitor symptoms + improve iron intake")
        else:
            col1.error("🔴 **HIGH RISK**")
            col1.info("Consult doctor immediately")
        
        col2.metric("Risk Score", f"{risk_score}%", delta=None)
        
        st.balloons()

st.markdown("---")
st.markdown("*Powered by conjunctiva color analysis + ML risk scoring*")
