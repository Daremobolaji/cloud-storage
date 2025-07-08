import streamlit as st
from textblob import TextBlob
nltk.download('wordnet')

# Emotion-based song recommendations with MP3 preview URLs
music_recommendations = {
    "happy": [
        {"title": "Happy - Pharrell Williams", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
        {"title": "Can't Stop the Feeling - Justin Timberlake", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    ],
    "sad": [
        {"title": "Someone Like You - Adele", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
        {"title": "Let Her Go - Passenger", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
    ],
    "neutral": [
        {"title": "Let It Be - The Beatles", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"},
        {"title": "Clocks - Coldplay", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"},
    ],
    "angry": [
        {"title": "Breaking the Habit - Linkin Park", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"},
        {"title": "Stronger - Kanye West", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"},
    ],
}

def detect_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.4:
        return "happy"
    elif polarity < -0.4:
        return "sad"
    else:
        return "neutral"

# Streamlit UI
st.set_page_config(page_title="Emotion-Based Music Recommender", layout="centered")

st.title("🎵 Emotion-Based Music Recommender")
st.markdown("Enter your mood or how you're feeling, and get music that fits!")

user_input = st.text_area("How are you feeling today?", height=100)

if st.button("Recommend Music"):
    if user_input:
        emotion = detect_emotion(user_input)
        st.subheader(f"Detected Emotion: {emotion.capitalize()}")
        st.markdown("### Recommended Songs 🎧")

        songs = music_recommendations.get(emotion, [])
        for song in songs:
            st.markdown(f"**{song['title']}**")
            st.audio(song['url'], format="audio/mp3")
    else:
        st.warning("Please describe your mood to get music recommendations.")

st.markdown("---")
st.caption("🎶 Built with Streamlit & love.")
