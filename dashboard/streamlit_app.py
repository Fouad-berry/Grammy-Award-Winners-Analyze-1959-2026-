import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Grammy Awards Dashboard", layout="wide")

# -------------------------
# LOAD DATA
# -------------------------
import os
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "dataset", "grammy_awards.csv")
    return pd.read_csv(csv_path)

df = load_data()

# -------------------------
# WIKIPEDIA IMAGE FUNCTION
# -------------------------
def get_artist_image(artist):

    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "GrammyDashboard/1.0 (your_email@example.com)"
    }

    params = {
        "action": "query",
        "titles": artist,
        "prop": "pageimages",
        "pithumbsize": 500,
        "format": "json",
        "redirects": 1
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()

        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            if "thumbnail" in page:
                return page["thumbnail"]["source"]

    except Exception as e:
        print("Wikipedia API error:", e)

    return None

st.title("Grammy Awards Dashboard (1959–2026) – Big Four & Pop uniquement")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Aller à :",
    ["Dashboard général", "Artist Analyzer"]
)

# -------------------------
# DASHBOARD GENERAL
# -------------------------
if page == "Dashboard général":

    st.header("Statistiques générales")

    st.subheader("Nombre de Grammys par décennie")

    dec = df['Decade'].value_counts().sort_index()
    st.bar_chart(dec)

    st.subheader("Top 10 artistes les plus récompensés")

    top_artists = df['Artist'].value_counts().head(10)
    st.bar_chart(top_artists)


# -------------------------
# ARTIST ANALYZER
# -------------------------
elif page == "Artist Analyzer":

    st.header("Artist Analyzer")

    # Liste unique des artistes (Artist + Winner)
    artist_list = pd.Series(df['Artist'].tolist() + df['Winner'].tolist()).dropna().unique()
    artist_list = sorted(set(artist_list))

    # Saisie libre
    import streamlit as st
    if 'selected_artist' not in st.session_state:
        st.session_state['selected_artist'] = ''

    artist = st.text_input("Nom de l'artiste (autocomplétion)", "")

    # Suggestions dynamiques
    def normalize(s):
        return ''.join(s.lower().split())

    suggestions = []
    if artist:
        artist_norm = normalize(artist)
        suggestions = [a for a in artist_list if artist_norm in normalize(a)][:5]  # max 5 suggestions

    show_result = False
    if suggestions:
        st.markdown("Suggestions :")
        cols = st.columns(len(suggestions))
        for idx, s in enumerate(suggestions):
            if cols[idx].button(s, key=f"suggestion_{s}"):
                st.session_state['selected_artist'] = s
                show_result = True
    # Affiche le résultat seulement si une suggestion a été cliquée
    if st.session_state['selected_artist']:
        artist = st.session_state['selected_artist']
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
            # IMAGE ARTISTE
            image_url = get_artist_image(artist)
            col1, col2 = st.columns([1,2])
            with col1:
                if image_url:
                    st.image(image_url, width=250)
                else:
                    st.info("Image non trouvée sur Wikipedia")
            with col2:
                if not big_four.empty:
                    st.markdown("### Victoires Big Four")
                    st.write("Catégories :", ', '.join(big_four['Category'].unique()))
                    st.write("Années :", ', '.join(map(str, big_four['Year'].unique())))
                if not genre.empty:
                    st.markdown("### Victoires par Genre")
                    st.write("Catégories :", ', '.join(genre['Category'].unique()))
                    st.write("Années :", ', '.join(map(str, genre['Year'].unique())))