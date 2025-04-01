import psycopg2
import os

# ✅ PostgreSQL connection settings
DB_NAME = "testdb"
DB_USER = "hunukcho"  # Changed from "hunukcho" anyother name
DB_PASSWORD = "password"  # Modify according to your settings
DB_HOST = "localhost"
DB_PORT = "5432"

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# ✅ Create 'images' table if it does not exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        plant_name VARCHAR(50) NOT NULL,
        line_number BIGINT NOT NULL,
        operation_number VARCHAR(50) NOT NULL,
        operator_id VARCHAR(50) NOT NULL,
        serial_number VARCHAR(50) NOT NULL,
        path_to_image TEXT NOT NULL,
        test_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        test_result BOOLEAN NOT NULL,
        failure_reason TEXT NULL
    );
""")
conn.commit()

# ✅ Folder where images are stored (`bad` folder)
image_folder = "/Users/hunukcho/Desktop/Capstone/bad/"

# ✅ Retrieve all image files from the folder (filter extensions: JPG, PNG, JPEG)
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# ✅ Insert multiple data entries at once using executemany
if not image_files:
    print("No image files found! Please check if there are images in the `bad` folder.")
else:
    # Create a list of data to be inserted
    data_to_insert = [
        ("Plant A", 101, "OP-2024", "OP123", filename.split('.')[0], os.path.join(image_folder, filename), True, None)
        for filename in image_files
    ]

    # Use executemany() to insert multiple entries at once
    cur.executemany("""
        INSERT INTO images (plant_name, line_number, operation_number, operator_id, serial_number, path_to_image, test_result, failure_reason)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, data_to_insert)

    conn.commit()
    print(f"{len(image_files)} image file paths have been stored in the database!")

# ✅ Close PostgreSQL connection
cur.close()
conn.close()
