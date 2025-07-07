# text_emotion_music_app.py

import streamlit as st
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load CNN text-based emotion model
model = tf.keras.models.load_model("text_cnn_emotion_model.keras")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Emotion labels (must match model training order)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Emotion to music mapping (YouTube links or song titles)
emotion_to_music = {
    'Angry': ["https://www.youtube.com/watch?v=2vjPBrBU-TM"],
    'Disgust': ["https://www.youtube.com/watch?v=K0ibBPhiaG0"],
    'Fear': ["https://www.youtube.com/watch?v=wXhTHyIgQ_U"],
    'Happy': ["https://www.youtube.com/watch?v=ZbZSe6N_BXs"],
    'Sad': ["https://www.youtube.com/watch?v=J_ub7Etch2U"],
    'Surprise': ["https://www.youtube.com/watch?v=YqeW9_5kURI"],
    'Neutral': ["https://www.youtube.com/watch?v=V1Pl8CzNzCw"]
}

# Function to preprocess user input text
def preprocess_text(text, tokenizer, max_len=100):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_len, padding='post')
    return padded

st.title("💬 Emotion-Based Music Recommender (Text Chat)")
st.write("Enter a message, and we'll suggest music based on your emotion!")

user_input = st.text_area("Enter your message:")

if st.button("Analyze Emotion & Recommend Music"):
    if not user_input.strip():
        st.warning("Please enter a valid message.")
    else:
        with st.spinner("Predicting emotion..."):
            processed_text = preprocess_text(user_input, tokenizer)
            predictions = model.predict(processed_text)
            predicted_emotion = emotion_labels[np.argmax(predictions)]

        st.success(f"Detected Emotion: **{predicted_emotion}**")
        st.subheader("🎧 Recommended Music:")
        for song_url in emotion_to_music[predicted_emotion]:
            st.markdown(f"[Listen here]({song_url})")
