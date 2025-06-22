import streamlit as st
import hashlib
import time
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from googletrans import Translator

# Set page config
st.set_page_config(page_title="Fake Review Detector", layout="centered")

# Language dictionary
languages = {
    'en': {
        'title': "🕵️‍♀️ Fake Review Detection System",
        'user_id': "👤 Enter User ID:",
        'product_id': "📦 Enter Product ID:",
        'review_input': "📝 Enter Product Review:",
        'analyze': "🔍 Analyze Review",
        'translate_hi': "🇮🇳 Translate to Hindi",
        'translate_en': "🇬🇧 Translate to English",
        'view_reviews': "📂 View Stored Reviews"
    },
    'hi': {
        'title': "🕵️‍♀️ नकली समीक्षा पहचान प्रणाली",
        'user_id': "👤 उपयोगकर्ता आईडी दर्ज करें:",
        'product_id': "📦 उत्पाद आईडी दर्ज करें:",
        'review_input': "📝 उत्पाद समीक्षा दर्ज करें:",
        'analyze': "🔍 समीक्षा विश्लेषण करें",
        'translate_hi': "🇮🇳 हिंदी में अनुवाद करें",
        'translate_en': "🇬🇧 अंग्रेज़ी में अनुवाद करें",
        'view_reviews': "📂 संग्रहीत समीक्षाएँ देखें"
    }
}

# Language selector
lang_choice = st.selectbox("🌐 Choose Language", ["en", "hi"])
L = languages[lang_choice]

# Translator instance
translator = Translator()

# Load models
try:
    scaler = joblib.load('scaler.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    model = load_model('fake_review_model_with_attention.h5')
except Exception as e:
    st.error(f"❌ Error loading models: {str(e)}")
    st.stop()


# Style block
st.markdown("""<style>
/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #1e1e2f, #2b2e44) !important;
    color: #f1f2f6 !important;
}

/* Page text */
body, .stTextInput label, .stTextArea label, .stMarkdown, .stCaption, .stAlert {
    color: #f1f2f6 !important;
    font-family: 'Segoe UI', sans-serif;
}

/* Main title */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-weight: 600;
    font-size: 36px;
    margin-bottom: 10px;
}

/* Input fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #353b48 !important;
    color: #ffffff !important;
    border: 1px solid #57606f !important;
    border-radius: 6px;
    padding: 10px;
    font-size: 16px;
}

/* Buttons */
.stButton > button {
    background-color: #487eb0 !important;
    color: #ffffff !important;
    border-radius: 6px;
    font-weight: 600;
    font-size: 15px;
    padding: 10px 24px;
    margin-top: 10px;
}
.stButton > button:hover {
    background-color: #40739e !important;
}

/* Footer text */
.stCaption {
    color: #dcdde1 !important;
    font-style: italic;
    text-align: center;
    margin-top: 40px;
    font-size: 13px;
}
</style>""", unsafe_allow_html=True)



# Blockchain classes
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode())
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    def create_genesis_block(self):
        return Block(0, time.time(), {"User_ID": "0", "Product_ID": "0", "Review": "Genesis", "Timestamp": time.time()}, "0")
    def is_duplicate_review(self, user_id, product_id, review_text):
        return any(block.data.get("User_ID") == user_id and
                   block.data.get("Product_ID") == product_id and
                   block.data.get("Review") == review_text for block in self.chain)
    def add_review(self, review):
        if self.is_duplicate_review(review["User_ID"], review["Product_ID"], review["Review"]):
            return False
        prev = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), review, prev.hash)
        self.chain.append(new_block)
        return True

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state["blockchain"] = Blockchain()
blockchain = st.session_state["blockchain"]

# Title and inputs
st.title(L['title'])
col1, col2 = st.columns(2)
with col1:
    user_id = st.text_input(L['user_id'], key="user_id")
with col2:
    product_id = st.text_input(L['product_id'], key="product_id")
review_text = st.text_area(L['review_input'], key="review_text")

# Translate buttons
col3, col4 = st.columns(2)
with col3:
    if st.button(L['translate_hi'], key="translate_hi_button"):
        if review_text:
            try:
                st.write("**Translated to Hindi:**")
                st.success(translator.translate(review_text, dest="hi").text)
            except Exception as e:
                st.error(f"Translation error: {e}")
        else:
            st.warning("⚠️ Please enter a review.")
with col4:
    if st.button(L['translate_en'], key="translate_en_button"):
        if review_text:
            try:
                st.write("**Translated to English:**")
                st.success(translator.translate(review_text, dest="en").text)
            except Exception as e:
                st.error(f"Translation error: {e}")
        else:
            st.warning("⚠️ Please enter a review.")

# Analyze button
if st.button(L['analyze'], key="analyze_button"):
    if blockchain.is_duplicate_review(user_id, product_id, review_text):
        st.error("🚨 This review already exists. Possible spam.")
    else:
        with st.spinner("Analyzing..."):
            review_data = {
                "User_ID": user_id,
                "Product_ID": product_id,
                "Review": review_text,
                "Timestamp": time.time()
            }
            if not blockchain.add_review(review_data):
                st.error("⚠️ This is a duplicate review submission.")
            else:
                try:
                    vector = tfidf.transform([review_text])
                    scaled = scaler.transform(vector.toarray())
                    pred = model.predict(scaled)[0][0]
                    if pred > 0.5:
                        st.success(f"✅ Review is likely REAL (Confidence: {pred:.2f})")
                    else:
                        st.error(f"❌ Review is likely FAKE (Confidence: {1 - pred:.2f})")
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

# View stored reviews
st.markdown("---")
if st.button(L['view_reviews'], key="view_reviews_button"):
    reviews = [block.data for block in blockchain.chain if block.index > 0]
    if reviews:
        st.write("### Stored Reviews 📝")
        st.table(reviews)
    else:
        st.warning("⚠️ No reviews stored yet. Submit one first!")

# Footer
st.markdown("""
<hr style='border-top:1px solid #ccc; margin-top:40px;'/>
<div style='text-align:center; font-size:13px; color: #888;'>
    🔐 Built with Blockchain + AI | 🚀 Designed by <b>Ritu</b>
</div>
""", unsafe_allow_html=True)
