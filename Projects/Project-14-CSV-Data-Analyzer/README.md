# Project 14: CSV Data Analyzer & Visualizer

A modular and robust Python tool that loads tabular CSV data, calculates essential exploratory data statistics, and generates three fundamental types of Matplotlib visualizations saved as PNG files.

---

## 1. What This Project Does
This project serves as a practical, beginner-friendly introduction to data profiling and data visualization in Python. It automatically:
- Ingests and inspects CSV files using **pandas**.
- Identifies numerical vs. categorical data types and reports missing values.
- Computes summary statistics (mean, median, standard deviation, min, max, unique counts).
- Intelligently generates three core **Matplotlib** charts:
  1. **Line Chart** (`line_chart.png`)
  2. **Bar Chart** (`bar_chart.png`)
  3. **Pie Chart** (`pie_chart.png`)
- Saves the resulting images inside a local `charts/` directory.

---

## 2. Expected CSV Input
The script expects a CSV file named `train.csv` in this folder:
```
Projects/Project-14-CSV-Data-Analyzer/train.csv
```
*Note: The analyzer is dynamically designed. It does not hardcode column names and will adapt to analyze and chart different CSV datasets.*

---

## 3. Basic Statistics Calculated
When executed, the program generates an informative terminal report displaying:
- **Dimensions**: Total rows and columns.
- **Data Types**: Inferred types (`int64`, `float64`, `object`, etc.) for every column.
- **Missing Data**: Null/NaN count and percentage for every column.
- **Numerical Summary**: Count, mean, median, standard deviation, minimum, and maximum for numeric columns.
- **Categorical Summary**: Unique count cardinality for categorical columns.

---

## 4. What the 3 Charts Represent

### 1. Line Chart (`charts/line_chart.png`)
- **Concept**: Shows progression or value trends over a sequence of observations.
- **Implementation**: Tracks a numeric column over sample records with markers and gridlines using `plt.plot()`.

### 2. Bar Chart (`charts/bar_chart.png`)
- **Concept**: Compares discrete categories against numeric aggregates or frequencies.
- **Implementation**: Computes group averages (or category counts) across a low-cardinality category using `plt.bar()`.

### 3. Pie Chart (`charts/pie_chart.png`)
- **Concept**: Visualizes part-to-whole proportions.
- **Implementation**: Illustrates percentage distribution across categories with labels and percentage callouts using `plt.pie()`. Small categories are bundled into "Other" if necessary to prevent visual clutter.

---

## 5. Where Charts Are Saved
Generated visualizations are saved directly into the `charts/` folder:
```
Projects/Project-14-CSV-Data-Analyzer/
└── charts/
    ├── line_chart.png
    ├── bar_chart.png
    └── pie_chart.png
```

---

## 6. How to Run the Project

This project uses the shared virtual environment (`.venv`) located at the root of `Genai-Learning-Lab`.

### From the Root Directory:
```powershell
# 1. Activate the root environment
.\.venv\Scripts\Activate.ps1

# 2. Run the script
python Projects/Project-14-CSV-Data-Analyzer/main.py
```

### From the Project Directory:
```powershell
# 1. Navigate to the project directory
cd Projects/Project-14-CSV-Data-Analyzer

# 2. Run the analyzer
python main.py
```

*(Or directly run without activating: `..\..\.venv\Scripts\python.exe main.py`)*
