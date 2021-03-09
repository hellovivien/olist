# **Rapport du projet  E-COMMERCE**

*Giovanny, Vivien et Farid*

**HOWTO**

1. open **start.ipynb** and exec first block to create database (you must have csv files inside csv folders) 
2. - rich version : ```pip install prettytable``` and ```python main.py```
   - simple version : ```python queries.py```

## 1 -  Création de la base de donnée.

Nous avons choisi d'utiliser SQLite pour simplifier le développement (on a juste à effacer un fichier pour réinitialiser la base) et faciliter le partage de code (pas de paramètres de connexions).

Tout d'abord il a fallu créer une base de données que nous avons nommé **olist.db** ensuite voir fichier main de la ligne 56 à 81 le code permet la convertion des **fichiers csv** à la base de données **olist.db.**

Il y avait un souci avec le fichier **csv** "product_category_name" que nous avons résolue grâce à la variable **fields** qui corrige cette erreur.

Ensuite il y a eu la création de olist.sql avec les tables et l'ajout des information telle que les clés primaires et secondaires. 

/_\  attention nous avons remarqué dans la base de donnée des doublons de clé primaires

**UPDATE**

Nous avons finalement utiliser PANDAS (voir notebook) qui permet de générer le code SQL des tables depuis un Dataframe. Ce code a ensuite été modifié à la main pour  corriger les datatypes et ajouter les clés primaires et les clés étrangères puis toujours avec pandas nous avons converti le contenu du dataframe en sql pour réaiser les inserts.



## 2- Requêtes

Pour cela nous avons utilisé des requêtes qui permettent l'utilisation de la base de données **olist.db**  et en ressortir les informations que nous recherchions ce qui nous a permis de répondre aux questions suivante.

Par la suite nous avons crée une méthode **add_requete**  avec une boucle for qui permet de recupéré toute les infos demandée dans ma requête et limiter la recherche à 5 lignes.

Ensuite nous appelons la méthode **add_requete** avec les deux valeur demandée qui son **conn** pour la connextion et **q1** qui correspond à la variable question1 avec la requête correspondante.

Parallement le code a été adapté en objet dans une version plus riche : **main.py** et en pandas sous forme d'un notebook : **queries.ipynb** (voir ci-dessous).



## 3-  Amélioration et correction de la base de donnée:

Pour corriger les données améliorer la structure de la base nous avons rédiger un notebook (cf **start.ipynb**) avec pour chaque table les problèmes identifiés et les solutions proposées. Nous avons pu traduire une partie de ces solutions en python avec pandas (le code est présent dans le notebook).



# ANNEXES

## Requêtes SQL

**Question 1** : Nombre de client total 

| COUNT customer_unique_id |
| ------------------------ |
| 96096                    |

**Question 2**  : Nombre de produit total 

| DISTINCT product id |
| ------------------- |
| 32951               |

**Question 3** :  Nombre de produit par catégorie

| product_category_name     | COUNT (product_id) |
| ------------------------- | ------------------ |
|                           | 610                |
| agro_industria_e_comercio | 74                 |
| alimentos                 | 82                 |
| alimentos_bebidas         | 104                |
| artes                     | 55                 |

LIMIT 5 info

**Question 4 :**  Nombre de commande total 

| COUNT(dinstinct order_id) |
| ------------------------- |
| 99441                     |

**Question 5** :  Nombre de commande selon leurs états

| order_status | count(ORDER_ID) |
| ------------ | --------------- |
| APPROVED     | 2               |
| CANCELED     | 625             |
| CREATED      | 5               |
| DELIVERED    | 96478           |
| INVOICED     | 314             |

Limit 5 info



**Question 6** : Nombre de commande par mois

| orders | month   |
| ------ | ------- |
| 4      | 9-2016  |
| 324    | 10-2016 |
| 1      | 12-2016 |
| 800    | 01-2017 |
| 1780   | 02-2017 |

**Question 7** : Prix moyen d'une commande

154.10



**Question 8** : Score de satifaction moyen

4,07

**Question 9** : Nombre de vendeur

3095



**Question 10** :  Nombre de vendeur par région 

| SELLER_DATE | COUNT(SELLER_ID) |
| ----------- | ---------------- |
| AC          | 1                |
| AM          | 1                |
| BA          | 19               |
| CE          | 13               |
| DF          | 30               |





#### Pour aller plus loin:



**Question 11 **:   Quantité de produit vendue par catégorie 

| product_category_name     | COUNT(order_item_id) |
| ------------------------- | -------------------- |
|                           | 1603                 |
| agro_industria_e_comercio | 212                  |
| alimentos                 | 510                  |
| alimento_bebidas          | 278                  |
| artes                     | 209                  |

**Question 12:**  Nombre de commande par jours

156.85

**Question 13:** Durée moyenne entre la commande et la livraison

12 jours

