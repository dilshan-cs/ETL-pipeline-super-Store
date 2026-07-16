from database import get_connection


def load_table(df, table_name):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        columns = list(df.columns)

        column_names = ", ".join(f'"{col}"' for col in columns)

        placeholders = ", ".join(["%s"] * len(columns))

        query = f'''
        INSERT INTO "{table_name}"
        ({column_names})
        VALUES ({placeholders})
        '''

        for _, row in df.iterrows():

            cursor.execute(
                query,
                tuple(row.values)
            )

        conn.commit()

        print(f"{table_name} loaded successfully!")

        cursor.close()
        conn.close()

    except Exception as e:

        print(f"Error loading {table_name}: {e}")