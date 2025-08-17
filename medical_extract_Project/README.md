# 🩺 Medical Data Extraction and Analysis Project

## 📌 Description

This project focuses on extracting meaningful medical information from unstructured clinical text data such as doctor's notes, prescriptions, and medical reports. Using Natural Language Processing (NLP) and machine learning techniques, we transform raw medical documents into structured, analyzable datasets to support healthcare insights and decision-making.

---

## 🎯 Objectives

- Extract clinical entities such as diagnoses, medications, and test results from raw text
- Structure the extracted data into a relational database format
- Perform exploratory data analysis on patient-level medical data
- Build visualizations to uncover health trends and patterns
- (Optional) Predict conditions or cluster patient profiles based on extracted data

---

## 🛠️ Technologies Used

| Category         | Tools/Technologies                                |
|------------------|---------------------------------------------------|
| Programming      | Python, Jupyter Notebook                          |
| NLP              | spaCy, NLTK, Scikit-learn, Hugging Face Transformers (BERT) |
| OCR (if needed)  | Tesseract OCR, pdfplumber                         |
| Data Handling    | pandas, NumPy                                     |
| Visualization    | matplotlib, seaborn, Plotly                       |
| Database         | SQLite / PostgreSQL                              |
| Annotation       | Doccano / Prodigy (manual labeling - optional)    |
| Deployment (opt) | Streamlit / Flask (for simple UI)                |

---

## 📂 Dataset

- Publicly available or synthetic medical records
- Sample files: `sample_note.txt`, `patient_data.pdf`, or MIMIC-III/i2b2 datasets
- ⚠️ All data used is either simulated or anonymized to ensure patient privacy

---

## 📊 Key Features

- 🧾 **Text Cleaning & Preprocessing:** Tokenization, lemmatization, stopword removal
- 🧠 **NER for Clinical Terms:** Detect diseases, drugs, tests using custom NER pipeline or BERT
- 🧱 **Data Structuring:** Store patient data in structured tabular format (CSV/SQL)
- 📈 **Exploratory Analysis:** Frequency of conditions, drug usage, and trends
- 📊 **Visualization:** Time-series charts, bar plots, and word clouds
- 🤖 **(Bonus)** Predictive models or clustering for patient profiling

---

## 📁 Project Structure

📦 medical-data-extraction
├── data/
│ └── raw/
│ └── processed/
├── notebooks/
│ └── 01_data_cleaning.ipynb
│ └── 02_ner_extraction.ipynb
│ └── 03_visualizations.ipynb
├── src/
│ └── ocr.py
│ └── ner.py
│ └── utils.py
├── results/
│ └── figures/
│ └── tables/
├── README.md
├── requirements.txt
└── main.py