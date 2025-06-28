import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🎤 Taylor Swift Lyrics Visualizer")

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Searching Genius..."):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        search_url = f"https://genius.com/api/search/multi?per_page=5&q=Taylor Swift {song_title}"
        r = requests.get(search_url, headers=headers)

        if r.status_code == 200:
            hits = r.json()['response']['sections'][0]['hits']
            if hits:
                song_url = hits[0]['result']['url']
                st.markdown(f"🔗 [View Song on Genius]({song_url})")

                page = requests.get(song_url, headers=headers)
                soup = BeautifulSoup(page.text, "html.parser")

                # Modern method to get lyrics
                lyrics_blocks = soup.select("div[data-lyrics-container='true']")
                lyrics = "\n".join([block.get_text(separator="\n") for block in lyrics_blocks])

                if lyrics.strip():
                    st.subheader("Lyrics:")
                    st.text_area("Full Lyrics", lyrics, height=300)

                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(lyrics)
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot(plt)
                else:
                    st.warning("❌ Couldn't extract lyrics from the page.")
            else:
                st.warning("❌ No results found on Genius.")
        else:
            st.error("⚠️ Genius search API failed.")
