# =========================================
# CALL CENTER DATA VISUALIZATION (VS CODE)
# =========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


df = pd.read_csv("cleaned_customer_calls.csv")

df.columns = df.columns.str.strip()

print("Columns in dataset:")
print(df.columns)


TEXT_COLUMN = "cleaned_text"   

df["text_length"] = df[TEXT_COLUMN].astype(str).str.len()

plt.figure(figsize=(8,5))
plt.hist(df["text_length"], bins=30)
plt.title("Transcript Length Distribution")
plt.xlabel("Length of Transcript")
plt.ylabel("Number of Calls")
plt.show()

df["word_count"] = df[TEXT_COLUMN].astype(str).str.split().apply(len)

plt.figure(figsize=(8,5))
plt.hist(df["word_count"], bins=30)
plt.title("Word Count Distribution")
plt.xlabel("Number of Words")
plt.ylabel("Number of Calls")
plt.show()


if "sentiment" in df.columns:
    plt.figure(figsize=(6,4))
    sns.countplot(x="sentiment", data=df)
    plt.title("Sentiment Distribution")
    plt.show()


if "intent" in df.columns:
    plt.figure(figsize=(8,5))
    sns.countplot(x="intent", data=df)
    plt.title("Intent Distribution")
    plt.xticks(rotation=45)
    plt.show()


text = " ".join(df[TEXT_COLUMN].dropna().astype(str))

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most Frequent Words in Calls")
plt.show()

print("Visualization complete ✅")
