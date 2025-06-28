import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import urllib.parse

st.title("🎤 Taylor Swift Lyrics Visualizer")

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    with st.spinner("Finding song page..."):
        try:
            query = f"{song_title} site:genius.com lyrics Taylor Swift"
            google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            headers = {"User-Agent": "Mozilla/5.0"}

            response = requests.get(google_search_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # Try to find first result that links to genius.com
            links = soup.find_all("a", href=True)
            genius_links = [l['href'] for l in links if 'genius.com' in l['href']]
            if genius_links:
                # Google result links are prefixed, we extract clean URL
                start = genius_links[0].find("https://")
                end = genius_links[0].find("&", start)
                song_url = genius_links[0][start:end]
                st.markdown(f"🔗 [View Song on Genius]({song_url})")

                lyrics_page = requests.get(song_url, headers=headers)
                soup = BeautifulSoup(lyrics_page.text, "html.parser")
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
                    st.warning("Could not extract lyrics from the song page.")
            else:
                st.warning("Could not find Genius link via Google.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
