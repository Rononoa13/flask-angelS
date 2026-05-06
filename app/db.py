import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="awtest",
        user="postgres",
        host="localhost",
        port=5432
    )