import duckdb

# Conexión a la base de datos DuckDB
DB_FILE = "iot_data.duckdb"
connection = duckdb.connect(database=DB_FILE, read_only=False)

def initialize_database():


    
    connection.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    """)

    connection.execute("""
    CREATE SEQUENCE IF NOT EXISTS seq_companyid START 1;
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY,
        company_name TEXT NOT NULL,
        company_api_key TEXT UNIQUE NOT NULL
    );
    """)

    connection.execute("""
    CREATE SEQUENCE IF NOT EXISTS seq_locationid START 1;
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        company_id INTEGER NOT NULL,
        location_name TEXT NOT NULL,
        location_country TEXT,
        location_city TEXT,
        location_meta TEXT,
        FOREIGN KEY (company_id) REFERENCES company(id)
    );
    """)

    connection.execute("""
    CREATE SEQUENCE IF NOT EXISTS seq_sensorid START 1;
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS sensor (
        id INTEGER PRIMARY KEY,
        location_id INTEGER NOT NULL,
        sensor_name TEXT NOT NULL,
        sensor_category TEXT,
        sensor_meta TEXT,
        sensor_api_key TEXT UNIQUE NOT NULL,
        FOREIGN KEY (location_id) REFERENCES location(id)
    );
    """)

    connection.execute("""
    CREATE SEQUENCE IF NOT EXISTS seq_sensor_dataid START 1;
    """)

    connection.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY,
        sensor_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        data JSON NOT NULL,
        FOREIGN KEY (sensor_id) REFERENCES sensor(id)
    );
    """)
