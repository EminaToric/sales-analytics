# Sales Explorer

Interactive analytics dashboard demonstrating sales trends using the UCI Online Retail dataset as a proxy for Yoga Tots product sales.

## 🔍 Project Overview

This project showcases:
- Data loading & cleaning with **pandas**
- Exploratory Data Analysis (EDA) and static plots with **Matplotlib**
- Interactive dashboard built in **Streamlit**
- Rich visualizations using **Plotly**

## 🚀 Live Demo

Deployed on Streamlit Cloud:  
[Open Live Dashboard](https://share.streamlit.io/EminaToric/yoga-analytics/main/app.py)

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/EminaToric/yoga-analytics.git
   cd yoga-analytics
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # mac/linux
   # or .\venv\Scripts\Activate.ps1 on Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the dataset**

   This project uses the UCI Online Retail dataset. Download and save it as `OnlineRetail.xlsx` in the project root:
   ```bash
   curl -L -o OnlineRetail.xlsx \
     https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx
   ```

## 📊 Usage

### 1. Offline Analysis

Run the analysis script to generate static charts:
```bash
python analysis.py
```
- Output files: `monthly_revenue.png`, `top10_products.png`

### 2. Interactive Dashboard

Launch the Streamlit app:
```bash
streamlit run app.py
```
- Opens at `http://localhost:8501`
- Use sidebar filters to adjust date range and select products.

## 📁 Repo Structure

```
├── analysis.py         # Data cleaning & static EDA script
├── app.py              # Streamlit interactive dashboard
├── requirements.txt    # Python dependencies
└── README.md           # Project overview & instructions
```

## 🔗 Links

- **Dataset**: UCI Online Retail
- **Source Code**: https://github.com/EminaToric/yoga-analytics
- **Portfolio**: https://eminatoric.github.io

---
*Built by Emina Toric*

