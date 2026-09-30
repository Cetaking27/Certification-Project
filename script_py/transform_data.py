"""
Purpose:
    Transform raw AdventureWorks data into business-ready
    tables used for VAT calculations.

Inputs:
    - FactInternetSales
    - FactResellerSales
    - DimProduct
    - DimCustomer
    - DimReseller
    - DimDate

Outputs:
    - Sales
    - Purchases
    - TaxAdjustments
"""

import pandas as pd

from load_data import load_table


# ---------- INTERNET SALES ----------

def transform_internet_sales(
    internet_sales_df: pd.DataFrame,
    product_df: pd.DataFrame,
    customer_df: pd.DataFrame,
    tax_rules_table:pd.DataFrame
) -> pd.DataFrame:
    """
    Transform raw Internet sales data into a business-ready Sales table.
    """

    # 1. Copy the source DataFrame
    sales_df = internet_sales_df.copy()

    # 2. Select only the useful sales columns
    sales_columns = [
        "SalesOrderNumber",
        "SalesOrderLineNumber",
        "OrderDate",
        "CustomerKey",
        "ProductKey",
        "OrderQuantity",
        "SalesAmount",
        "TotalProductCost",
        "TaxAmt"
    ]

    sales_df = sales_df[sales_columns].copy()

    # 3. Prepare the product lookup table
    product_columns = [
        "ProductKey",
        "EnglishProductName"
    ]

    product_lookup = product_df[product_columns].copy()

    product_lookup = product_lookup.drop_duplicates(
        subset=["ProductKey"]
    )

    # 4. Enrich sales with product information
    sales_df = sales_df.merge(
        product_lookup,
        on="ProductKey",
        how="left",
        validate="many_to_one"
    )

    # 5. Prepare the customer lookup table
    customer_columns = [
        "CustomerKey",
        "FirstName",
        "LastName"
    ]

    customer_lookup = customer_df[customer_columns].copy()

    customer_lookup = customer_lookup.drop_duplicates(
        subset=["CustomerKey"]
    )

    customer_lookup["BuyerName"] = (
        customer_lookup["FirstName"].fillna("")
        + " "
        + customer_lookup["LastName"].fillna("")
    ).str.strip()

    customer_lookup = customer_lookup[
        [
            "CustomerKey",
            "BuyerName"
        ]
    ]

    # 6. Enrich sales with customer information
    sales_df = sales_df.merge(
        customer_lookup,
        on="CustomerKey",
        how="left",
        validate="many_to_one"
    )

    # 7. Rename technical columns into business-friendly names
    sales_df = sales_df.rename(
        columns={
            "SalesOrderNumber": "InvoiceID",
            "SalesOrderLineNumber": "InvoiceLineNumber",
            "OrderQuantity": "Quantity",
            "TotalProductCost": "CostAmount",
            "TaxAmt": "OutputVAT",
            "EnglishProductName": "ProductName",
            "CustomerKey": "BuyerKey"
        }
    )

    # 8. Add business and tax-related columns
    sales_df["BuyerType"] = "Customer"
    sales_df["Department"] = "Internet Sales"
    sales_df["Province"] = "NB"
    sales_df["TaxCode"] = "STANDARD"

    # 9. Determine the applicable tax rate for each transaction
    sales_df["TaxRate"] = sales_df.apply(
        lambda row: get_tax_rule(
            row["OrderDate"],
            row["TaxCode"],
            row["Province"],
            tax_rules_table
        )[0],
        axis=1
    )

    # 10. Recalculate Output VAT using the applicable tax rate
    sales_df["OutputVAT"] = (
        sales_df["SalesAmount"]
        * sales_df["TaxRate"]
    )

    # 11. Organize the final table
    final_columns = [
        "InvoiceID",
        "InvoiceLineNumber",
        "OrderDate",
        "Department",
        "BuyerType",
        "BuyerKey",
        "BuyerName",
        "ProductKey",
        "ProductName",
        "Quantity",
        "SalesAmount",
        "CostAmount",
        "TaxRate",
        "OutputVAT",
        "Province",
        "TaxCode"
    ]

    sales_df = sales_df[final_columns]

    # 12. Return the transformed DataFrame
    return sales_df


# ---------- RESELLER SALES ----------

