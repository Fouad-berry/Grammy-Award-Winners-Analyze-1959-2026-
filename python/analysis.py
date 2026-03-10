# Analyse des Grammy Awards (1959-2026)
# Ce script charge, explore et visualise les données du fichier grammy_awards.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le dataset
def load_data(path='../dataset/grammy_awards.csv'):
    df = pd.read_csv(path)
    return df

def main():
    df = load_data()
    print('Aperçu des données:')
    print(df.head())
    print('\nColonnes:', df.columns.tolist())
    print('\nNombre de lignes:', len(df))
    # Ajoute ici d'autres analyses/explorations

if __name__ == '__main__':
    main()
