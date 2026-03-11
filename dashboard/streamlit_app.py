import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Grammy Awards Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('../dataset/grammy_awards.csv')

df = load_data()
st.title("Grammy Awards Dashboard (1959–2026) – Toutes catégories")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Aller à :", ["Dashboard général", "Timeline", "Artist Analyzer"])

if page == "Dashboard général":
    st.header("Statistiques générales")
    st.subheader("Nombre de Grammys par décennie")
    dec = df['Decade'].value_counts().sort_index()
    st.bar_chart(dec)
    st.subheader("Top 10 artistes les plus récompensés")
    top_artists = df['Artist'].value_counts().head(10)
    st.bar_chart(top_artists)

elif page == "Timeline":
    st.header("Timeline interactive des Grammy Awards")
    st.line_chart(df.groupby('Year').size())

elif page == "Artist Analyzer":
    st.header("Artist Analyzer")
    artist = st.text_input("Nom de l'artiste")
    if artist:
        # Recherche insensible à la casse et aux espaces, et accepte le nom comme sous-chaîne dans Artist OU Winner
        def normalize(s):
            return ''.join(s.lower().split())
        artist_norm = normalize(artist)
        artist_df = df[
            df['Artist'].apply(lambda x: artist_norm in normalize(str(x))) |
            df['Winner'].apply(lambda x: artist_norm in normalize(str(x)))
        ]
        if artist_df.empty:
            st.warning("Artiste non trouvé.")
        else:
            big_four = artist_df[artist_df['Award_Group'] == 'Big Four']
            genre = artist_df[artist_df['Award_Group'] == 'Genre']
            total = len(big_four) + len(genre)
            st.success(f"{artist} : {total} victoires (toutes catégories)")
            if not big_four.empty:
                st.markdown("**Victoires Big Four :**")
                st.write("Catégories :", ', '.join(big_four['Category'].unique()))
                st.write("Années :", ', '.join(map(str, big_four['Year'].unique())))
            if not genre.empty:
                st.markdown("**Victoires par Genre :**")
                st.write("Catégories :", ', '.join(genre['Category'].unique()))
                st.write("Années :", ', '.join(map(str, genre['Year'].unique())))