**Question 14:**  Nombre de commande par ville (ville du vendeur)



| seller_city     | COUNT(order_item_id) |
| --------------- | -------------------- |
| 04482255        | 1                    |
| abadia de goias | 1                    |
| afonson claudio | 6                    |
| aguas claras df | 1                    |
| alambari        | 5                    |

**Question 15:** Prix minimum des commandes

0€

**Question 16:**  Prix maximum des commandes

13664.08€

**Question 17:**  Le temps moyen d'une livraison par mois

| days | month   |
| ---- | ------- |
| 54   | 09-2016 |
| 19   | 10-2016 |
| 4    | 12-2016 |
| 12   | 01-2017 |
| 13   | 02-2017 |





## Requêtes pandas 

- - -

### import et préparation des variables

```python
import pandas as pd
import datetime

customers_df      = pd.read_csv("./dataset/olist_customers_dataset.csv")
products_df       = pd.read_csv("./dataset/olist_products_dataset.csv")
sellers_df        = pd.read_csv("./dataset/olist_sellers_dataset.csv")
orders_df         = pd.read_csv("./dataset/olist_orders_dataset.csv")
order_payments_df = pd.read_csv("./dataset/olist_order_payments_dataset.csv")
order_reviews_df  = pd.read_csv("./dataset/olist_order_reviews_dataset.csv")
order_items_df    = pd.read_csv("./dataset/olist_order_items_dataset.csv")
geolocation_df    = pd.read_csv("./dataset/olist_geolocation_dataset.csv")
#category_df = pd.read_csv("./datasets/category.csv")
```

## Data Cleaning

### Geolocation

Suppression de 261831 doublons de la tavle geolocation :

(utilisé ['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'])

```python
clean_geo_df = geolocation_df.drop_duplicates(subset=['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'])
```

### Payments

3 paiements ont un type de paiement non défini et un montant de 0 on peut les supprimmer ainsi que 6 autres paiements par bon d'achat avec un montant de 0
clean_pay_df = order_payments_df[order_payments_df.payment_value != 0]

### Products

supprimer trois colonnes : 

- product_name_lenght
- product_description_lenght
- product_photos_qty

```python
clean_products_df = products_df.drop(["product_name_lenght", "product_description_lenght", "product_photos_qty"], axis="columns")
```

## Requêtes

### Nombre de clients total

```python
total_customers = customers_df.customer_id.count()
```

### Nombre de produits total

```python
total_products = products_df.product_id.count()
```

### Nombre de commandes total

```python
total_orders = orders_df.order_id.count()
```

### Nombre de commandes selon leurs états (en cours de livraison etc...)

```python
total_orders_by_status = orders_df.order_status.value_counts()
```

### Nombre de commandes par mois

```python
orders_df["month"] = pd.DatetimeIndex(orders_df.order_purchase_timestamp).month

total_orders_by_month = orders_df.month.value_counts().sort_index()
```

### Panier moyen d'un client

```python
mean_payment = order_payments_df.payment_value.mean()
```

### Score de satisfaction moyen (notation sur la commande)

```python
mean_reviews = order_reviews_df.review_score.mean()
```

### Nombre de vendeurs

```python
total_sellers = sellers_df.seller_id.count()
```

### Nombre de vendeurs par région

```python
total_sellers_by_state = sellers_df.seller_state.value_counts()
```

### Durée moyenne entre la commande et la livraison

```python
delivered = pd.to_datetime(orders_df.order_delivered_customer_date)
purchase = pd.to_datetime(orders_df.order_purchase_timestamp)

mean_time = (delivered - purchase).mean()
```

### Quantité de produit vendu par catégorie

```python
# fusion des tables order_items_df et products_df
merged_order_items = pd.merge(order_items_df,products_df)

sold_by_category = merged_order_items_df.product_category_name.value_counts().sort_index()
```

### Nombre de commande par jours

```python
# création d'une nouvelle colonne date à partir du order_purchase_timestamp
orders_df["date"] = pd.DatetimeIndex(orders_df.order_purchase_timestamp).date

total_orders_by_date = orders_df.date.value_counts().sort_index()
```

### Nombre de commande par ville (ville du vendeur)

```python
# fusion des tables order_items_df et sellers_df
merged_items_seller_df = pd.merge(order_items_df, sellers_df)

total_orders_by_seller_city = merged_items_seller_df.seller_city.value_counts().sort_index()
```

### Prix minimum des commandes

```python
# fusion des tables orders_df et order_payments_df
merged_payment = pd.merge(orders_df, order_payments_df)
# utilisation des tuples avec le statut livré uniquement
merged_payment = merged_payment.loc[merged_payment["order_status"] == "delivered"]

min_order_value = merged_payment.payment_value.min()
```

### Prix maximum des commandes

```python
max_order_value = order_payments_df.payment_value.max()
```