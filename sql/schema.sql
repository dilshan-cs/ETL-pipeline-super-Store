-- ==========================================
-- Create Dimension Tables
-- ==========================================

CREATE TABLE IF NOT EXISTS "DIM CUSTOMER" (

    "Customer Key" SERIAL PRIMARY KEY,

    "Customer ID" VARCHAR(20) NOT NULL,

    "Customer Name" VARCHAR(100) NOT NULL,

    "Segment" VARCHAR(20) NOT NULL

);


CREATE TABLE IF NOT EXISTS "DIM PRODUCT" (

    "Product Key" SERIAL PRIMARY KEY,

    "Product ID" VARCHAR(30) NOT NULL,

    "Product Name" VARCHAR(255) NOT NULL,

    "Category" VARCHAR(50) NOT NULL,

    "Sub-Category" VARCHAR(50) NOT NULL

);


CREATE TABLE IF NOT EXISTS "DIM LOCATION" (

    "Location Key" SERIAL PRIMARY KEY,

    "Postal Code" VARCHAR(20),

    "Country" VARCHAR(50),

    "Region" VARCHAR(50),

    "State" VARCHAR(50),

    "City" VARCHAR(50)

);


CREATE TABLE IF NOT EXISTS "DIM TIME" (

    "Time Key" SERIAL PRIMARY KEY,

    "Full Date" DATE NOT NULL UNIQUE,

    "Year" INTEGER,

    "Quarter" INTEGER,

    "Month" INTEGER,

    "Month Name" VARCHAR(20),

    "Day" INTEGER,

    "Day of Week" INTEGER,

    "Is Weekend" BOOLEAN

);


-- ==========================================
-- Create Fact Table
-- ==========================================

CREATE TABLE IF NOT EXISTS "FACT SALES" (

    "Row ID" INTEGER PRIMARY KEY,

    "Customer Key" INTEGER NOT NULL,

    "Product Key" INTEGER NOT NULL,

    "Location Key" INTEGER NOT NULL,

    "Order_Date_Key" INTEGER NOT NULL,

    "Ship_Date_Key" INTEGER NOT NULL,

    "Order ID" VARCHAR(30),

    "Ship Mode" VARCHAR(50),

    "Sales" NUMERIC(12,2),

    "Quantity" INTEGER,

    "Discount" NUMERIC(5,2),

    "Profit" NUMERIC(12,2),

    CONSTRAINT fk_customer
        FOREIGN KEY ("Customer Key")
        REFERENCES "DIM CUSTOMER"("Customer Key"),

    CONSTRAINT fk_product
        FOREIGN KEY ("Product Key")
        REFERENCES "DIM PRODUCT"("Product Key"),

    CONSTRAINT fk_location
        FOREIGN KEY ("Location Key")
        REFERENCES "DIM LOCATION"("Location Key"),

    CONSTRAINT fk_order_time
        FOREIGN KEY ("Order_Date_Key")
        REFERENCES "DIM TIME"("Time Key"),

    CONSTRAINT fk_ship_time
        FOREIGN KEY ("Ship_Date_Key")
        REFERENCES "DIM TIME"("Time Key")

);