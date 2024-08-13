# Import the required libraries
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Create an instance of Tkinter Frame
win = Tk()

# Set the geometry of Tkinter Frame
''' GUI STARTS'''
win.geometry("900x650")
win.resizable(False, False)
win.title("Anime Recommendation System")

# Create a Canvas
canvas = Canvas(win, width=1000, height=1000)
canvas.pack(fill=BOTH, expand=False)

# Add Image inside the Canvas
# bg = ImageTk.PhotoImage(file="Top-25-Best-Anime-Quotes-of-All-Time-MyAnimeList.net.png")
# canvas.create_image(0, 0, image=bg, anchor='nw')

headingFrame = Frame(win, bg="azure", bd=5)
headingFrame.place(relx=0.11, rely=0.05, relwidth=0.80, relheight=0.1)

headingLabel = Label(headingFrame, text="Anime Recommendation System", bg=None, font=('Times', 20, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

def text_cleaning(text):
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    return text

# Read and clean data
anime = pd.read_csv("anime.csv")
anime_rating = pd.read_csv("rating.csv")
anime.dropna(inplace=True)  # Cleansing anime csv; rating is already cleansed
anime_rating.drop_duplicates(keep='first', inplace=True)
anime['name'] = anime['name'].apply(text_cleaning)
print("********** Cleansing done ********* Need Plotting *********************")

def plots():
    print("Plotting started")
    
    # Calculate counts for each type
    ona = anime.loc[anime['type'] == 'ONA'].shape[0]
    tv = anime.loc[anime['type'] == 'TV'].shape[0]
    movie = anime.loc[anime['type'] == 'Movie'].shape[0]
    music = anime.loc[anime['type'] == 'Music'].shape[0]
    special = anime.loc[anime['type'] == 'Special'].shape[0]
    ova = anime.loc[anime['type'] == 'OVA'].shape[0]

    labels = ['ONA', 'TV', 'Movie', 'Music', 'Special', 'OVA']
    colors = ['#81F4E1', '#56CBF9', '#F5D491', '#BEB7A4', '#B4E1FF', '#F06C9B']

    # Pie chart for Anime Categories Distribution
    plt.figure(figsize=(10, 7))
    plt.title('Anime Categories Distribution')
    plt.pie([ona, tv, movie, music, special, ova],
            labels=labels,
            colors=colors,
            autopct='%.2f %%')
    plt.show()
    
    # Top 10 Anime Community Plot
    plt.figure(figsize=(20, 15))
    top10_anime = anime[['name', 'members']].sort_values(by='members', ascending=False).head(10)

    colors = ['#87255B', '#56CBF9', '#F5D491', '#BEB7A4', '#B4E1FF', '#F06C9B', '#D3C4D1', '#81F4E1', '#C2AFF0', '#C57B57']

    labels = top10_anime['name'].values
    values = top10_anime['members'].values

    plt.barh(labels, values, color=colors, edgecolor='black')
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='x', alpha=0.7)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title("Top 10 Anime Community", fontdict={'fontsize': 20})
    plt.show()

def recom():
    tf = TfidfVectorizer()
    tfidf_matrix = tf.fit_transform(anime['genre'])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=anime['name'], columns=anime['name'])

    def anime_recommendations(name, similarity_data=cosine_sim_df, items=anime[['name', 'genre']], k=10):
        index = similarity_data.loc[:, name].to_numpy().argpartition(range(-1, -k, -1))
        closest = similarity_data.columns[index[-1:-(k+2):-1]]
        closest = closest.drop(name, errors='ignore')
        return pd.DataFrame(closest).merge(items).head(10)

    recommendations = anime_recommendations(anime_entry.get())
    print(recommendations)
    
    text_to_display = anime_entry.get()
    label = Label(win, text=text_to_display)
    label.pack()

def get_input():
    user_input = anime_entry.get()
    print("User input:", user_input)
    # Do something with the user input, such as process or display it

Frame1 = Frame(win, bg=None)
Frame1.place(relx=0.25, rely=0.43, relwidth=0.50, relheight=0.18)

label1 = Label(Frame1, text="Enter Anime Name to get recommendations: ", bg=None, fg='black', font=('Courier', 13, 'bold'))
label1.place(relx=0.05, rely=0.2, relheight=0.15)

anime_entry = Entry(Frame1, font=('Century 12'))
anime_entry.place(relx=0.05, rely=0.5, relwidth=0.8, relheight=0.3)

button = Button(win, text='Show Data', font=('Courier', 15, 'normal'), command=plots)
button.place(relx=0.10, rely=0.7, relwidth=.3, relheight=.2)

button = Button(win, text='Show Predictions', font=('Courier', 15, 'normal'), command=recom)
button.place(relx=0.65, rely=0.7, relwidth=.3, relheight=.2)

win.mainloop()
