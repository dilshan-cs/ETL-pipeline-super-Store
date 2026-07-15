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


    connection = get_connection()

    if connection is None:
        print("Database connection failed.")
        return
    print("Database connected successfully!\n")

    df = extract_data()

    if df is None:
        print("Extract failed.")
        connection.close()
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

    except Exception as e:
        print(f"Transform failed: {e}")
        connection.close()
        return


    
    
    connection.close()
    print("\n========== ETL Pipeline Finished ==========")    

if __name__ == "__main__":
    main()