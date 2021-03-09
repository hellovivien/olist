import sqlite3 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


conn = create_connection("olist.db")
# select_all_tasks(conn)

q1 = "SELECT COUNT(DISTINCT customer_unique_id) FROM customers"
q2 = "SELECT COUNT(DISTINCT product_id) FROM products"
q3 = "SELECT product_category_name, COUNT(product_id) FROM products GROUP BY product_category_name"
q4 = "SELECT COUNT(DISTINCT order_id) FROM orders"
q5 = "SELECT order_status, COUNT(order_id) FROM orders GROUP BY order_status"
q6 = "SELECT COUNT(*) as orders, strftime('%m-%Y', order_purchase_timestamp) as month from orders group by month ORDER BY order_purchase_timestamp;"
q7 = "SELECT order_id, AVG(payment_value) FROM order_payments"
q8 = "SELECT AVG(review_score) as score_moyen FROM order_reviews"
q9 = "SELECT COUNT(DISTINCT seller_id) FROM sellers"
q10 = "SELECT seller_state, COUNT(seller_id) FROM sellers GROUP BY seller_state"
q11 = "SELECT product_category_name,COUNT(order_item_id) FROM products INNER JOIN order_items ON products.product_id = order_items.product_id GROUP BY products.product_category_name;"
q12 = "SELECT AVG(orders) as 'order/day' FROM (SELECT COUNT(*) as orders, strftime('%d-%m-%Y', order_purchase_timestamp) as days from orders group by days);"
q13 = "SELECT Cast(AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)) AS Integer) AS days FROM orders"
q14 = "SELECT seller_city , COUNT(order_item_id) FROM order_items INNER JOIN sellers ON order_items.seller_id = sellers.seller_id  GROUP BY sellers.seller_city;"
q15 = "SELECT MIN(payment_value) FROM order_payments;"
q16 = "SELECT MAX(payment_value) FROM order_payments;"
q17 = "SELECT Cast(AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)) AS Integer) AS days, strftime('%m-%Y', order_purchase_timestamp) FROM orders group by strftime('%m-%Y', order_purchase_timestamp) ORDER BY order_purchase_timestamp"


def add_requete(conn, query):
        
    cur = conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()
    
    i = 0
    for row in rows:
        print(row)
        i += 1
        if i >= 5 :
            break

add_requete(conn, q1)
add_requete(conn, q2)
add_requete(conn, q3)
add_requete(conn, q4)
add_requete(conn, q5)
add_requete(conn, q6)
add_requete(conn, q7)
add_requete(conn, q8)
add_requete(conn, q9)
add_requete(conn, q10)  
add_requete(conn, q11)
add_requete(conn, q12)
add_requete(conn, q13)
add_requete(conn, q14)
add_requete(conn, q15)
add_requete(conn, q16)
add_requete(conn, q17)
