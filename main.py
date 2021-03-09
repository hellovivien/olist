import sqlite3
from prettytable import PrettyTable


class Database:
    def __init__(self):
        self._conn = sqlite3.connect("olist.db")
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def last_id(self):
        return self.cursor.lastrowid()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def query_with_cols(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        fields = [i[0] for i in self.cursor.description]
        return fields, self.fetchall()

    def queryOne(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchone()


files = {
    "product_category_name_translation.csv" : "category_name_translation",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv" : "products",
    "olist_orders_dataset.csv" : "orders",
    "olist_order_payments_dataset.csv" : "order_payments",
    "olist_order_items_dataset.csv" : "order_items",
    "olist_order_reviews_dataset.csv" : "order_reviews",
    "olist_sellers_dataset.csv" : "sellers",
}


with Database() as db:
    queries = {
        "Nombre de client total" :
        "SELECT COUNT(DISTINCT customer_unique_id) as customers FROM customers",

        "Nombre de produits" :
        "SELECT COUNT(*) as products FROM products",

        "Nombre de produit par catégorie" :
        "SELECT product_category_name as category, COUNT(*) as products FROM products GROUP BY product_category_name ORDER BY products",

        "Nombre de commande total":
        "SELECT COUNT(*) as orders_count FROM orders",

        "Nombre de commande selon leurs états" :
        "SELECT order_status as status, COUNT(*) as orders FROM orders GROUP BY order_status ORDER BY orders",

        "Nombre de commande par mois" :
        "SELECT COUNT(*) as orders, strftime('%m-%Y', order_purchase_timestamp) as month from orders group by month ORDER BY order_purchase_timestamp",

        "Prix moyen d'une commande " :
        "SELECT AVG(payment_value) as panier_moyen FROM order_payments",

        "Score de satisfaction moyen" :
        "SELECT AVG(review_score) as score_moyen FROM order_reviews",

        # "BONUS : Score de satisfaction moyen par vendeur (100 permiers)" : """
        #     SELECT AVG(seller_score) as avg_score, seller FROM(
        #         SELECT SUM(review_score) as seller_score, items.seller_id as seller FROM order_reviews as reviews
        #             INNER JOIN order_items as items ON items.order_id = reviews.order_id
        #         GROUP BY reviews.order_id
        #     )GROUP BY seller ORDER BY avg_score DESC LIMIT 100
        # """,

        "Nombre de vendeur" :
        "SELECT COUNT(*) as sellers FROM sellers",

        "Nombre de vendeur par région" :
        "SELECT COUNT(*) as sellers, seller_state as state FROM sellers GROUP BY seller_state ORDER BY sellers",

        "Quantité de produit vendu par catégorie" :
        "SELECT COUNT(*) as products, p.product_category_name as category FROM order_items as items INNER JOIN products AS p ON p.product_id = items.product_id GROUP BY p.product_category_name ORDER BY products",

        "Nombre de commande par jours" :
        "SELECT AVG(orders) as 'order/day' FROM (SELECT COUNT(*) as orders, strftime('%d-%m-%Y', order_purchase_timestamp) as days from orders group by days)",
        
        "Durée moyenne entre la commande et la livraison":
        "SELECT Cast(AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)) AS Integer) AS days FROM orders",

        "Nombre de commande par ville (ville du vendeur)":
        "SELECT seller_city as city, COUNT(o.order_id) AS orders FROM sellers as s INNER JOIN order_items as o ON o.seller_id = s.seller_id GROUP BY seller_city ORDER BY orders",

        "Prix maximum et minimum des commandes":
        "SELECT MAX(payment_value) as max, MIN(payment_value) as min FROM order_payments",

        "Le temps moyen d'une livraison par mois":
        "SELECT Cast(AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)) AS Integer) AS days, strftime('%m-%Y', order_purchase_timestamp) FROM orders group by strftime('%m-%Y', order_purchase_timestamp) ORDER BY order_purchase_timestamp"
    }


    for question, query in queries.items():
        print(question)
        fields, data = db.query_with_cols(query)
        x = PrettyTable()
        x.field_names = fields
        x.add_rows(data)
        print(x)
        input("press to continue")

    
    db.execute("INSERT INTO products (product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm) VALUES('test', 100, 100, 1, 100, 10, 10, 10)")
    print("ADD PRODUCT 'TEST' DONE")