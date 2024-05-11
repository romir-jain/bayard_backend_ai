import psycopg2

# PostgreSQL database connection
DATABASE_URL = "postgres://bayard:Asu690PTw4u4wVoXp72dzE4TuJR6xTew@dpg-cov78c21hbls73dll1t0-a.oregon-postgres.render.com/bayard_3xol"

def create_keys_table():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create the keys table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS keys (
                api_key VARCHAR(255) PRIMARY KEY
            );
        """)

        conn.commit()
        print("Keys table created successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating keys table: {str(error)}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_keys_table()