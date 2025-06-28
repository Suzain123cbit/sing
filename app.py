import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🎤 Taylor Swift Lyrics Visualizer")

def generate_genius_url(title):
    # Convert title to Genius URL slug (e.g., "Blank Space" → "blank-space")
    slug = "-".join(title.lower().strip().split())
    return f"https://genius.com/Taylor-swift-{slug}-lyrics"

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Fetching lyrics..."):
        try:
            url = generate_genius_url(song_title)
            st.markdown(f"🔗 [View Song on Genius]({url})")

            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

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
                st.warning("⚠️ Couldn't extract lyrics. Check the song title.")
        except Exception as e:
            st.error(f"Error: {e}")
