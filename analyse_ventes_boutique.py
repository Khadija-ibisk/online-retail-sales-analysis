# Analyse des ventes d'une boutique en ligne

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Chargement des données
print("="*60)
print("CHARGEMENT DES DONNÉES")
print("="*60)

#implementation du fichier Excel avec test voir si c'est bon et retourner le nombre de lignes dans le fichier, sinon afficher un message d'erreur et quitter le programme

try:
    df = pd.read_excel("Data/online_retail_II.xlsx")
    print(f"✓ Fichier chargé : {len(df)} lignes")
except FileNotFoundError:
    print("❌ Fichier introuvable : Data/online_retail_II.xlsx")
    exit()

print("\nColonnes disponibles :")
print(df.columns.tolist())

print("\nAperçu des données :")
print(df.head())

# 2. Nettoyage des données du fichier Excel

print("\n" + "="*60)
print("NETTOYAGE DES DONNÉES")
print("="*60)

lignes_avant = len(df)

# Suppression des doublons si il y'en a
df = df.drop_duplicates()
print(f"✓ Doublons supprimés : {lignes_avant - len(df)}")

# Suppression des valeurs manquantes critiques
df = df.dropna(subset=["Customer ID", "Quantity", "Price"])

# Conversion des types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')
df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

# Suppression des valeurs incohérentes et illogiques

df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Création de la colonne Total
df["Total"] = df["Quantity"] * df["Price"]

lignes_apres = len(df)
print(f"✓ Lignes conservées : {lignes_apres} / {lignes_avant}")

print("\nStatistiques après nettoyage :")
print(df[["Quantity", "Price", "Total"]].describe())

# 3. Analyse du chiffre d'affaires global
print("\n" + "="*60)
print("ANALYSE DU CHIFFRE D'AFFAIRES")
print("="*60)

chiffre_affaires_global = df["Total"].sum()
print(f"\n💰 Chiffre d'affaires global : {chiffre_affaires_global:,.2f} £")

# 4. Analyse des ventes par produit Top 10

print("\n" + "="*60)
print("TOP 10 DES PRODUITS")
print("="*60)

top_produits = (
    df.groupby("Description")["Total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 des produits les plus rentables :")
for i, (produit, ca) in enumerate(top_produits.items(), 1):
    print(f"{i:2d}. {produit[:40]:<40} : {ca:>12,.2f} £")

# Graphiques pour les produits les plus rentables

plt.figure(figsize=(12, 6))
top_produits.plot(kind="bar", color='steelblue')
plt.title("Top 10 des produits les plus rentables", fontsize=14, fontweight='bold')
plt.xlabel("Produit")
plt.ylabel("Chiffre d'affaires (£)")
plt.xticks(rotation=75, ha='right')
plt.tight_layout()
plt.savefig('graph_top10_produits.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : graph_top10_produits.png")
plt.close()

# 5. Analyse par catégorie (si disponible)
if "Category" in df.columns:
    print("\n" + "="*60)
    print("ANALYSE PAR CATÉGORIE")
    print("="*60)
    
    ventes_par_categorie = df.groupby("Category")["Total"].sum()
    
    print("\nVentes par catégorie :")
    print(ventes_par_categorie)

    plt.figure(figsize=(10, 6))
    ventes_par_categorie.plot(kind="bar", color='coral')
    plt.title("Chiffre d'affaires par catégorie")
    plt.xlabel("Catégorie")
    plt.ylabel("Chiffre d'affaires (£)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('graph_categories.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé : graph_categories.png")
    plt.close()

# 6. Calcul du panier moyen et médian

print("\n" + "="*60)
print("ANALYSE DU PANIER MOYEN")
print("="*60)

panier_moyen = df.groupby("Invoice")["Total"].sum().mean()
panier_median = df.groupby("Invoice")["Total"].sum().median()

print(f"\n🛒 Panier moyen  : {panier_moyen:,.2f} £")
print(f"🛒 Panier médian : {panier_median:,.2f} £")

# 7. Analyse temporelle des ventes voir l'évolution mensuelle du chiffre d'affaires
print("\n" + "="*60)
print("ANALYSE TEMPORELLE")
print("="*60)

df["Month"] = df["InvoiceDate"].dt.to_period("M")
ventes_mensuelles = df.groupby("Month")["Total"].sum()

print("\nVentes mensuelles :")
for mois, ca in ventes_mensuelles.items():
    print(f"{str(mois):<10} : {ca:>12,.2f} £")

# Convertir pour matplotlib et éviter les problèmes d'affichage des périodes

ventes_mensuelles.index = ventes_mensuelles.index.astype(str)

plt.figure(figsize=(12, 6))
ventes_mensuelles.plot(kind='line', marker='o', linewidth=2, color='darkblue')
plt.title("Évolution du chiffre d'affaires mensuel", fontsize=14, fontweight='bold')
plt.xlabel("Mois")
plt.ylabel("Chiffre d'affaires (£)")
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_ventes_mensuelles.png', dpi=300, bbox_inches='tight')
print("\n✓ Graphique sauvegardé : graph_ventes_mensuelles.png")
plt.close()

print("\n" + "="*60)
print("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
print("="*60)
print(f"\nGraphiques générés : {len([f for f in os.listdir('.') if f.startswith('graph_')])}")