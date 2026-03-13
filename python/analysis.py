# Analyse des Grammy Awards (1959-2026)
# Ce script charge, explore et visualise les données du fichier grammy_awards.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le dataset
import os
def load_data():
    # Chemin absolu basé sur l'emplacement de ce script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "dataset", "grammy_awards.csv")
    df = pd.read_csv(csv_path)
    return df

def main():
    df = load_data()
    print('Aperçu des données:')
    print(df.head())
    print('\nColonnes:', df.columns.tolist())
    print('\nNombre de lignes:', len(df))

    # Top 10 artistes ayant gagné le plus de Grammys
    print('\nTop 10 artistes les plus récompensés:')
    top_artists = df['Artist'].value_counts().head(10)
    print(top_artists)

    # Top 10 genres les plus récompensés
    if 'Genre' in df.columns:
        print('\nTop 10 genres les plus récompensés:')
        top_genres = df['Genre'].value_counts().head(10)
        print(top_genres)
    else:
        print("\nColonne 'Genre' absente du dataset.")

    # Nombre de Grammys par décennie
    print('\nNombre de Grammys par décennie:')
    print(df['Decade'].value_counts().sort_index())

    # Artistes ayant remporté dans plusieurs catégories
    print('\nArtistes ayant gagné dans plusieurs catégories:')
    artist_cat = df.groupby('Artist')['Category'].nunique()
    multi_cat = artist_cat[artist_cat > 1].sort_values(ascending=False)
    for artist, n_cat in multi_cat.head(10).items():
        cats = df[df['Artist'] == artist]['Category'].unique()
        print(f"{artist} : {n_cat} catégories -> {', '.join(cats)}")

    # Pour la catégorie 'Song of the Year' : artistes les plus récompensés et chansons gagnantes
    song_of_year = df[df['Category'].str.lower() == 'song of the year']
    print("\nArtistes ayant le plus remporté 'Song of the Year':")
    print(song_of_year['Artist'].value_counts().head(10))

    print("\nChansons ayant remporté 'Song of the Year':")
    print(song_of_year['Winner'].value_counts().head(10))

    # Visualisation: Grammys par artiste (top 10)
    plt.figure(figsize=(10,5))
    top_artists.plot(kind='bar', color='gold')
    plt.title('Top 10 artistes les plus récompensés')
    plt.ylabel('Nombre de Grammys')
    plt.xlabel('Artiste')
    plt.tight_layout()
    plt.show()

    # Visualisation: Grammys par décennie
    plt.figure(figsize=(8,4))
    df['Decade'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Nombre de Grammys par décennie')
    plt.ylabel('Nombre de Grammys')
    plt.xlabel('Décennie')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
