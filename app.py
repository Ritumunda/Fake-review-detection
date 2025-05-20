# ✅ Import necessary libraries
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import hashlib
import time
from tensorflow.keras.models import load_model

# ✅ Load the trained models and vectorizer
scaler = joblib.load('scaler.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')
model = load_model('fake_review_model_with_attention.h5')

# ✅ Blockchain classes (same as you made earlier)
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        block_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        sha.update(block_data.encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.reviewers = set()

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_review(self, review):
        reviewer_id = review.get('User_ID', None)
        if reviewer_id and reviewer_id not in self.reviewers:
            self.reviewers.add(reviewer_id)
            previous_block = self.chain[-1]
            new_block = Block(len(self.chain), time.time(), review, previous_block.hash)
            self.chain.append(new_block)
            return True
        else:
            return False

# ✅ Streamlit App Layout
st.set_page_config(page_title="Fake Review Detector", page_icon="🤔", layout="wide")

st.title("🤔 Fake Review Detection App")
st.subheader("Blockchain + DNN + Attention Powered Fake Review Detector")

# Sidebar
with st.sidebar:
    st.title("ℹ️ About")
    st.info("""
    🚀 This is a Fake Review Detection app built using:
    - Blockchain-based reviewer verification
    - Deep Neural Network (DNN)
    - Attention Mechanism
    - TF-IDF Feature Extraction
    """)

# Input box
user_review = st.text_area("Enter your product review here:")

# Dummy user ID for demo (In production, fetch real User ID)
user_id = st.text_input("Enter your User ID (for blockchain verification):")

# Predict Button
if st.button("Predict"):
    if user_review.strip() == "" or user_id.strip() == "":
        st.warning("⚠️ Please enter both a review and User ID!")
    else:
        with st.spinner('Verifying reviewer and predicting...'):

            # Step 1: Blockchain Verification (simulate one review at a time)
            blockchain = Blockchain()  # In production, you'd keep the chain persistent
            verified = blockchain.add_review({"User_ID": user_id, "Review": user_review})

            if not verified:
                st.error("❌ This reviewer is flagged! Review might be Fake!")
            else:
                # Step 2: Preprocessing the input
                review_transformed = tfidf.transform([user_review])
                review_scaled = scaler.transform(review_transformed.toarray())

                # Step 3: Predicting
                prediction = model.predict(review_scaled)
                predicted_label = (prediction > 0.5).astype("int32")[0][0]

                if predicted_label == 1:
                    st.success("✅ This review seems *Real*! Great!")
                else:
                    st.error("❌ This review seems *Fake*! Be cautious!")

