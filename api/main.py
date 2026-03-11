# FastAPI pour exposer les analyses Grammy Awards
from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.cluster import KMeans

app = FastAPI()

# Charger les données une fois au démarrage
df = pd.read_csv('dataset/grammy_awards.csv')

# Clustering artistes (mémorisé)
def get_artist_clusters(n_clusters=3):
    pivot = pd.pivot_table(df, index='Artist', columns='Category', values='Year', aggfunc='count', fill_value=0)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(pivot)
    pivot['Cluster'] = clusters
    return pivot

@app.get("/")
def read_root():
    return {"message": "Grammy Awards API"}

@app.get("/artist/{name}")
def artist_info(name: str):
    artist_df = df[df['Artist'].str.lower() == name.lower()]
    if artist_df.empty:
        raise HTTPException(status_code=404, detail="Artiste non trouvé")
    categories = artist_df['Category'].unique().tolist()
    years = artist_df['Year'].unique().tolist()
    total = len(artist_df)
    return {
        "artist": name,
        "total_wins": total,
        "categories": categories,
        "years": years
    }

@app.get("/stats/decade")
def stats_decade():
    return df['Decade'].value_counts().sort_index().to_dict()

@app.get("/clusters")
def clusters():
    pivot = get_artist_clusters()
    out = {}
    for c in sorted(pivot['Cluster'].unique()):
        out[f"Cluster {c}"] = pivot[pivot['Cluster'] == c].index.tolist()
    return out
