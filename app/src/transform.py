import pandas as pd


def create_dim_product(df):
    """
    Create Product Dimension Table
    """
    try:

        dim_product = (
            df[
                [
                    "Product ID",
                    "Product Name",
                    "Category",
                    "Sub-Category"
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        # Create Surrogate Key
        dim_product.insert(
            0,
            "Product Key",
            range(1, len(dim_product) + 1)
        )

        return dim_product
    except Exception as e:
        print(f"Error creating dim_product: {e}")
        return None

def create_dim_customer(df):
    """
    Create Customer Dimension Table
    """

    try:

        dim_customer = (
            df[
                [
                    "Customer ID",
                    "Customer Name",
                    "Segment"                
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        dim_customer.insert(
            0,
            "Customer Key",
            range(1, len(dim_customer) + 1)
        )

        return dim_customer
    except Exception as e:
        print(f"Error creating dim_customer: {e}")
        return None

def create_dim_location(df):
    """
    Create Location Dimension Table
    """

    try:
    
        dim_location = (
            df[
                [
                "Postal Code",
                "Country",
                "Region",
                "State",
                "City"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
        )

        dim_location.insert(
            0,
            "Location Key",
            range(1, len(dim_location) + 1)
        )

        return dim_location
    except Exception as e:
        print(f"Error creating dim_location: {e}")
        return None

# def create_dim_time(df):
#     """
#     Create Time Dimension Table
#     """

#     try:

#         time = pd.DataFrame()

#         time["Full Date"] = pd.to_datetime(df["Order Date"]) 

#         time = time.drop_duplicates().reset_index(drop=True)

#         time["Year"] = time["Full Date"].dt.year
#         time["Quarter"] = time["Full Date"].dt.quarter
#         time["Month"] = time["Full Date"].dt.month
#         time["Month Name"] = time["Full Date"].dt.month_name()
#         time["Day"] = time["Full Date"].dt.day
#         time["Day of Week"] = time["Full Date"].dt.day_name()
#         time["Is Weekend"] = (time["Day of Week"] == "Saturday") | (time["Day of Week"] == "Sunday") 
    

#         time.insert(
#             0,
#             "Time Key",
#             range(1, len(time) + 1)
#         )

#         return time
#     except Exception as e:
#         print(f"Error creating dim_time: {e}")
#         return None

def create_dim_time(df):
    """
    Create Time Dimension Table
    """

    try:

        # Combine Order Date and Ship Date
        all_dates = pd.concat([
            pd.to_datetime(df["Order Date"]),
            pd.to_datetime(df["Ship Date"])
        ])

        # Remove duplicates and sort
        all_dates = (
            all_dates
            .drop_duplicates()
            .sort_values()
            .reset_index(drop=True)
        )

        # Create Time Dimension
        dim_time = pd.DataFrame({
            "Full Date": all_dates
        })

        dim_time["Year"] = dim_time["Full Date"].dt.year
        dim_time["Quarter"] = dim_time["Full Date"].dt.quarter
        dim_time["Month"] = dim_time["Full Date"].dt.month
        dim_time["Month Name"] = dim_time["Full Date"].dt.month_name()
        dim_time["Day"] = dim_time["Full Date"].dt.day

        # Monday = 0 ... Sunday = 6
        dim_time["Day of Week"] = dim_time["Full Date"].dt.dayofweek

        dim_time["Is Weekend"] = (
            dim_time["Day of Week"] >= 5
        )

        dim_time.insert(
            0,
            "Time_Key",
            range(1, len(dim_time) + 1)
        )

        return dim_time

    except Exception as e:

        print(f"Error creating dim_time: {e}")

        return None

def create_fact_sales(df,dim_product,dim_customer,dim_location,dim_time):    
    try:
        fact = df.copy()

        # -----------------------------------------
        # Merge Product Dimension
        # -----------------------------------------
        fact = fact.merge(
            dim_product,
            on=[
                "Product ID",
                "Product Name",
                "Category",
                "Sub-Category"
            ],
            how="left"
        )

        # -----------------------------------------
        # Merge Customer Dimension
        # -----------------------------------------
        fact = fact.merge(
            dim_customer,
            on=[
                "Customer ID",
                "Customer Name",
                "Segment"
            ],
            how="left"
        )

        # -----------------------------------------
        # Merge Location Dimension
        # -----------------------------------------
        fact = fact.merge(
            dim_location,
            on=[
                "Postal Code",
                "Country",
                "Region",
                "State",
                "City"
            ],
            how="left"
        )

        # -----------------------------------------
        # Merge Order Date
        # -----------------------------------------
        order_time = dim_time.rename(
            columns={
                "Full Date": "Order Date",
                "Time_Key": "Order_Date_Key"
            }
        )

        fact = fact.merge(
            order_time[
                [
                    "Order Date",
                    "Order_Date_Key"
                ]
            ],
            on="Order Date",
            how="left"
        )

        # -----------------------------------------
        # Merge Ship Date
        # -----------------------------------------
        ship_time = dim_time.rename(
            columns={
                "Full Date": "Ship Date",
                "Time_Key": "Ship_Date_Key"
            }
        )

        fact = fact.merge(
            ship_time[
                [
                    "Ship Date",
                    "Ship_Date_Key"
                ]
            ],
            on="Ship Date",
            how="left"
        )

        # -----------------------------------------
        # Select Fact Table Columns
        # -----------------------------------------
        fact_sales = fact[
            [
                "Row ID",
                "Customer Key",
                "Product Key",
                "Location Key",
                "Order_Date_Key",
                "Ship_Date_Key",
                "Order ID",
                "Ship Mode",
                "Sales",
                "Quantity",
                "Discount",
                "Profit"
            ]
        ].copy()

        # Rename to match SQL table
        fact_sales.rename(
            columns={
                "Row ID": "Row_ID",
                "Order ID": "Order_ID",
                "Ship Mode": "Ship_Mode"
            },
            inplace=True
        )

        return fact_sales

    except Exception as e:

        print(f"Error creating fact_sales: {e}")

        return None
    


def save_processed_data(
    dim_product,
    dim_customer,
    dim_location,
    dim_time,
    fact_sales
):
    """
    Save all transformed tables to CSV files.
    """

    dim_product.to_csv(
        "/app/data/processed/dim_product.csv",
        index=False
    )

    dim_customer.to_csv(
        "/app/data/processed/dim_customer.csv",
        index=False
    )

    dim_location.to_csv(
        "/app/data/processed/dim_location.csv",
        index=False
    )

    dim_time.to_csv(
        "/app/data/processed/dim_time.csv",
        index=False
    )

    fact_sales.to_csv(
        "/app/data/processed/fact_sales.csv",
        index=False
    )

    print("All processed tables saved successfully!")