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
    - PurchaseQualityKPIs.csv
    - PurchaseValidationReport.csv
"""

import pandas as pd
import numpy as np
from load_data import load_table


# =================================================================
# 01 — TAX RULES
# =================================================================

def create_tax_rules() -> pd.DataFrame:
    """Build the project's simulated New Brunswick HST lookup table.

    Rates, dates, and recoverability assumptions must be verified against
    authoritative tax rules before any real-world fiscal use.
    """

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
        # HST First historical standard rate
        {
            "TaxCode": "HST14",
            "TaxDescription": "NB Standard HST",
            "VATRate": 0.14,
            "Province": "NB",
            "EffectiveFrom": "2006-07-01",
            "EffectiveTo": "2007-12-31",
            "Recoverable": True
        },  
        # HST Second historical standard rate
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


def get_tax_rule(
    transaction_date: str,
    tax_code: str,
    province: str,
    tax_rules_table: pd.DataFrame
) -> tuple[float, bool]:
    """Return the single matching VAT rate and recoverability flag.

    STANDARD uses effective dates; ZERO and EXEMPT use their fixed entries.
    Raises ValueError when no unique applicable rule can be found.
    """

    transaction_date = pd.to_datetime(transaction_date)
    if pd.isna(transaction_date):
        raise ValueError("Missing or invalid transaction date")

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
            (province_rules["TaxCode"].str.startswith("HST"))
            & (province_rules["EffectiveFrom"] <= transaction_date)
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



# =================================================================
# 02 — INTERNET AND RESELLER SALES
# =================================================================

def transform_internet_sales(
    internet_sales_df: pd.DataFrame,
    product_df: pd.DataFrame,
    customer_df: pd.DataFrame,
    tax_rules_table: pd.DataFrame
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
            "TaxAmt": "OriginalOutputVAT",
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
    ).round(2)

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
        "OriginalOutputVAT",
        "OutputVAT",
        "Province",
        "TaxCode"
    ]

    sales_df = sales_df[final_columns]

    # 12. Return the transformed DataFrame
    return sales_df


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
            "TaxAmt": "OriginalOutputVAT",
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
    ).round(2)
    
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
        "OriginalOutputVAT",
        "OutputVAT",
        "Province",
        "TaxCode"
    ]
    
    sales_df = sales_df[final_columns]
    
    # 12. Return the transformed DataFrame
    return sales_df


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



# =================================================================
# 03 — PURCHASES AND VALIDATION
# =================================================================

def transform_purchases(
    purchases_df: pd.DataFrame,
    product_df: pd.DataFrame,
    date_df: pd.DataFrame,
    tax_rules_table: pd.DataFrame
) -> pd.DataFrame:
    """Create a simulated purchases table enriched with tax information.

    OriginalInputVAT preserves the source value; InputVAT is recalculated
    under the project's simplified recoverability assumptions.
    """

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

    # 8. Add business and tax-related columns (simulation assumptions)
    purchases_table["Department"] = "Purchasing"
    purchases_table["Province"] = "NB"
    purchases_table["TaxCode"] = "STANDARD"

    # Preserve source VAT for subsequent data-quality reconciliation
    purchases_table = purchases_table.rename(
        columns={"InputVAT": "OriginalInputVAT"}
    )

    # 9. Determine tax rate and recoverability for each purchase
    tax_results = purchases_table.apply(
        lambda row: get_tax_rule(
            row["PurchaseDate"],
            row["TaxCode"],
            row["Province"],
            tax_rules_table
        ),
        axis=1
    )
    purchases_table[["TaxRate", "Recoverable"]] = pd.DataFrame(
        tax_results.tolist(),
        index=purchases_table.index,
        columns=["TaxRate", "Recoverable"]
    )

    # 10. Tax charged on purchases, before recoverability rules
    purchases_table["TaxPaid"] = (
        purchases_table["PurchaseAmount"] * purchases_table["TaxRate"]
    ).round(2)

    # 11. Eligible input tax credit (simplified simulation)
    purchases_table["InputVAT"] = (
        purchases_table["TaxPaid"]
        * purchases_table["Recoverable"].astype(int)
    ).round(2)

    # 12. Organize the final table
    purchases_final_columns = [
        "PurchaseID", "PurchaseDate", "Department", "ProductKey",
        "ProductName", "PurchaseAmount", "Province", "TaxCode",
        "TaxRate", "Recoverable", "OriginalInputVAT", "TaxPaid", "InputVAT"
    ]
    purchases_table = purchases_table[purchases_final_columns]

    # 13. Return the transformed DataFrame
    return purchases_table


def validate_purchases(
    purchases_table: pd.DataFrame
) -> pd.DataFrame:
    """Audit TaxPaid and InputVAT without mutating the input table.

    Independent checks return PASS, FAIL, or MISSING. The overall status
    prioritizes INVALID over INCOMPLETE over VALID.
    """

    purchases = purchases_table.copy()

    # 1. Allow missing values in Recoverable; create the boolean mask below
    purchases["Recoverable"] = (
        purchases["Recoverable"].astype(object)
    )

    # 2. Identify missing values in required columns
    tax_columns = [
        "PurchaseAmount",
        "TaxRate",
        "TaxPaid"
    ]

    input_columns = [
        "PurchaseAmount",
        "TaxRate",
        "Recoverable",
        "InputVAT"
    ]

    missing_mask = purchases[tax_columns].isna().any(axis=1)
    missing_mask2 = purchases[input_columns].isna().any(axis=1)

    # 3. Calculate expected tax paid
    purchases["ExpectedTaxPaid"] = (
        purchases["PurchaseAmount"] *
        purchases["TaxRate"]
    ).round(2)

    # 4. Calculate expected recoverable input tax
    # The Boolean mask uses False only for computation; unknown source
    # recoverability is still recorded as NaN in ExpectedInputVAT.
    recoverable_mask = (
        purchases["Recoverable"]
        .astype("boolean")
        .fillna(False)
        .astype(bool)
    )
    purchases["ExpectedInputVAT"] = np.where(
        purchases["Recoverable"].isna(),
        np.nan,
        np.where(
            recoverable_mask,
            purchases["ExpectedTaxPaid"],
            0.0
        )
    )

    # 5. Validate TaxPaid
    purchases["TaxPaidValidation"] = np.select(
        condlist=[
            missing_mask,
            (
                purchases["TaxPaid"] -
                purchases["ExpectedTaxPaid"]
            ).abs() < 0.000001
        ],
        choicelist=[
            "MISSING",
            "PASS"
        ],
        default="FAIL"
    )

    # 6. Validate InputVAT
    purchases["InputVATValidation"] = np.select(
        condlist=[
            missing_mask2,
            (
                purchases["InputVAT"] -
                purchases["ExpectedInputVAT"]
            ).abs() < 0.000001
        ],
        choicelist=[
            "MISSING",
            "PASS"
        ],
        default="FAIL"
    )

    # 7. Classify each purchase: FAIL takes priority over MISSING.
    validation_columns = [
        "TaxPaidValidation",
        "InputVATValidation"
    ]

    invalid_mask = purchases[validation_columns].eq("FAIL").any(axis=1)

    incomplete_mask = purchases[validation_columns].eq("MISSING").any(axis=1)

    # print("INVALID detected:", invalid_mask.sum())
    # print("INCOMPLETE detected:", incomplete_mask.sum())

    purchases["PurchaseValidationStatus"] = np.select(
        condlist=[
            invalid_mask,
            incomplete_mask
        ],
        choicelist=[
            "INVALID",
            "INCOMPLETE"
        ],
        default="VALID"
    )
    return purchases

def generate_purchase_validation_report(
    purchases: pd.DataFrame
) -> pd.DataFrame:
    """Return only INVALID and INCOMPLETE purchases for review.

    Preserves the original validated table and reports key amounts,
    expected amounts, and their corresponding validation statuses.
    """
    final_column = [
        "PurchaseID",
        "PurchaseDate",
        "PurchaseAmount",
        "TaxPaid",
        "ExpectedTaxPaid",
        "InputVAT",
        "ExpectedInputVAT",
        "TaxPaidValidation",
        "InputVATValidation",
        "PurchaseValidationStatus",
    ]

    filter_mask = purchases["PurchaseValidationStatus"].isin(
        ["INVALID", "INCOMPLETE"]
    )

    validation_file = purchases.loc[filter_mask, final_column].copy()
    
    validation_file = validation_file.sort_values(
        by="PurchaseValidationStatus"
    )
    return validation_file


def calculate_purchase_quality_kpis(
    validation_file: pd.DataFrame
) -> dict:
    """Summarize purchase-validation statuses across the full validated table.

    Rates use all transactions as denominator and are rounded to 2 decimals.
    Empty inputs return None for rates (undefined denominator).
    """

    Kpis_calculation = validation_file.copy()

    # 1. Count total transactions
    TotalTransactions = len(Kpis_calculation)

    # 2. Count VALID, INVALID and INCOMPLETE
    status_counts = Kpis_calculation[
        "PurchaseValidationStatus"
    ].value_counts()

    invalid_count = status_counts.get("INVALID", 0)
    valid_count = status_counts.get("VALID", 0)
    incomplete_count = status_counts.get("INCOMPLETE", 0)

    # 3. Handle an empty DataFrame
    if TotalTransactions == 0:
        invalid_percentage = None
        valid_percentage = None
        incomplete_percentage = None

    # 4. Calculate three percentages
    else:
        invalid_percentage = round(
            (invalid_count / TotalTransactions) * 100, 2
        )

        valid_percentage = round(
            (valid_count / TotalTransactions) * 100, 2
        )

        incomplete_percentage = round(
            (incomplete_count / TotalTransactions) * 100, 2
        )

    # 5. Return the KPI dictionary
    kpis = {
        "TotalTransactions": TotalTransactions,
        "ComplianceRate": valid_percentage,
        "InvalidRate": invalid_percentage,
        "IncompleteRate": incomplete_percentage
    }

    return kpis
# =================================================================
# 04 — TAX ADJUSTMENTS
# =================================================================

def create_tax_adjustments(
    sales_table: pd.DataFrame,
    purchases_table: pd.DataFrame
) -> pd.DataFrame:
    """Generate 40 reproducible, simulated sales/purchase adjustments.

    The 5% reductions are test data, not real correction documents.
    """

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
    Purchase_sample["Reason"] = "5% simulated Purchase correction"

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

# =================================================================
# 05 — VAT/HST RETURN GENERATION
# =================================================================

def calculate_net_hst(
    sales_table: pd.DataFrame,
    purchases_table: pd.DataFrame,
    tax_adjustments_table: pd.DataFrame
) -> dict:
    
    TotalOutputVAT = sales_table["OutputVAT"].sum()
    TotalInputVAT = purchases_table["InputVAT"].sum()
    
    SalesVATAdjustments = tax_adjustments_table.loc[
        tax_adjustments_table["AdjustmentType"] == "Sales Correction",
        "VATAdjustment"
    ].sum()

    PurchaseVATAdjustments = tax_adjustments_table.loc[
        tax_adjustments_table["AdjustmentType"] == "Purchase Correction",
        "VATAdjustment"
    ].sum()
    
    NetHST = (
        (TotalOutputVAT + SalesVATAdjustments)
        - (TotalInputVAT + PurchaseVATAdjustments)
    )
    
    return {
        "TotalOutputVAT": TotalOutputVAT,
        "TotalInputVAT": TotalInputVAT,
        "SalesVATAdjustments": SalesVATAdjustments,
        "PurchaseVATAdjustments": PurchaseVATAdjustments,
        "NetHST": round(NetHST, 2)
    }

# =================================================================
# 05 — CSV EXPORTS
# =================================================================

def save_sales_table(
    sales_table: pd.DataFrame
):
    """Export the Sales table to the project clean_dataset directory."""
    sales_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/Sales.csv",
        index=False
    )

    print("Sales.csv exported successfully.")


def save_purchases_table(
    purchases_table: pd.DataFrame
):
    """Export the Purchases table to the project clean_dataset directory."""
    purchases_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/Purchases.csv",
        index=False
    )

    print("Purchases.csv exported successfully.")


def save_tax_adjustments_table(
    tax_adjustments_table: pd.DataFrame
):
    """Export the TaxAdjustments table to the project clean_dataset directory."""
    tax_adjustments_table.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/TaxAdjustments.csv",
        index=False
    )
    print("TaxAdjustments.csv exported successfully.")
    
def save_purchase_quality_report(
    validation_file: pd.DataFrame
):
    """Export KPI summary and anomaly details from the full validated table."""

    # 1. Calculate KPIs using the existing function
    kpis = calculate_purchase_quality_kpis(validation_file)

    # 2. Convert the KPI dictionary into a DataFrame
    kpis_df = pd.DataFrame([kpis])

    # 3. Export the one-row KPI summary to CSV
    kpis_df.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/PurchaseQualityKPIs.csv",
        index=False
    )
    # 4. Export only INVALID and INCOMPLETE purchase transactions
    anomaly_file =  generate_purchase_validation_report(validation_file)
    anomaly_file.to_csv(
        "C:/Users/Cetaking/Desktop/formation/"
        "Projet_tax_Autamation/clean_dataset/PurchaseValidationReport.csv",
        index=False
    )

    # 5. Print an export confirmation
    print("PurchaseQualityKPIs.csv exported successfully.")
    print("PurchaseValidationReport.csv exported successfully.")


# =================================================================
# 06 — MAIN PIPELINE AND ALL TESTS
# =================================================================

def main():
    """Run transformations, inspections, anomaly tests, and CSV exports.

    All existing inline tests are intentionally retained to keep the
    project's development and validation history visible.
    """

    # 1. Load source DataFrames
    print("#" * 50)
    print("Load source DataFrames")
    print("#" * 50)

    internet_sales_df = load_table("FactInternetSales")
    reseller_sales_df = load_table("FactResellerSales")
    product_df = load_table("DimProduct")
    customer_df = load_table("DimCustomer")
    reseller_df = load_table("DimReseller")
    
    # 2. Tax rules: table inspection and lookup test
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
    
    tax_rate, recoverable = get_tax_rule(
        "2013-05-10",
        "STANDARD",
        "NB",
        tax_rules_table
        )
    print(tax_rate, recoverable)

    # 3. Transform Internet Sales
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

    # 4. Transform Reseller Sales
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

    # 5. Build consolidated Sales table
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

    # 6. Export Sales table
    print("\n" + "=" * 50)
    print("Export Sales table")
    print("=" * 50)

    save_sales_table(
        sales_table
    )

    # 7. Sales VAT calculation tests 
    # Validate Output VAT calculations
    expected_output_vat = (
        sales_table["SalesAmount"]
        * sales_table["TaxRate"]
    ).round(2)

    output_vat_errors = (
        sales_table["OutputVAT"]
        .sub(expected_output_vat)
        .abs()
        .gt(0.001)
    )

    print("\nSALES OUTPUT VAT VALIDATION")
    print("Total sales records:", len(sales_table))
    print("Incorrect Output VAT calculations:", output_vat_errors.sum())

    print("\nTax rates distribution:")
    print(sales_table["TaxRate"].value_counts())
    
        # Investigate Output VAT differences
    sales_check = sales_table.copy()

    sales_check["ExpectedVAT_Raw"] = (
        sales_check["SalesAmount"]
        * sales_check["TaxRate"]
    )

    sales_check["ExpectedVAT_Rounded"] = (
        sales_check["ExpectedVAT_Raw"].round(2)
    )

    sales_check["Difference_Raw"] = (
        sales_check["OutputVAT"]
        - sales_check["ExpectedVAT_Raw"]
    )

    sales_check["Difference_Rounded"] = (
        sales_check["OutputVAT"]
        - sales_check["ExpectedVAT_Rounded"]
    )

    print("\nOUTPUT VAT DIFFERENCE ANALYSIS")

    print(
        sales_check[
            [
                "InvoiceID",
                "SalesAmount",
                "TaxRate",
                "OutputVAT",
                "ExpectedVAT_Raw",
                "ExpectedVAT_Rounded",
                "Difference_Raw",
                "Difference_Rounded"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nMaximum absolute raw difference:")
    print(sales_check["Difference_Raw"].abs().max())

    print("\nMaximum absolute rounded difference:")
    print(sales_check["Difference_Rounded"].abs().max())

    print("\nErrors without rounding:")
    print(
        (sales_check["Difference_Raw"].abs() > 0.000001).sum()
    )
    
    print("\nSALES DATE RANGE")
    print("Earliest:", sales_table["OrderDate"].min())
    print("Latest:", sales_table["OrderDate"].max())

    print("\n" + "=" * 50)


    # 8. Load Purchases source tables
    print("\n" + "=" * 50)
    print("Purchases transformation")
    print("=" * 50)

    purchases_df = load_table("Purchases")
    date_df = load_table("DimDate")

    # 9. Transform Purchases
    purchases_table = transform_purchases(
        purchases_df,
        product_df,
        date_df,
        tax_rules_table
    )
    
    # 10. Purchases tests 

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

    # 11. Export Purchases table
    print("\n" + "=" * 50)
    print("Export Purchases table")
    print("=" * 50)

    save_purchases_table(
        purchases_table
    )
    print("\nPURCHASE TAX VALIDATION")

    print(
        purchases_table[
            [
                "PurchaseID",
                "PurchaseDate",
                "PurchaseAmount",
                "TaxRate",
                "Recoverable",
                "TaxPaid",
                "InputVAT"
            ]
        ].head(10)
    )
    # Validate calculated purchase tax
    expected_tax = (
        purchases_table["PurchaseAmount"]
        * purchases_table["TaxRate"]
    ).round(2)

    tax_errors = (
        purchases_table["TaxPaid"]
        .sub(expected_tax)
        .abs()
        .gt(0.001)
    )

    print("\nPURCHASE TAX CALCULATION CHECK")
    print("Incorrect tax calculations:", tax_errors.sum())
    
    # Validate recoverable input tax
    expected_input_vat = (
        purchases_table["TaxPaid"]
        * purchases_table["Recoverable"].astype(int)
    ).round(2)

    input_vat_errors = (
        purchases_table["InputVAT"]
        .sub(expected_input_vat)
        .abs()
        .gt(0.001)
    )

    print("\nINPUT VAT RECOVERABILITY CHECK")
    print("Incorrect Input VAT calculations:", input_vat_errors.sum())
    print(
        "Non-recoverable purchases:",
        (~purchases_table["Recoverable"]).sum()
    )
    
    # Temporary non-recoverable VAT test 
    # Test a non-recoverable purchase
    test_purchase = purchases_table.iloc[0].copy()

    test_purchase["Recoverable"] = False

    test_input_vat = (
        test_purchase["TaxPaid"]
        * int(test_purchase["Recoverable"])
    )

    print("\nNON-RECOVERABLE PURCHASE TEST")
    print("Purchase ID:", test_purchase["PurchaseID"])
    print("Tax Paid:", test_purchase["TaxPaid"])
    print("Recoverable:", test_purchase["Recoverable"])
    print("Expected Input VAT:", test_input_vat)
    
    # 12. Purchase validation function tests
    print("\n" + "=" * 50)
    print("Validate function")
    print("=" * 50)
    
    validate_purch_table = validate_purchases(
        purchases_table
        )
    print("Validate table shape",validate_purch_table.shape)
    print(
        "Validated columns", validate_purch_table.columns.to_list()
    )
    
  
    # ---------- INDIVIDUAL PURCHASE VALIDATION TESTS ----------
    # Each case modifies an independent copy; source purchases stay unchanged.
    print("###" * 30)
    print("TaxPaid incorrect value")
    adding_incorrect_val = purchases_table.copy()
    row_index1 = adding_incorrect_val.index[0]
    
    adding_incorrect_val.loc[row_index1, "TaxPaid"] = (
        adding_incorrect_val.loc[row_index1, "TaxPaid"] + 10
    )
    adding_incorrect_val = validate_purchases(adding_incorrect_val)
    print(adding_incorrect_val.loc[[row_index1]])
    print("\nTaxPaid Validation:")
    print(
        adding_incorrect_val["TaxPaidValidation"].value_counts()
    )
    print("\nInputVAT Validation:")
    print(
        adding_incorrect_val["InputVATValidation"].value_counts()
    )
    
        
    print("###" * 30)
    print("InputVAT Missing Value Testing")
  

    missing_inputvat_test = purchases_table.copy()
    row_index = missing_inputvat_test.index[3]
    missing_inputvat_test["Recoverable"] = (
        missing_inputvat_test["Recoverable"].astype("boolean")
    )
    missing_inputvat_test.loc[row_index, "Recoverable"] = pd.NA
    missing_inputvat_result = validate_purchases(missing_inputvat_test)
    print(missing_inputvat_result.loc[[row_index]])
    print("\nTaxPaid Validation:")
    print(
        missing_inputvat_result["TaxPaidValidation"].value_counts()
    )
    print("\nInputVAT Validation:")
    print(
        missing_inputvat_result["InputVATValidation"].value_counts()
    )

    print("###" * 30)
    print("###"*30)
   

    print("Input Val testing")
    inputVAT_validation = purchases_table.copy()
    row_index2 = inputVAT_validation.index[4]
    inputVAT_validation.loc[row_index2, "InputVAT"] += 20
    
    input_purchase_val = validate_purchases(inputVAT_validation)
    print(input_purchase_val.loc[[row_index2]])
    print(input_purchase_val["TaxPaidValidation"].value_counts())
    print(input_purchase_val["InputVATValidation"].value_counts())
    print("###"*30)
    print("###"*30)
    
    # ---------- PHASE 4.4: COMBINED PURCHASE VALIDATION TEST ----------
    # Inject three different anomalies into a single test DataFrame.

    print("###" * 30)
    print("Combined Purchase Validation Testing")

    # 1. Create a copy of the original purchases table
    combined_purchase_test = purchases_table.copy()

    # 2. Convert Recoverable to nullable boolean
    combined_purchase_test["Recoverable"] = (
        combined_purchase_test["Recoverable"].astype("boolean")
    )

    # 3. Introduce incorrect TaxPaid on the third row
    row_ind = combined_purchase_test.index[2]
    combined_purchase_test.loc[row_ind, "TaxPaid"] += 10

    # 4. Introduce missing Recoverable on the fourth row
    four_row = combined_purchase_test.index[3]
    combined_purchase_test.loc[four_row, "Recoverable"] = pd.NA

    # 5. Introduce incorrect InputVAT on the fifth row
    fifth_ind = combined_purchase_test.index[4]
    combined_purchase_test.loc[fifth_ind, "InputVAT"] += 20

    # 6. Validate all transactions for the combined test
    result = validate_purchases(combined_purchase_test)

    # 7. Display the three modified transactions
    print("\nModified Transactions:")
    print(
        result.loc[
            [row_ind, four_row, fifth_ind],
            [
                "PurchaseID",
                "TaxPaid",
                "ExpectedTaxPaid",
                "Recoverable",
                "InputVAT",
                "ExpectedInputVAT",
                "TaxPaidValidation",
                "InputVATValidation"
            ]
        ]
    )

    # 8. Display TaxPaid validation counts
    print("\nTaxPaid Validation:")
    print(
        result["TaxPaidValidation"].value_counts()
    )

    # 9. Display InputVAT validation counts
    print("\nInputVAT Validation:")
    print(
        result["InputVATValidation"].value_counts()
    )
    # Additional status-count check (retained as an existing test).
    # The next two calls repeat the same validation; consider reusing
    # `result` when optimizing performance, after baseline verification.
    new_status = validate_purchases(combined_purchase_test)
    print(new_status["PurchaseValidationStatus"].value_counts())
    
    validated_combined = validate_purchases(combined_purchase_test)

    purchase_report = generate_purchase_validation_report(
        validated_combined
    )

    print("\nPurchase Validation Report:")
    print(purchase_report)

    print("Total anomalies:", len(purchase_report))
    
    # ---------- PHASE 4.7: PURCHASE QUALITY KPI TEST ----------

    print("\n" + "=" * 50)
    print("PURCHASE QUALITY KPI REPORT")
    print("=" * 50)

    purchase_kpis = calculate_purchase_quality_kpis(result)

    for kpi, value in purchase_kpis.items():
        print(f"{kpi}: {value}")
        
    # ---------- PURCHASE QUALITY KPI EXPORT ----------
    save_purchase_quality_report(validate_purch_table)
    
    # ---------- TAX ADJUSTMENTS TESTS  ----------

    # 13. Create Tax Adjustments
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
    # 14. Export tax adjustments
    print("\n" + "=" * 50)
    print("Export TaxAdjustment table")
    print("=" * 50)
    
    save_tax_adjustments_table(
        tax_adjustments_table
        )
    
    # ---------- PHASE 5.1: NET HST CALCULATION TEST ----------

    print("\n" + "=" * 50)
    print("NET HST CALCULATION")
    print("=" * 50)
    
    net_hst_result = calculate_net_hst(
        sales_table,
        purchases_table,
        tax_adjustments_table
    )
    
    for indicator, value in net_hst_result.items():
        print(f"{indicator}: {value}")

if __name__ == "__main__":
    main()
