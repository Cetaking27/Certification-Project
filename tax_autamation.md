### Phase 1: Problem Statement

Design and develop an end-to-end tax data automation solution that ingests monthly tax files from multiple business units, validates and transforms data, loads it into a centralized database, and generates interactive Power BI dashboards. Implement automated workflow orchestration, logging, error reporting, and monitoring to reduce manual processing and improve data quality.
### Project Roadmap 
A realistic learning roadmap (8–10 weeks)
Week 1: Design the business scenario, create sample tax datasets, and set up the project structure.
Weeks 2–3: Build the ingestion and validation pipelines in Python using pandas.
Week 4: Implement transformation logic and load the cleaned data into PostgreSQL.
Week 5: Develop SQL queries and create a normalized reporting schema.
Week 6: Build Power BI dashboards for tax reporting and pipeline monitoring.
Week 7: Add logging, error handling, and automated email or Teams notifications.
Week 8: Connect to a free-tier Snowflake account and migrate the pipeline.
Weeks 9–10 (optional): Explore Dataiku, integrate with SharePoint and Microsoft Power Automate, and experiment with Microsoft Copilot for natural-language queries.

### Phase 2: Data understanding and ghathering 
#### - Business simulation: 
    - Global Tech Ltd (Firm name)
    -- Department :
        -- Canada
        -- France
        -- USA
        -- Germany
        -- UK
    -- Data uploaded from each  Department
        - Sales
        - Purchases
        - tax adjustements
        - VAT returns
    -- Data Folders map:
        Raw_Data/

            - Canada/
                January.xlsx
                February.xlsx
                Mars.xlsx
                April.xlsx
                Mai.xlsx
                june.xlsx

            - USA/
                January.xlsx
                February.xlsx
                Mars.xlsx
                April.xlsx
                Mai.xlsx
                june.xlsx
            - Germany/ 
            - France/
            - UK/

### Phase 3 : Data ingestion model

-- Data ingestion: is a process of importing, loading or transforming data collected from different external sources that can be store in a system or storage infrastructure to be process, and analyz.</br>
-- Data ingestion can help business and compagnies in effectevly gaining insights, drive innovations, make data driven decision...so important for better quality data, automation.</br>

-- Differents type of data ingestion: 

            -- *Real-time Data ingestion* : process of collecting and sending data from souces in real time solution like **Change Data Capture (CDC)**;

            -- *Batch-based data ingestion*: process of gathering and sending data in batches at regular intervals.

            -- *Micro batching*: process that falls between real-time and batch-based approaches.

-- **Step of Data ingestion:**

    1- *Collecting from wide sources:* databases, files, APIs, streaming services, lot Devices.
    2- *Data transformation*: process of cleaning, Data normalization and data enrichment.
    3- *Data loading*: loading in data warehouses, data lakes depending to the organizations.

**Final note** : Data ingestion workflow then lookalike this: Data Source identification -> Data extraction -> data staging -> Data validation -> Data transformation -> Data loading -> Data monitoring.


    - Tools identification:
        Python( pandas, openpyxl)
    -Integration map:
        - Raw Data
            ↓
        - Python  
            ↓
        - Standard DataFrame
            ↓
        - Database

### Phase 3: Data Validation
Data validation involves checking that the data is clean, accurate and ready for use.
As part of this project, I carried out the following steps to check whether the data met the project’s requirements, as follows:
        - code checks : whether the valus is valid by comparing it to a list of acceptable values.
        - consistency checks: comfirm that input data is logical and does not conflict with other values.
        - Data type checks : dfines the valid format for data in a each column.
        - Format checks: for columns that have specific data formatting requirements such as phone number, email....
        - Range checks : determine wether numerical data falls within a predefined range of minimum and maximum values.
        - Uniqueness checks : Apply to columns where every data entry must be unique and there are no duplicate values.

- Validation Rules for the project:
    - Invoice number : default not empty
    - Tax amount : Not negative
    - Country Code : default not null
    - Currency : CAD
    - GST Rate: 0, 5, 13, 15
- Document preparation: Validation Report.xlsx 
#### phase 5: Data Transformation
convert messy data into a clean warehouse table.
-- Data transformation map overivews
    input::
        - Invoice
        - Inv#
        - Invoice Number
        - Invoice_ID
    output::
        - invoice_number
        - Standardize
        - currencies
        - Dates
        - Country names
        - Tax codes
        - customer IDs
### Phase 6: Database builds
    -(learn snowflake)
SQLite -> PostgreSQL -> Snowflake
    - Table overviews:
        - Invoices
        - Customers
        - Countries
        - TaxCodes
        - TaxReturns
        - AuditLogs
### Phase 7: Workflow automation
System structure:: instead of runny manually 
        - New file arrives
            ↓
        - Automatically start pipeline
            ↓
        - Validate
            ↓
        - Transform
            ↓      
        - Insert database
            ↓
        - Refresh Power BI
            ↓
        - Send Email
### Power BI 
    - Dasboards preparations
        - Countries
        - Tax by Country 
        - Validation Errors
        - invoices Processed
        - Pipeline Success
        - Duplicate invoices
        - Duplicate Pages

    - Pages summary of BI
        Executive Summary
                ↓
        Country Analysis
                ↓
        Validation Errors
                ↓
        Audit Report        
                ↓
        Automation Monitoring
### Phases 9 : Monitoring
    - Create : pipeline_log.csv
    - Columns:
        - Run data
        - file Processed
        - Rows loaded,
        - Errors
        - Durations and status
    - Dashboard : 
        - Pipeline Health
        - Success % 
        - Average Runtime
        - Failure Rate
### Phase 10: Notifications platforme   
    Send Email
        OR
    Send Teams Message
        OR
    Write Log
Example::
    5 invoices rejected
    Reason
    Missing GST
    Click here to review

### Phase 11: Documentation
create a documentatiom to the project
        SharePoint
            ↓
        Excel Upload    
            ↓
        Python
            ↓
        Validation
            ↓
        Transformation
            ↓
        Snowflake
            ↓
        Power BI
            ↓
        Power Automate

##### FInal sTAGE:
    TaxAutomationProject/

        data/

            raw/

            processed/

            archive/

        database/

        scripts/

            ingest.py

            validate.py

            transform.py

            load.py

        dashboards/

        logs/

        reports/

        documentation/

        tests/

tools to master :
Dataiku
sharePoint API
snowFlake
Python
PowerBI
SQL

database overview

                    📂 Tax Automation Project
                    │
                    ├── data/
                    │   ├── Sales.csv
                    │   ├── Purchases.csv
                    │   ├── TaxAdjustments.csv
                    │   └── VATReturns.csv
                    │
                    ├── load_data.py
                    ├── transform_data.py
                    ├── validate_data.py
                    ├── calculate_vat.py
                    ├── generate_vat_return.py
                    │
                    ├── config.py
                    ├── requirements.txt
                    │
                    ├── sql/
                    │   ├── create_tables.sql
                    │   ├── transformations.sql
                    │   └── validation.sql
                    │
                    └── powerbi/
                        └── VAT_Dashboard.pbix      



#### Full Projet Flow

                    AdventureWorksDW2025
                            │
                            ▼
                    load_data.py
                            │
                            ▼
                    Raw DataFrames
                            │
                            ▼
                    transform_data.py
                            │
                            ├── Sales.csv
                            ├── Purchases.csv
                            └── TaxAdjustments.csv
                            │
                            ▼
                    validate_data.py
                            │
                            ▼
                    calculate_vat.py
                            │
                            ▼
                    generate_vat_return.py
                            │
                            ▼
                    VATReturns.csv
                            │
                            ▼
                    Power BI