import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import lyricsgenius

st.title("🎤 Taylor Swift Lyrics Visualizer")

# Add your Genius API token here (keep this secret in real apps)
GENIUS_API_TOKEN = "Hyj3OPecmkFPPyEgGPWgF9p9oDplEiU_u-L4KTPOGJ5nfQHQAlfEv4"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Fetching lyrics..."):
        song = genius.search_song(song_title, "Taylor Swift")
        if song and song.lyrics:
            st.subheader("Lyrics:")
            st.text_area("Full Lyrics", song.lyrics, height=300)

            # Generate and display word cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(song.lyrics)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt)
        else:
            st.warning("Could not find lyrics for this song.")
