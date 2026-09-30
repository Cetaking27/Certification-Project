import pandas as pd
import numpy as np
#from sqlalchemy import create_engine

from config import Engine


def load_table(table_name):
    """
    Load a SQL Server table into a pandas DataFrame.
    """
    query = f"SELECT * FROM AdventureWorksDW2025.dbo.{table_name}"
    return pd.read_sql(query, Engine)

def main():
    internet_sales_df = load_table("FactInternetSales")
    reseller_sales_df = load_table("FactResellerSales")
    Date_df = load_table("DimDate")
    Product_df = load_table("DimProduct")
    Customer_df = load_table("DimCustomer")
    
    print("=" * 50)
    print("Tables loaded successfully")
    print("=" * 50)
        
    
    print(f"internet_sales_df: {internet_sales_df.shape}")
    print(f"reseller_sales_df: {reseller_sales_df.shape}")
    print(f"Date_df: {Date_df.shape}")
    print(f"Product_df: {Product_df.shape}")
    print(f"Customer_DF:{Customer_df.shape}")
    
    print('#'*50)
    print("\ninternet_sales_df")
    print(internet_sales_df.head(5))
    print(internet_sales_df.tail(5))
    print(internet_sales_df.sample(5))
    
    print(internet_sales_df.dtypes)
    print(internet_sales_df.columns)

 
if __name__ == "__main__":
    main()
    
    