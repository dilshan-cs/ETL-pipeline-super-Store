import pandas as pd


def extract_data():
    try:
        
        # Read the CSV file
        df = pd.read_csv("/app/data/raw/Sample - Superstore.csv", encoding="latin1")

        df['Order Date'] = pd.to_datetime(df["Order Date"])
        df['Ship Date'] = pd.to_datetime(df["Ship Date"])

        # remove extra space
        text_columns = df.select_dtypes(include="object").columns
        for column in text_columns:
            df[column] = df[column].str.strip()

        # Print number of rows and columns
        print("Number of rows:", df.shape[0])
        print("Number of columns:", df.shape[1])

        # Print column names
        print("\nColumn Names:")
        print(df.columns.tolist())

        # Print data types
        print("\nData Types:")
        print(df.dtypes)

        # Print missing values
        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        # -----------------------------
        # Check duplicate rows
        # -----------------------------
        duplicate_count = df.duplicated().sum()

        print(f"\nDuplicate Rows: {duplicate_count}")

        if duplicate_count > 0:
            df = df.drop_duplicates()
            print("Duplicate rows removed.")
        else:
            print("No duplicate rows found.")
    
        # Return the DataFrame
        return df

    except Exception as e:
        print(f"Extract failed: {e}")
        return None
