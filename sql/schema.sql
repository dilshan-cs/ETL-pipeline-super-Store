-- ==========================================
-- Create Dimension Tables
-- ==========================================

CREATE TABLE IF NOT EXISTS DIM_CUSTOMER (

    Customer_Key SERIAL PRIMARY KEY,

    Customer_ID VARCHAR(20) NOT NULL,

    Customer_Name VARCHAR(100) NOT NULL,

    Segment VARCHAR(20) NOT NULL

);


CREATE TABLE IF NOT EXISTS DIM_PRODUCT (

    Product_Key SERIAL PRIMARY KEY,

    Product_ID VARCHAR(30) NOT NULL,

    Product_Name VARCHAR(255) NOT NULL,

    Category VARCHAR(50) NOT NULL,

    Sub_Category VARCHAR(50) NOT NULL

);


CREATE TABLE IF NOT EXISTS DIM_LOCATION (

    Location_Key SERIAL PRIMARY KEY,

    Postal_Code VARCHAR(20),

    Country VARCHAR(50),

    Region VARCHAR(50),

    State VARCHAR(50),

    City VARCHAR(50)

);


CREATE TABLE IF NOT EXISTS DIM_TIME (

    Time_Key SERIAL PRIMARY KEY,

    Full_Date DATE NOT NULL UNIQUE,

    Year INTEGER,

    Quarter INTEGER,

    Month INTEGER,

    Month_Name VARCHAR(20),

    Day INTEGER,

    Day_of_Week INTEGER,

    Is_Weekend BOOLEAN

);


-- ==========================================
-- Create Fact Table
-- ==========================================

CREATE TABLE IF NOT EXISTS FACT_SALES (

    Row_ID INTEGER PRIMARY KEY,

    Customer_Key INTEGER NOT NULL,

    Product_Key INTEGER NOT NULL,

    Location_Key INTEGER NOT NULL,

    Order_Date_Key INTEGER NOT NULL,

    Ship_Date_Key INTEGER NOT NULL,

    Order_ID VARCHAR(30),

    Ship_Mode VARCHAR(50),

    Sales NUMERIC(12,2),

    Quantity INTEGER,

    Discount NUMERIC(5,2),

    Profit NUMERIC(12,2),

    CONSTRAINT fk_customer
        FOREIGN KEY (Customer_Key)
        REFERENCES DIM_CUSTOMER(Customer_Key),

    CONSTRAINT fk_product
        FOREIGN KEY (Product_Key)
        REFERENCES DIM_PRODUCT(Product_Key),

    CONSTRAINT fk_location
        FOREIGN KEY (Location_Key)
        REFERENCES DIM_LOCATION(Location_Key),

    CONSTRAINT fk_order_time
        FOREIGN KEY (Order_Date_Key)
        REFERENCES DIM_TIME(Time_Key),

    CONSTRAINT fk_ship_time
        FOREIGN KEY (Ship_Date_Key)
        REFERENCES DIM_TIME(Time_Key)

);