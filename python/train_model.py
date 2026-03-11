# Machine Learning sur les Grammy Awards
# Ce script servira à entraîner des modèles (clustering, classification, etc.)

import pandas as pd


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_data(path='../dataset/grammy_awards.csv'):
	df = pd.read_csv(path)
	return df

def cluster_artists(df, n_clusters=3):
	# Crée une table artistes x catégories (nombre de victoires par catégorie)
	pivot = pd.pivot_table(df, index='Artist', columns='Category', values='Year', aggfunc='count', fill_value=0)
	# Clustering KMeans
	kmeans = KMeans(n_clusters=n_clusters, random_state=42)
	clusters = kmeans.fit_predict(pivot)
	pivot['Cluster'] = clusters
	print(pivot.groupby('Cluster').size())
	print('\nExemple d\'artistes par cluster:')
	for c in range(n_clusters):
		print(f"\nCluster {c}:")
		print(pivot[pivot['Cluster'] == c].index.tolist()[:10])
	return pivot

def main():
	df = load_data()
	print('Clustering des artistes selon leur profil de victoires...')
	cluster_artists(df, n_clusters=3)

if __name__ == '__main__':
	main()