def transform_reseller_sales(
    reseller_sales_df: pd.DataFrame,
    product_df: pd.DataFrame,
    reseller_df: pd.DataFrame,
    tax_rules_table: pd.DataFrame
) -> pd.DataFrame:
    """
    Transform raw Reseller sales data into a business-ready Sales table.
    """

    # 1. Copy the source DataFrame
    sales_df = reseller_sales_df.copy()

    # 2. Select only the useful sales columns
    reseller_sales_columns = [
        "SalesOrderNumber",
        "SalesOrderLineNumber",
        "OrderDate",
        "ResellerKey",
        "ProductKey",
        "OrderQuantity",
        "SalesAmount",
        "TotalProductCost",
        "TaxAmt"
    ]

    sales_df = sales_df[reseller_sales_columns].copy()

    # 3. Prepare the product lookup table
    product_columns = [
        "ProductKey",
        "EnglishProductName"
    ]

    product_lookup = product_df[product_columns].copy()

    product_lookup = product_lookup.drop_duplicates(
        subset=["ProductKey"]
    )

    # 4. Enrich sales with product information
    sales_df = sales_df.merge(
        product_lookup,
        on="ProductKey",
        how="left",
        validate="many_to_one"
    )

    # 5. Prepare the reseller lookup table
    reseller_columns = [
        "ResellerKey",
        "ResellerName"
    ]

    reseller_lookup = reseller_df[reseller_columns].copy()

    reseller_lookup = reseller_lookup.drop_duplicates(
        subset=["ResellerKey"]
    )

    # 6. Enrich sales with reseller information
    sales_df = sales_df.merge(
        reseller_lookup,
        on="ResellerKey",
        how="left",
        validate="many_to_one"
    )

    # 7. Rename technical columns into business-friendly names
    sales_df = sales_df.rename(
        columns={
            "SalesOrderNumber": "InvoiceID",
            "SalesOrderLineNumber": "InvoiceLineNumber",
            "OrderQuantity": "Quantity",
            "TotalProductCost": "CostAmount",
            "TaxAmt": "OutputVAT",
            "EnglishProductName": "ProductName",
            "ResellerKey": "BuyerKey",
            "ResellerName": "BuyerName"
        }
    )

  # 8. Add business and tax-related columns
    sales_df["BuyerType"] = "Reseller"
    sales_df["Department"] = "Reseller Sales"
    sales_df["Province"] = "NB"
    sales_df["TaxCode"] = "STANDARD"
    
    # 9. Determine the applicable tax rate for each transaction
    sales_df["TaxRate"] = sales_df.apply(
        lambda row: get_tax_rule(
            row["OrderDate"],
            row["TaxCode"],
            row["Province"],
            tax_rules_table
        )[0],
        axis=1
    )
    
    # 10. Recalculate Output VAT using the applicable tax rate
    sales_df["OutputVAT"] = (
        sales_df["SalesAmount"]
        * sales_df["TaxRate"]
    )
    
    # 11. Organize the final table
    final_columns = [
        "InvoiceID",
        "InvoiceLineNumber",
        "OrderDate",
        "Department",
        "BuyerType",
        "BuyerKey",
        "BuyerName",
        "ProductKey",
        "ProductName",
        "Quantity",
        "SalesAmount",
        "CostAmount",
        "TaxRate",
        "OutputVAT",
        "Province",
        "TaxCode"
    ]
    
    sales_df = sales_df[final_columns]
    
    # 12. Return the transformed DataFrame
    return sales_df


# ---------- BUILD SALES TABLE ----------

def build_sales_tables(
    internet_sales: pd.DataFrame,
    reseller_sales: pd.DataFrame
) -> pd.DataFrame:
    """
    Combine Internet Sales and Reseller Sales into one Sales table.
    """

    sales_table = pd.concat(
        [
            internet_sales,
            reseller_sales
        ],
        ignore_index=True
    )

    return sales_table


# ---------- PURCHASES ----------

