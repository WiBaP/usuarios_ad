import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=;"
        "DATABASE=;"
        "Trusted_Connection=yes;"
    )

def get_connection_linx():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=;"
            "DATABASE=;"
            "Trusted_Connection=yes;"
        )
        return conn

    except Exception as e:
        print("❌ Erro ao conectar no LINX:", e)
        return None
