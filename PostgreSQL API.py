from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# PostgreSQL connection settings
DB_NAME = "testdb"
DB_USER = "hunukcho"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Folder where images are stored
IMAGE_FOLDER = "/Users/hunukcho/Desktop/Capstone/bad/"

@app.post("/upload-images/")
def upload_images_to_db():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # Create table if not exists
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

    # Get image files
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        cur.close()
        conn.close()
        return {"message": "No image files found in folder."}

    data_to_insert = [
        ("Plant A", 101, "OP-2024", "OP123", filename.split('.')[0], os.path.join(IMAGE_FOLDER, filename), True, None)
        for filename in image_files
    ]

    cur.executemany("""
        INSERT INTO images (plant_name, line_number, operation_number, operator_id, serial_number, path_to_image, test_result, failure_reason)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, data_to_insert)

    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"{len(image_files)} image files inserted into database."}
