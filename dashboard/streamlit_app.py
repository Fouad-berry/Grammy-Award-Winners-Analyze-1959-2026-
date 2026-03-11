import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Grammy Awards Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('../dataset/grammy_awards.csv')

df = load_data()
st.title("Grammy Awards Dashboard (1959–2026) – Big Four uniquement")

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
        artist_df = df[df['Artist'].str.lower() == artist.lower()]
        if artist_df.empty:
            st.warning("Artiste non trouvé.")
        else:
            st.success(f"{artist} : {len(artist_df)} victoires")
            st.write("Catégories :", ', '.join(artist_df['Category'].unique()))
            st.write("Années :", ', '.join(map(str, artist_df['Year'].unique())))

