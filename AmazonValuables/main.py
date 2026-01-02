# The libraries I used
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import nltk
import kagglehub
import zipfile
import os

#start up
# Word list for the AI brain
nltk.download('vader_lexicon')
# Whole screen as the dashboard
st.set_page_config(page_title="Amazon Insight Pro", layout="wide")


# Data Engine Fixed all the problems I got
@st.cache_data
def load_and_sample_data(size):
    try:
        #Downloaded the dataset folder from Kaggle
        path = kagglehub.dataset_download("arhamrumi/amazon-product-reviews")
        csv_path = os.path.join(path, "Reviews.csv")

        # If the CSV isn't there,I made it so it will find the zip and extract it had one of those errors
        # where it couldn't get the content
        if not os.path.exists(csv_path):
            for file in os.listdir(path):
                if file.endswith(".zip"):
                    with zipfile.ZipFile(os.path.join(path, file), 'r') as z:
                        z.extractall(path)

        # Read the file using the 'python' engine so it doesn't crash on long reviews
        df = pd.read_csv(
            csv_path,
            encoding="ISO-8859-1",
            on_bad_lines="skip", # It skips lines that are broken
            engine="python",      # This engine is better for messy text
            quoting=3             # Now pandas ignore weird quotes in reviews
        )

        # Finds the column that actually has the review text
        text_col = next((c for c in ['Text', 'text', 'ReviewText'] if c in df.columns), None)
        if not text_col: return pd.DataFrame()

        # Grab a random sample based on what I picked in the slider
        sampled = df[[text_col, 'Score']].sample(size).reset_index(drop=True)
        return sampled.rename(columns={text_col: 'text'})
    except Exception as e:
        # Show me if something goes wrong
        st.error(f"Error: {e}")
        return pd.DataFrame()


# Sidebar Controls
st.sidebar.header("Dashboard Controls")
st.sidebar.info("Change the settings to change the analysis too.")
# Slider for how many reviews I want to look at
review_count = st.sidebar.slider("Number of Reviews", 500, 5000, 1000, step=500)
# Dropdown for the look of the app
theme_choice = st.sidebar.selectbox("Color Theme", ["Modern", "Classic", "High Contrast"])

#AI Sentiment Brain
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    # Get the score for the review
    score = analyzer.polarity_scores(str(text))['compound']
    # If score is high it's happy, if low it's sad
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    return 'Neutral'


# Website UI
st.title("Amazon Product Review Tracker and Analysis")
st.markdown("---")

# loading spinner shoes while it's working
with st.spinner("Analyzing data... hang on..."):
    df = load_and_sample_data(review_count)

if not df.empty:
    # Run the sentiment AI on every review in the table
    df['Sentiment'] = df['text'].apply(get_sentiment)

    # 1. Top Stats (Metric cards)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Reviews Scanned", len(df))
    # This is the 'Ground Truth' to compare against the AI
    m2.metric("Avg Rating", f"{round(df['Score'].mean(), 1)} ⭐")

    # Work out the percentages for the metrics
    pos_p = (len(df[df['Sentiment'] == 'Positive']) / len(df)) * 100
    neg_p = (len(df[df['Sentiment'] == 'Negative']) / len(df)) * 100

    m3.metric("Positive", f"{round(pos_p)}%", "Good")
    m4.metric("Negative", f"{round(neg_p)}%", "-Bad", delta_color="inverse")

    # 2. Tabs to keep it clean
    tab_charts, tab_clouds, tab_data = st.tabs(["📈 Analysis Charts", "☁️ Word Themes", "📋 Raw Data"])

    with tab_charts:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots()
            # Bar chart showing the split of Pos/Neg/Neu
            sns.countplot(data=df, x='Sentiment', palette='viridis')
            st.pyplot(fig)
        with col_right:
            st.subheader("Rating vs Sentiment")
            fig2, ax2 = plt.subplots()
            # Boxplot to see if the star rating actually matches the AI's guess
            sns.boxplot(data=df, x='Sentiment', y='Score', palette='Set2')
            st.pyplot(fig2)

    with tab_clouds:
        c1, c2 = st.columns(2)
        # Create word clouds for happy and sad reviews
        with c1:
            st.markdown("### 🟢 Positive Buzz")
            pos_words = " ".join(df[df['Sentiment'] == 'Positive']['text'])
            if pos_words:
                # Use 'summer' colors for a positive feel
                wc = WordCloud(background_color="white", colormap="summer").generate(pos_words)
                st.image(wc.to_array())
        with c2:
            st.markdown("### 🔴 Pain Points")
            neg_words = " ".join(df[df['Sentiment'] == 'Negative']['text'])
            if neg_words:
                # Use 'autumn' colors for warnings/negative words
                wc = WordCloud(background_color="white", colormap="autumn").generate(neg_words)
                st.image(wc.to_array())

    with tab_data:
        st.subheader("Complete Data Feed")
        # Search the table for specific keywords like 'delivery' or 'quality'
        search = st.text_input("Search for a specific word in reviews (e.g., 'battery'):")
        if search:
            display_df = df[df['text'].str.contains(search, case=False)]
        else:
            display_df = df
        st.dataframe(display_df, use_container_width=True)

# Footer stuff in the sidebar
st.sidebar.markdown("---")
st.sidebar.write("Project: Amazon Sentiment Analysis")
st.sidebar.write("Data Source: Kaggle (Raw Reviews)")