import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set up page
st.title("🎤 Taylor Swift Lyrics Visualizer")

# Input box
song_title = st.text_input("Enter a Taylor Swift song title:")

# Genius API token
GENIUS_API_TOKEN = "LWHbjh1qK_4RIMqAgbGkKfDgK7qfURxcjGy2diHlxXDLf8XFABKZ1DtPqlEX4ar9"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN)

if song_title:
    try:
        song = genius.search_song(song_title, artist="Taylor Swift")
        if song and song.lyrics:
            st.subheader("Lyrics:")
            st.text_area("Full Lyrics", value=song.lyrics, height=300)

            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(song.lyrics)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.warning("Lyrics not found for this song.")
    except Exception as e:
        st.error(f"Error: {e}")
