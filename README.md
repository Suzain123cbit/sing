# 🎵 Taylor Swift Lyrics Visualizer

This is a Streamlit app that fetches the lyrics of a Taylor Swift song using the Genius API and displays a word cloud from the lyrics.

## How It Works
- Enter the title of a Taylor Swift song
- The app fetches lyrics using Genius API
- Lyrics are displayed in a text box
- A word cloud is generated from the lyrics

## Setup
1. Install required packages:
```bash
pip install streamlit requests wordcloud matplotlib
```

2. Set your Genius API Token in the `headers` of `app.py`.

3. Run the app:
```bash
streamlit run app.py
```

## Deployment
Deployed using [Streamlit Community Cloud](https://streamlit.io/cloud).
