from load import load_table
import time
from database import get_connection
from extract import extract_data
from transform import(
    create_dim_product,
    create_dim_customer,
    create_dim_location,
    create_dim_time,
    create_fact_sales,
    save_processed_data
)

def main():

    print("========== ETL Pipeline Started ==========")

    conn = None
    for i in range(10):
        conn = get_connection()

        if conn:
            print("Connected!")
            break

        print("Waiting for PostgreSQL...")
        time.sleep(3)

    if conn is None:
        print("Database connection failed.")
        return
    print("Database connected successfully!\n")

    df = extract_data()

    if df is None:
        print("Extract failed.")
        conn.close()
        return
    print("Data extracted successfully!\n")
    print(df)


    try:        
        dim_product = create_dim_product(df)
        dim_customer = create_dim_customer(df)
        dim_location = create_dim_location(df)
        dim_time = create_dim_time(df)
        fact_sales = create_fact_sales(
            df,
            dim_product,
            dim_customer,
            dim_location,
            dim_time
        )

        save_processed_data(
            dim_product,
            dim_customer,
            dim_location,
            dim_time,
            fact_sales
        )
        
        print(dim_product.columns.tolist())
        print(dim_product.head())
        print(dim_customer.columns.tolist())
        print(dim_customer.head())
        print(dim_location.columns.tolist())
        print(dim_location.head())
        print(dim_time.columns.tolist())
        print(dim_time.head()) 

        print("\nDimensions created successfully!\n")

        print(fact_sales.columns.tolist())
        print(fact_sales.head()) 

        print("\nFact table created successfully!\n")
        print("Data transforms successfully!\n")

        
    except Exception as e:
        print(f"Transform failed: {e}")
        conn.close()
        return


    try:
        print("========== Loading into PostgreSQL ==========")

        load_table(dim_product, "DIM PRODUCT")

        load_table(dim_customer, "DIM CUSTOMER")

        load_table(dim_location, "DIM LOCATION")

        load_table(dim_time, "DIM TIME")

        load_table(fact_sales, "FACT SALES")

        print("Data loaded successfully!")
    
    except Exception as e:
        print(f"Load failed: {e}")
        conn.close()
        return
    
    conn.close()
    print("\n========== ETL Pipeline Finished ==========")    

if __name__ == "__main__":
    main()