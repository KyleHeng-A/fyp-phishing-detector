import streamlit as st
import joblib
import os
from detector.features import extract_features
from detector.url_checks import analyze_url
from detector.rules import calculate_risk_score, classify_hybrid

# Page Configuration
st.set_page_config(page_title="AI Phishing Shield", page_icon="🛡️")

st.title("🛡️ Hybrid Phishing Detection System")
st.markdown("""
This system uses a **Hybrid Approach** combining:
1. **Rule-Based Heuristics** (Regex & URL Analysis)
2. **Machine Learning** (Logistic Regression & Random Forest)
""")

# Input Section
st.subheader("Analyze Message")
message = st.text_area("Paste the email or message text here:", height=150)
url = st.text_input("Enter any associated URL (optional):")

if st.button("Run Security Scan"):
    if not message.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing patterns and running ML models..."):
            # 1. Run Feature Extraction
            features = extract_features(message)
            if url.strip():
                features.update(analyze_url(url))

            # 2. Get Rule Score and Hybrid Classification
            score = calculate_risk_score(features)
            result_string = classify_hybrid(message, score)

            # 3. Display Results with UI Formatting
            st.divider()

            if "Phishing" in result_string:
                st.error(f"### Result: {result_string}")
            elif "Suspicious" in result_string:
                st.warning(f"### Result: {result_string}")
            else:
                st.success(f"### Result: {result_string}")

            # 4. Show triggered rules for transparency (Great for FYP viva!)
            with st.expander("View Detected Rule Features"):
                detected = [f for f, v in features.items() if v]
                if detected:
                    for d in detected:
                        st.write(f"- ✅ {d.replace('_', ' ').title()}")
                else:
                    st.write("No explicit rule-based red flags detected.")

st.sidebar.info(f"System trained on 82,486 samples. \nTarget Accuracy: 99%")