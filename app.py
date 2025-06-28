import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🎤 Taylor Swift Lyrics Visualizer")

def create_genius_url(title):
    # Converts "Blank Space" → "blank-space-lyrics"
    return "https://genius.com/Taylor-swift-" + "-".join(title.lower().split()) + "-lyrics"

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Fetching lyrics..."):
        try:
            song_url = create_genius_url(song_title)
            st.markdown(f"🔗 [View Song on Genius]({song_url})")

            headers = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(song_url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            lyrics_divs = soup.select("div[data-lyrics-container='true']")
            lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])

            if lyrics.strip():
                st.subheader("Lyrics:")
                st.text_area("Full Lyrics", lyrics, height=300)

                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt)
            else:
                st.warning("❌ Could not extract lyrics from Genius page.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