def transform_purchases(
    purchases_df: pd.DataFrame,
    product_df: pd.DataFrame,
    date_df: pd.DataFrame
) -> pd.DataFrame:

    # 1. Copy the source DataFrame
    purchases_table = purchases_df.copy()

    # 2. Select only the useful purchase columns
    purchases_columns = [
        "PurchaseID",
        "OrderDateKey",
        "ProductKey",
        "PurchaseAmount",
        "InputVAT"
    ]

    purchases_table = purchases_table[
        purchases_columns
    ].copy()

    # 3. Prepare the product lookup table
    product_columns = [
        "ProductKey",
        "EnglishProductName"
    ]

    product_lookup = product_df[
        product_columns
    ].copy()

    product_lookup = product_lookup.drop_duplicates(
        subset=["ProductKey"]
    )

    # 4. Enrich purchases with product information
    purchases_table = purchases_table.merge(
        product_lookup,
        on="ProductKey",
        how="left",
        validate="many_to_one"
    )

    # 5. Prepare the date lookup table
    date_columns = [
        "DateKey",
        "FullDateAlternateKey"
    ]

    date_lookup = date_df[
        date_columns
    ].copy()

    date_lookup = date_lookup.drop_duplicates(
        subset=["DateKey"]
    )

    # 6. Enrich purchases with date information
    purchases_table = purchases_table.merge(
        date_lookup,
        left_on="OrderDateKey",
        right_on="DateKey",
        how="left",
        validate="many_to_one"
    )

    # 7. Rename technical columns into business-friendly names
    purchases_table = purchases_table.rename(
        columns={
            "EnglishProductName": "ProductName",
            "FullDateAlternateKey": "PurchaseDate"
        }
    )

    # 8. Add business columns
    purchases_table["Department"] = "Purchasing"

    # 9. Organize the final table
    purchases_final_columns = [
        "PurchaseID",
        "PurchaseDate",
        "Department",
        "ProductKey",
        "ProductName",
        "PurchaseAmount",
        "InputVAT"
    ]

    purchases_table = purchases_table[
        purchases_final_columns
    ]

    # 10. Return the transformed DataFrame
    return purchases_table


# ---------- TAX ADJUSTMENTS ----------

def create_tax_adjustments(
    sales_table: pd.DataFrame,
    purchases_table: pd.DataFrame
) -> pd.DataFrame:

    # 1. Select the sales columns required for tax adjustments
    sales_adjustments = sales_table[
        [
            "InvoiceID",
            "OrderDate",
            "SalesAmount",
            "OutputVAT"
        ]
    ].copy()

    # 2. Select a reproducible sample of 20 sales transactions
    Sales_sample = sales_adjustments.sample(
        n=20,
        random_state=42
    )

    # 3. Rename sales reference and date columns
    Sales_sample = Sales_sample.rename(
        columns={
            "InvoiceID": "ReferenceID",
            "OrderDate": "AdjustmentDate"
        }
    )

    # 4. Calculate a simulated 5% reduction of the original sales amount
    Sales_sample["AdjustmentAmount"] = (
        Sales_sample["SalesAmount"] * -0.05
    )

    # 5. Calculate the related Output VAT adjustment
    Sales_sample["VATAdjustment"] = (
        Sales_sample["OutputVAT"] * -0.05
    )

    # 6. Add business information for sales adjustments
    Sales_sample["AdjustmentType"] = "Sales Correction"
    Sales_sample["Department"] = "Finance"
    Sales_sample["Reason"] = "5% simulated Sales correction"

    # 7. Generate unique adjustment IDs for sales adjustments
    Sales_sample["AdjustmentID"] = [
        f"ADJ{i:05d}"
        for i in range(
            1,
            len(Sales_sample) + 1
        )
    ]

    # 8. Select the purchase columns required for tax adjustments
    purchase_adjustments = purchases_table[
        [
            "PurchaseID",
            "PurchaseDate",
            "PurchaseAmount",
            "InputVAT"
        ]
    ].copy()

    # 9. Select a reproducible sample of 20 purchase transactions
    Purchase_sample = purchase_adjustments.sample(
        n=20,
        random_state=42
    )

    # 10. Rename purchase reference and date columns
    Purchase_sample = Purchase_sample.rename(
        columns={
            "PurchaseID": "ReferenceID",
            "PurchaseDate": "AdjustmentDate"
        }
    )

    # 11. Calculate a simulated 5% reduction of the original purchase amount
    Purchase_sample["AdjustmentAmount"] = (
        Purchase_sample["PurchaseAmount"] * -0.05
    )

    # 12. Calculate the related Input VAT adjustment
    Purchase_sample["VATAdjustment"] = (
        Purchase_sample["InputVAT"] * -0.05
    )

    # 13. Add business information for purchase adjustments
    Purchase_sample["AdjustmentType"] = "Purchase Correction"
    Purchase_sample["Department"] = "Finance"
    Purchase_sample["Reason"] = "'5%' simulated Purchase correction"

    # 14. Generate unique adjustment IDs for purchase adjustments
    Purchase_sample["AdjustmentID"] = [
        f"ADJ{i:05d}"
        for i in range(
            len(Sales_sample) + 1,
            len(Sales_sample) + len(Purchase_sample) + 1
        )
    ]
    
    # 15. Standardize sales amount and VAT column names
    Sales_sample = Sales_sample.rename(
        columns={
            "SalesAmount": "OriginalAmount",
            "OutputVAT": "OriginalVAT"
        }
    )

    # 16. Standardize purchase amount and VAT column names
    Purchase_sample = Purchase_sample.rename(
        columns={
            "PurchaseAmount": "OriginalAmount",
            "InputVAT": "OriginalVAT"
        }
    )
    
    
    final_adjustment_columns = [
        "AdjustmentID",
        "ReferenceID",
        "AdjustmentDate",
        "AdjustmentType",
        "Department",
        "OriginalAmount",
        "OriginalVAT",
        "AdjustmentAmount",
        "VATAdjustment",
        "Reason"
    ]

    Sales_sample = Sales_sample[final_adjustment_columns]
    Purchase_sample = Purchase_sample[final_adjustment_columns]

    # 17. Combine sales and purchase adjustments
    tax_adjustments_table = pd.concat(
        [
            Sales_sample,
            Purchase_sample
        ],
        ignore_index=True
    )

    return tax_adjustments_table


