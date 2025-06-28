import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set your Genius API token here
GENIUS_API_TOKEN = "LWHbjh1qK_4RIMqAgbGkKfDgK7qfURxcjGy2diHlxXDLf8XFABKZ1DtPqlEX4ar9"

st.set_page_config(page_title="Taylor Swift Lyrics Visualizer", page_icon="🎤")

st.title("🎤 Taylor Swift Lyrics Visualizer")
song_title = st.text_input("Enter a Taylor Swift song title:")

def get_lyrics_from_url(song_url):
    page = requests.get(song_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})

    if not lyrics_divs:
        return None

    lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])
    return lyrics.strip()

if song_title:
    # Search for the song using Genius API
    search_url = f"https://api.genius.com/search?q=Taylor Swift {song_title}"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        if hits:
            song_info = hits[0]["result"]
            song_url = song_info["url"]
            st.markdown(f"🔗 [View Song on Genius]({song_url})")

            lyrics = get_lyrics_from_url(song_url)
            if lyrics:
                st.subheader("Lyrics:")
                st.text_area("Full Lyrics", lyrics, height=300)

                # Generate and display word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt)
            else:
                st.warning("Could not extract lyrics from the song page.")
        else:
            st.error("No song found.")
    else:
        st.error("API error occurred.")
