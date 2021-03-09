CREATE TABLE category_name_translation(
   product_category_name         VARCHAR(50)  PRIMARY KEY
  ,product_category_name_english VARCHAR(50) 
);


CREATE TABLE customers(
   customer_id              VARCHAR(255) PRIMARY KEY
  ,customer_unique_id       VARCHAR(255)
  ,customer_zip_code_prefix VARCHAR(5) 
  ,customer_city            VARCHAR(50) 
  ,customer_state           VARCHAR(5)
  ,FOREIGN KEY(customer_zip_code_prefix) REFERENCES geolocation(geolocation_zip_code_prefix) 
);

CREATE TABLE geolocation(
   geolocation_zip_code_prefix VARCHAR(5)
  ,geolocation_lat             FLOAT 
  ,geolocation_lng             FLOAT 
  ,geolocation_city            VARCHAR(50) 
  ,geolocation_state           VARCHAR(5)
);

CREATE TABLE order_items(
   order_id            VARCHAR(255)
  ,order_item_id       VARCHAR(255)  --???
  ,product_id          VARCHAR(255) 
  ,seller_id           VARCHAR(255) 
  ,shipping_limit_date DATE
  ,price               FLOAT
  ,freight_value       FLOAT
  ,FOREIGN KEY(order_id) REFERENCES orders(order_id)
  ,FOREIGN KEY(product_id) REFERENCES products(product_id)
  ,FOREIGN KEY(seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE order_payments(
   order_id             VARCHAR(255)
  ,payment_sequential   BOOL  
  ,payment_type         VARCHAR(50) 
  ,payment_installments INT  
  ,payment_value        FLOAT
  ,FOREIGN KEY(order_id) REFERENCES orders(order_id) 
);


CREATE TABLE order_reviews(
   review_id               VARCHAR(255)
  ,order_id                VARCHAR(255) 
  ,review_score            INT  
  ,review_comment_title    VARCHAR(50)
  ,review_comment_message  VARCHAR(255)
  ,review_creation_date    DATE
  ,review_answer_timestamp TIMESTAMP
  ,FOREIGN KEY(order_id) REFERENCES orders(order_id) 
);

CREATE TABLE orders(
   order_id                      VARCHAR(255) PRIMARY KEY
  ,customer_id                   VARCHAR(32) 
  ,order_status                  VARCHAR(50) 
  ,order_purchase_timestamp      TIMESTAMP
  ,order_approved_at             DATE 
  ,order_delivered_carrier_date  DATE
  ,order_delivered_customer_date DATE
  ,order_estimated_delivery_date DATE
  ,FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE products(
   product_id                 VARCHAR(255)  PRIMARY KEY
  ,product_category_name      VARCHAR(50) 
  ,product_name_lenght        INT  
  ,product_description_lenght INT  
  ,product_photos_qty         INT  
  ,product_weight_g           INT  
  ,product_length_cm          INT  
  ,product_height_cm          INT  
  ,product_width_cm           INT
  ,FOREIGN KEY(product_category_name) REFERENCES category_name_translation(product_category_name)  
);

CREATE TABLE sellers(
   seller_id              VARCHAR(255)  PRIMARY KEY
  ,seller_zip_code_prefix VARCHAR(5)  
  ,seller_city            VARCHAR(50) 
  ,seller_state           VARCHAR(5)
  ,FOREIGN KEY(seller_zip_code_prefix) REFERENCES geolocation(geolocation_zip_code_prefix) 
);