# --------------Tax table -----------
def create_tax_rules() -> pd.DataFrame:
    
    # 1. Define New Brunswick tax rules
    tax_rules_data = [
        # HST old historical standard rate
        {
            "TaxCode": "HST15_OLD",
            "TaxDescription": "NB Standard HST",
            "VATRate": 0.15,
            "Province": "NB",
            "EffectiveFrom": "1997-04-01",
            "EffectiveTo": "2006-06-30",
            "Recoverable": True
        },
        # HST historical standard rate
        {
            "TaxCode": "HST14",
            "TaxDescription": "NB Standard HST",
            "VATRate": 0.14,
            "Province": "NB",
            "EffectiveFrom": "2006-07-01",
            "EffectiveTo": "2007-12-31",
            "Recoverable": True
        },  
        # HST historical standard rate
        {
            "TaxCode": "HST13",
            "TaxDescription": "NB Standard HST",
            "VATRate": 0.13,
            "Province": "NB",
            "EffectiveFrom": "2008-01-01",
            "EffectiveTo": "2016-06-30",
            "Recoverable": True
        },
        
        # HST current standard rate
        {
            "TaxCode": "HST15",
            "TaxDescription": "NB Standard HST",
            "VATRate": 0.15,
            "Province": "NB",
            "EffectiveFrom": "2016-07-01",
            "EffectiveTo": None,
            "Recoverable": True
        },
        # Zero-rated supply
        {
            "TaxCode": "ZERO",
            "TaxDescription": "NB Zero-rated Supply",
            "VATRate": 0.00,
            "Province": "NB",
            "EffectiveFrom": None,
            "EffectiveTo": None,
            "Recoverable": True
        },
        # Exempt supply
        {
            "TaxCode": "EXEMPT",
            "TaxDescription": "NB EXEMPT Supply",
            "VATRate": 0.00,
            "Province": "NB",
            "EffectiveFrom": None,
            "EffectiveTo": None,
            "Recoverable": False
        },
    ]
    tax_rules_table = pd.DataFrame(tax_rules_data)
    
    tax_rules_table["EffectiveFrom"] = pd.to_datetime(
        tax_rules_table["EffectiveFrom"]
    )
    tax_rules_table["EffectiveTo"] = pd.to_datetime(
        tax_rules_table["EffectiveTo"]
    )
    return tax_rules_table

# --------------- VAT returns ---------------

def get_tax_rule(
    transaction_date: str,
    tax_code:str,
    province:str,
    tax_rules_table:pd.DataFrame
) -> tuple[float,bool]:

    transaction_date = pd.to_datetime(transaction_date)
    
    if province not in tax_rules_table["Province"].values:
        raise ValueError("No applicable province data")

    province_rules = tax_rules_table[
        tax_rules_table["Province"] == province
    ].copy()
    

    if tax_code in ["ZERO", "EXEMPT"]:

        rule = province_rules[
            province_rules["TaxCode"] == tax_code
        ]
    

    elif tax_code == "STANDARD":

        rule = province_rules[
            (province_rules["EffectiveFrom"] <= transaction_date)
            &
            (
                (province_rules["EffectiveTo"] >= transaction_date)
                |
                province_rules["EffectiveTo"].isna()
            )
        ]
    else:
        raise ValueError("Invalid tax code")
    
    if rule.empty:
        raise ValueError("No applicable tax rule found")
    elif  rule.shape[0] > 1:
        raise ValueError("Multiple applicable tax rules found")

    return rule.iloc[0]["VATRate"], rule.iloc[0]["Recoverable"]

