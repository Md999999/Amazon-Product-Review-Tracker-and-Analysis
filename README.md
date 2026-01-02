# Amazon-Product-Review-Tracker-and-Analysis

Developed an AI-powered sentiment analysis dashboard that automates the processing of 500,000+ Amazon reviews to identify customer satisfaction trends and product pain points.
The link to the Dataset: https://www.kaggle.com/datasets/arhamrumi/amazon-product-reviews

Project Overview
This is a professional-grade intelligence dashboard designed to analyse customer emotions at scale. Using Natural Language Processing (NLP), the app processes thousands of raw Amazon reviews to categorise feedback as Positive, Negative, or Neutral, helping businesses identify "Pain Points" and "Buzz" without reading every single comment.

The Journey: My Step-by-Step Process
1. Data Strategy
I started with the raw Amazon Product Reviews dataset from Kaggle (500,000+ rows). The goal was to build a pipeline that could handle this massive volume while remaining fast and interactive.

2. Building the "AI Brain"
I implemented the VADER Sentiment Model. This AI is particularly well-suited for reviews because it understands social nuances—it recognises that capitalisation (e.g., "GREAT") and punctuation (e.g., "!!!") can intensify sentiment.

3. Dashboard Engineering
I used Streamlit to create the UI. I focused on making the data "scannable" by using:

Metric Cards: For high-level stats (Avg Rating, Unhappy %).

Tabs: To separate complex charts from raw data tables.

Sidebars: To give the user control over the sample size (500 to 5,000 reviews).

Mistakes & Fixes:

The "Broken CSV" Error: * Problem: Commas and quotes inside reviews were breaking the columns.

Fix: I added on_bad_lines='skip' and quoting=3 to make the data reader more "forgiving."

The "PK" ZIP Mystery: * Problem: I got a PK\x03\x04 error because the data was compressed in a ZIP file.

Fix: I added a manual extraction script using zipfile to unpack the data automatically before analysis.

The "Buffer Overflow" Crash: * Problem: Some reviews were so long that they crashed the default memory buffer.

Fix: I switched the engine to engine='python', which is more robust for handling massive blocks of text.

The Pathing Issue: * Problem: Streamlit wouldn't run from the standard terminal.

Fix: I learned to use the python -m streamlit run command to bypass Windows pathing restrictions.

Analysing the Visuals
1. Sentiment Distribution (The Tracker)
This bar chart tracks the volume of customer mood. It shows exactly how many people fall into each sentiment bucket, allowing a business to see if negative feedback is outweighing the positive.

2. Rating vs. Sentiment (The Analysis)
This boxplot analyses consistency. It compares the AI’s sentiment guess against the user's actual Star Rating. If the "Positive" box is set to 4-5 stars, it indicates that the AI is functioning correctly. It also helps spot "outliers" (like someone giving 1 star but writing a happy review).

3. Word Themes (The WordClouds)
I used color-coded clouds (Green for Happy, Red/Orange for Angry) to highlight the most used words. This instantly shows why people are upset or happy without needing to read the raw text.

Tech Stack
Language: Python

UI: Streamlit

Data: Pandas, Kagglehub

AI/NLP: NLTK (Vader Lexicon)

Visuals: Matplotlib, Seaborn, WordCloud

()(https://github.com/Md999999/Amazon-Product-Review-Tracker-and-Analysis/blob/main/Screenshot%202026-01-02%20042941.png)
