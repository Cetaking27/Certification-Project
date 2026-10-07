import urllib.parse
from sqlalchemy import create_engine


SERVER = r"localhost\SQLEXPRESS"
DATABASE = "AdventureWorksDW2025"
DRIVER = "ODBC Driver 18 for SQL Server"

odbc_str = (  
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
    f"Encrypt=optional;"
)

params = urllib.parse.quote_plus(odbc_str)
#Windows Authentification
CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={params}"
Engine = create_engine(CONNECTION_STRING)

if __name__ == "__main__":
    try:
        with Engine.connect() as conn:
            print("successfully connectec to SQL server using Windows Autentification")
    except Exception as e:
        print(f"Connection failed: {e}")