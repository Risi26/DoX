# 🍇 DOX v2 — Data Exploration System

> Unlock the power of your dataset — like a Devil Fruit ⚡

---

## 🚀 Overview

**DOX v2** is an interactive data analysis web application built using **Streamlit** that allows users to upload datasets and instantly explore, analyze, and visualize them.

It is designed to:

* Reduce manual data inspection effort
* Provide quick statistical insights
* Detect patterns, outliers, and relationships

---

## 🎯 Key Features

### 📂 Multi-Format Support

* Upload **CSV, Excel, or JSON** files
* Automatic parsing and loading

---

### 📊 Dataset Overview

* Total rows and columns
* Numeric vs categorical breakdown
* Missing value count

---

### 🔍 Data Preview

* Displays first 10 rows
* Responsive full-width table

---

### 🗂️ Column Information

* Data types
* Missing values (count & %)
* Unique values

---

### 🚨 Missing Value Analysis

* Detects missing data
* Column-wise breakdown

---

### 📈 Statistical Summary

* Mean, Median, Std, Min, Max
* Automatically computed for numeric columns

---

### 🔍 Outlier Detection (IQR Method)

* Identifies outliers using:

  * Q1 (25th percentile)
  * Q3 (75th percentile)
  * IQR = Q3 − Q1
* Highlights extreme values

---

### 🔥 Correlation Heatmap

* Displays relationships between numeric variables
* Adaptive visualization for large datasets
* Strong correlation filtering

---

### 📊 Histogram

* Distribution analysis
* Shows mean and median trends

---

### 🏷️ Smart Bar Chart

* Works for both:

  * Categorical data
  * Numeric data (auto-binned)

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/dox.git
cd dox
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

---

### 3️⃣ Activate environment

#### Windows:

```bash
.\venv\Scripts\Activate.ps1
```

---

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
dox/
│── app.py
│── requirements.txt
│── README.md
│── venv/
```

---

## 🧠 Key Concepts Used

* Data Cleaning & Preprocessing
* Exploratory Data Analysis (EDA)
* IQR Outlier Detection
* Correlation Analysis
* Data Visualization

---

## ⚠️ Known Limitations

* Correlation heatmap requires at least **2 numeric columns**
* Bar chart may be less meaningful for high-cardinality columns
* Large datasets may impact performance

---

## 🔮 Future Improvements (Phase 3)

* Data cleaning tools (fill/drop missing values)
* Export cleaned dataset
* Advanced filtering & querying
* Machine learning insights
* Dashboard UI improvements

---

## 👑 Author

**Risi Nigarish**

> "Building tools, not just projects."

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share it

---

## 📜 License

This project is open-source and available under the MIT License.

---

🔥 *DOX v2 is not just a project — it's your step into real data systems.*
