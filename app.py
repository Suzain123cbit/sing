import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

st.title("🎤 Taylor Swift Lyrics Visualizer")

song_title = st.text_input("Enter a Taylor Swift song title:")

if song_title:
    headers = {
        "Authorization": "Bearer LWHbjh1qK_4RIMqAgbGkKfDgK7qfURxcjGy2diHlxXDLf8XFABKZ1DtPqlEX4ar9"  # Replace this
    }
    search_url = f"https://api.genius.com/search?q=Taylor Swift {song_title}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        if hits:
            song_url = hits[0]["result"]["url"]  # Real song webpage
            st.write(f"🔗 [View Song on Genius]({song_url})")

            # Scrape lyrics from Genius song page
            page = requests.get(song_url)
            soup = BeautifulSoup(page.text, "html.parser")

            # Genius lyrics are often within <div> tags with data-lyrics-container="true"
            lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
            lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])

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
            st.warning("No matching song found.")
    else:
        st.error("API error. Check your access token.")