# ---------- EXPORT TABLES ----------

def save_sales_table(
    sales_table: pd.DataFrame
):
    sales_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/Sales.csv",
        index=False
    )

    print("Sales.csv exported successfully.")


def save_purchases_table(
    purchases_table: pd.DataFrame
):
    purchases_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/Purchases.csv",
        index=False
    )

    print("Purchases.csv exported successfully.")
    
def save_tax_adjustments_table(
    tax_adjustments_table: pd.DataFrame
):
    tax_adjustments_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/TaxAdjustments.csv",
        index=False
    )
    print("TaxAdjustment.csv exported successfully.")


# ---------- MAIN / TEST ----------

def main():

    # 1. Load source DataFrames
    print("#" * 50)
    print("Load source DataFrames")
    print("#" * 50)

    internet_sales_df = load_table("FactInternetSales")
    reseller_sales_df = load_table("FactResellerSales")
    product_df = load_table("DimProduct")
    customer_df = load_table("DimCustomer")
    reseller_df = load_table("DimReseller")
    
    #11. Export Purchases table
    print("\n" + "=" * 50)
    print("TAX RULES TEST")
    print("=" * 50)
    
    tax_rules_table = create_tax_rules()
    print(tax_rules_table)
    print("\nColumns:")
    print(tax_rules_table.columns.to_list())
    print("\nData types:")
    print(tax_rules_table.dtypes)
    print("\nTax codes:")
    
    
    print("\n" + "=" * 50)
    print("TAX RULES TEST")
    print("=" * 50)
    
    tax_rate, Recoverable = get_tax_rule(
        "2013-05-10",
        "STANDARD",
        "NB",
        tax_rules_table
        )
    print(tax_rate,Recoverable)

    # 2. Transform Internet Sales
    print("\n" + "=" * 50)
    print("Internet sales transformation")
    print("=" * 50)

    internet_sales = transform_internet_sales(
        internet_sales_df,
        product_df,
        customer_df,
        tax_rules_table
    )

    # ---------- INTERNET SALES TESTS ----------

    print("Raw shape:", internet_sales_df.shape)
    print("Transformed shape:", internet_sales.shape)

    print("\nColumns:")
    print(internet_sales.columns.tolist())

    print("\nFirst rows:")
    print(internet_sales.head())

    print("\nData types:")
    print(internet_sales.dtypes)

    print(
        "\nMissing product names:",
        internet_sales["ProductName"].isna().sum()
    )

    print(
        "Missing buyer names:",
        internet_sales["BuyerName"].isna().sum()
    )

    internet_duplicates = internet_sales.duplicated(
        subset=[
            "InvoiceID",
            "InvoiceLineNumber"
        ]
    ).sum()

    print(
        "Duplicate Internet invoice lines:",
        internet_duplicates
    )

    print("\nDepartment distribution:")
    print(
        internet_sales["Department"].value_counts()
    )

    # 3. Transform Reseller Sales
    print("\n" + "=" * 50)
    print("Reseller sales transformation")
    print("=" * 50)

    reseller_sales = transform_reseller_sales(
        reseller_sales_df,
        product_df,
        reseller_df,
        tax_rules_table
    )
    

    # ---------- RESELLER SALES TESTS ----------

    print("Raw shape:", reseller_sales_df.shape)
    print("Transformed shape:", reseller_sales.shape)

    print("\nColumns:")
    print(reseller_sales.columns.tolist())

    print("\nFirst rows:")
    print(reseller_sales.head())

    print("\nData types:")
    print(reseller_sales.dtypes)

    print(
        "\nMissing buyer names:",
        reseller_sales["BuyerName"].isna().sum()
    )

    print(
        "Missing product names:",
        reseller_sales["ProductName"].isna().sum()
    )

    print("\nDepartment distribution:")
    print(
        reseller_sales["Department"].value_counts()
    )

    # 4. Build consolidated Sales table
    print("\n" + "=" * 50)
    print("Sales table consolidation")
    print("=" * 50)

    sales_table = build_sales_tables(
        internet_sales,
        reseller_sales
    )

    # ---------- CONSOLIDATED SALES TESTS ----------

    print("Final Sales shape:", sales_table.shape)

    print("\nDepartment distribution:")
    print(
        sales_table["Department"].value_counts()
    )

    print("\nFinal columns:")
    print(sales_table.columns.tolist())

    print(
        "\nMissing buyer names:",
        sales_table["BuyerName"].isna().sum()
    )

    print(
        "Missing product names:",
        sales_table["ProductName"].isna().sum()
    )

    duplicate_count = sales_table.duplicated(
        subset=[
            "Department",
            "InvoiceID",
            "InvoiceLineNumber"
        ]
    ).sum()

    print(
        "Duplicate invoice lines:",
        duplicate_count
    )

    # 5. Export Sales table
    print("\n" + "=" * 50)
    print("Export Sales table")
    print("=" * 50)

    save_sales_table(
        sales_table
    )

    # 6. Load Purchases source tables
    print("\n" + "=" * 50)
    print("Purchases transformation")
    print("=" * 50)

    purchases_df = load_table("Purchases")
    date_df = load_table("DimDate")

    # 7. Transform Purchases
    purchases_table = transform_purchases(
        purchases_df,
        product_df,
        date_df
    )

    # ---------- PURCHASES TESTS ----------

    print("Raw shape:", purchases_df.shape)
    print("Transformed shape:", purchases_table.shape)

    print("\nColumns:")
    print(purchases_table.columns.tolist())

    print("\nFirst rows:")
    print(purchases_table.head())

    print("\nData types:")
    print(purchases_table.dtypes)

    print(
        "Missing product names:",
        purchases_table["ProductName"].isna().sum()
    )

    print(
        "Missing purchase dates:",
        purchases_table["PurchaseDate"].isna().sum()
    )

    duplicate_lines = purchases_table.duplicated(
        subset=[
            "PurchaseID",
            "ProductKey"
        ]
    ).sum()

    print(
        "Duplicate purchase lines:",
        duplicate_lines
    )

    print(
        "Negative purchase amounts:",
        (
            purchases_table["PurchaseAmount"] < 0
        ).sum()
    )

    print(
        "Zero purchase amounts:",
        (
            purchases_table["PurchaseAmount"] == 0
        ).sum()
    )

    print(
        "Negative Input VAT:",
        (
            purchases_table["InputVAT"] < 0
        ).sum()
    )

    vat_rate = (
        purchases_table["InputVAT"]
        / purchases_table["PurchaseAmount"]
    )

    print("\nVAT rate statistics:")
    print(vat_rate.describe())

    duplicated_purchase_ids = purchases_table[
        purchases_table.duplicated(
            subset=["PurchaseID"],
            keep=False
        )
    ].sort_values("PurchaseID")

    print(
        duplicated_purchase_ids.head(20)
    )

    print(
        "Unique PurchaseID:",
        purchases_table["PurchaseID"].nunique()
    )

    print(
        "Total rows:",
        len(purchases_table)
    )

    # 8. Export Purchases table
    print("\n" + "=" * 50)
    print("Export Purchases table")
    print("=" * 50)

    save_purchases_table(
        purchases_table
    )
    #-----------------test taxAdjusment -------------
    
    # 9. Create Tax Adjustments
    print("\n" + "=" * 50)
    print("Tax Adjustments")
    print("=" * 50)

    tax_adjustments_table = create_tax_adjustments(
        sales_table,
        purchases_table
    )
    print(tax_adjustments_table.head())

    print(
        tax_adjustments_table.columns.tolist()
    )

    print(
        "Tax Adjustments shape:",
        tax_adjustments_table.shape
    )

    print(
        tax_adjustments_table[
            "AdjustmentType"
        ].value_counts()
    )

    print(
        "Duplicate AdjustmentID:",
        tax_adjustments_table[
            "AdjustmentID"
        ].duplicated().sum()
    )
    # 10. Export Purchases table
    print("\n" + "=" * 50)
    print("Export TaxAdjustment table")
    print("=" * 50)
    
    save_tax_adjustments_table(
        tax_adjustments_table
    )
    #11. Export Purchases table
    print("\n" + "=" * 50)
    print("TAX RULES TEST")
    print("=" * 50)
    
    tax_rules_table = create_tax_rules()
    print(tax_rules_table)
    print("\nColumns:")
    print(tax_rules_table.columns.to_list())
    print("\nData types:")
    print(tax_rules_table.dtypes)
    print("\nTax codes:")
    
    
    print("\n" + "=" * 50)
    print("TAX RULES TEST")
    print("=" * 50)
    
    tax_rate, Recoverable = get_tax_rule(
        "2013-05-10",
        "STANDARD",
        "NB",
        tax_rules_table
        )
    print(tax_rate,Recoverable)



if __name__ == "__main__":
    main()