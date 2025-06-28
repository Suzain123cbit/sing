import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🎤 Taylor Swift Lyrics Visualizer")

GENIUS_API_KEY = "ZHJc3sdYWUmJFxp4Tr3vRPmh3pNQwSs04Gnibohpd5kWWLuFndfqedHA-RblWKyp"
genius = lyricsgenius.Genius(GENIUS_API_KEY, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Fetching lyrics..."):
        try:
            song = genius.search_song(song_title, "Taylor Swift")
            if song and song.lyrics:
                st.subheader("Lyrics:")
                st.text_area("Full Lyrics", song.lyrics, height=300)

                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(song.lyrics)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt)
            else:
                st.warning("Could not find lyrics for this song.")
        except Exception as e:
            st.error(f"Error: {e}")
