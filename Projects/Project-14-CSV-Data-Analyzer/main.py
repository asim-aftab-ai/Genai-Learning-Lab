from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PROJECT 14 - CSV DATA ANALYZER & VISUALIZER
# ============================================================
# Learning Concepts:
# 1. Loading & inspecting CSV data with pandas
# 2. Data profiling: dtypes, missing values, statistics
# 3. Dynamic column detection (numeric vs. categorical)
# 4. Matplotlib core visualization concepts:
#    - plt.figure()
#    - plt.plot() (Line chart)
#    - plt.bar()  (Bar chart)
#    - plt.pie()  (Pie chart)
#    - plt.title(), plt.xlabel(), plt.ylabel()
#    - plt.savefig()
# ============================================================


def load_dataset(file_path: Path):
    """Safely loads a CSV file into a pandas DataFrame."""
    if not file_path.exists():
        print(f"[Error] The file '{file_path.name}' was not found at:")
        print(f"        {file_path.resolve()}")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"[Success] Successfully loaded '{file_path.name}'!")
        return df
    except pd.errors.EmptyDataError:
        print(f"[Error] '{file_path.name}' is empty.")
        return None
    except Exception as e:
        print(f"[Error] Failed to read '{file_path.name}': {e}")
        return None


def print_data_overview(df: pd.DataFrame) -> None:
    """Prints comprehensive, beginner-friendly dataset statistics."""
    rows, cols = df.shape
    print("\n" + "=" * 55)
    print("              DATASET OVERVIEW")
    print("=" * 55)
    print(f"Total Rows (Records)    : {rows}")
    print(f"Total Columns (Features): {cols}")

    print("\n--- Columns & Data Types ---")
    for col in df.columns:
        print(f" - {col:<20} : {str(df[col].dtype):<10}")

    # Missing values analysis
    missing = df.isna().sum()
    missing_cols = missing[missing > 0]
    print("\n--- Missing Value Report ---")
    if missing_cols.empty:
        print("No missing values found across all columns! (Clean dataset)")
    else:
        for col, count in missing_cols.items():
            pct = (count / rows) * 100
            print(f" - {col:<20} : {count:>5} missing ({pct:.1f}%)")

    # Numeric summary statistics
    numeric_df = df.select_dtypes(include=["number"])
    if not numeric_df.empty:
        print("\n--- Numeric Column Summary ---")
        for col in numeric_df.columns:
            series = df[col].dropna()
            if series.empty:
                continue
            print(f"\nColumn: [{col}]")
            print(f"   Count : {len(series)}")
            print(f"   Mean  : {series.mean():.2f}")
            print(f"   Median: {series.median():.2f}")
            print(f"   StdDev: {series.std():.2f}")
            print(f"   Min   : {series.min():.2f}")
            print(f"   Max   : {series.max():.2f}")

    # Categorical summary
    cat_df = df.select_dtypes(exclude=["number"])
    if not cat_df.empty:
        print("\n--- Categorical Column Summary ---")
        for col in cat_df.columns[:5]:  # Display first few categorical columns
            unique_cnt = df[col].nunique(dropna=True)
            print(f" - {col:<20} : {unique_cnt:>5} unique values")
    print("=" * 55)


def generate_line_chart(df: pd.DataFrame, output_path: Path) -> bool:
    """Generates a line chart using suitable numeric data."""
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_cols:
        print("[Skipped] Cannot create line chart: No numeric columns found.")
        return False

    # Choose a numeric column with variance (avoiding constant or binary flags if possible)
    chosen_col = None
    for col in numeric_cols:
        if df[col].nunique() > 5 and not col.lower().endswith("id"):
            chosen_col = col
            break
    if not chosen_col:
        chosen_col = numeric_cols[0]

    # Use first 60 non-null values for a clean, readable line progression
    sample_series = df[chosen_col].dropna().head(60).reset_index(drop=True)

    if sample_series.empty:
        print(f"[Skipped] Column '{chosen_col}' has no valid values for a line chart.")
        return False

    # Matplotlib Line Chart demonstration
    plt.figure(figsize=(9, 5))
    plt.plot(sample_series.index, sample_series.values, color="#1f77b4", marker="o", markersize=4, linestyle="-", linewidth=1.5)
    plt.title(f"Line Chart: {chosen_col} Trend (First {len(sample_series)} Samples)", fontsize=13, pad=12)
    plt.xlabel("Sample Index", fontsize=11)
    plt.ylabel(chosen_col, fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.savefig(output_path, dpi=120)
    plt.close()
    return True


def generate_bar_chart(df: pd.DataFrame, output_path: Path) -> bool:
    """Generates a bar chart comparing categories or group averages."""
    # Find a good categorical or low-cardinality column (between 2 and 10 unique values)
    candidate_cat = None
    for col in df.columns:
        n_unique = df[col].nunique(dropna=True)
        if 2 <= n_unique <= 10 and not col.lower().endswith("id"):
            candidate_cat = col
            break

    # Fallback to any column with <= 15 unique values
    if not candidate_cat:
        for col in df.columns:
            if 2 <= df[col].nunique(dropna=True) <= 15:
                candidate_cat = col
                break

    if not candidate_cat:
        print("[Skipped] Cannot create bar chart: No suitable categorical column found.")
        return False

    # Find a continuous numeric column to average, or fall back to value counts
    numeric_cols = [c for c in df.select_dtypes(include=["number"]).columns if c != candidate_cat and not c.lower().endswith("id")]

    plt.figure(figsize=(9, 5))

    if numeric_cols:
        measure_col = numeric_cols[0]
        # Calculate group average
        grouped = df.groupby(candidate_cat)[measure_col].mean().dropna().sort_values(ascending=False)
        categories = [str(c) for c in grouped.index]
        values = grouped.values
        plt.bar(categories, values, color="#2ca02c", edgecolor="#1b611b", width=0.55)
        plt.title(f"Bar Chart: Average {measure_col} by {candidate_cat}", fontsize=13, pad=12)
        plt.xlabel(candidate_cat, fontsize=11)
        plt.ylabel(f"Average {measure_col}", fontsize=11)
    else:
        # Category counts
        counts = df[candidate_cat].value_counts().head(8)
        categories = [str(c) for c in counts.index]
        values = counts.values
        plt.bar(categories, values, color="#2ca02c", edgecolor="#1b611b", width=0.55)
        plt.title(f"Bar Chart: Distribution of {candidate_cat}", fontsize=13, pad=12)
        plt.xlabel(candidate_cat, fontsize=11)
        plt.ylabel("Count", fontsize=11)

    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.savefig(output_path, dpi=120)
    plt.close()
    return True


def generate_pie_chart(df: pd.DataFrame, output_path: Path) -> bool:
    """Generates a pie chart showing category proportions."""
    # Find a categorical column with 2 to 6 unique categories
    target_cat = None
    for col in df.columns:
        n = df[col].nunique(dropna=True)
        if 2 <= n <= 6 and not col.lower().endswith("id"):
            target_cat = col
            break

    # Fallback to any column with <= 8 unique values
    if not target_cat:
        for col in df.columns:
            if 2 <= df[col].nunique(dropna=True) <= 8:
                target_cat = col
                break

    if not target_cat:
        print("[Skipped] Cannot create pie chart: No suitable low-cardinality category found.")
        return False

    # Get counts and aggregate small slices into "Other" if needed
    val_counts = df[target_cat].dropna().value_counts()
    if len(val_counts) > 5:
        top_4 = val_counts.iloc[:4]
        other_sum = val_counts.iloc[4:].sum()
        val_counts = pd.concat([top_4, pd.Series({"Other": other_sum})])

    labels = [str(lbl) for lbl in val_counts.index]
    sizes = val_counts.values

    # Clean curated color palette
    colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948"]

    plt.figure(figsize=(7, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[: len(sizes)],
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    plt.title(f"Pie Chart: Proportions of {target_cat}", fontsize=13, pad=15)
    plt.axis("equal")  # Equal aspect ratio ensures circular pie
    plt.tight_layout()

    plt.savefig(output_path, dpi=120)
    plt.close()
    return True


def main():
    print("=" * 55)
    print("          CSV DATA ANALYZER & VISUALIZER")
    print("=" * 55)

    # 1. Path definitions
    project_dir = Path(__file__).parent
    csv_file = project_dir / "train.csv"
    charts_dir = project_dir / "charts"
    charts_dir.mkdir(exist_ok=True)

    # 2. Load dataset
    df = load_dataset(csv_file)
    if df is None:
        return

    # 3. Analyze data
    print_data_overview(df)

    # 4. Generate Visualizations
    print("\n--- Generating Visualizations ---")
    line_chart_path = charts_dir / "line_chart.png"
    bar_chart_path = charts_dir / "bar_chart.png"
    pie_chart_path = charts_dir / "pie_chart.png"

    charts_created = []

    # 1. Line Chart
    if generate_line_chart(df, line_chart_path):
        charts_created.append(line_chart_path)
        print(f" [OK] Created Line Chart: {line_chart_path.name}")

    # 2. Bar Chart
    if generate_bar_chart(df, bar_chart_path):
        charts_created.append(bar_chart_path)
        print(f" [OK] Created Bar Chart : {bar_chart_path.name}")

    # 3. Pie Chart
    if generate_pie_chart(df, pie_chart_path):
        charts_created.append(pie_chart_path)
        print(f" [OK] Created Pie Chart : {pie_chart_path.name}")

    # 5. Final summary
    print("\n" + "=" * 55)
    print("                  EXECUTION SUMMARY")
    print("=" * 55)
    print(f"Charts saved in : {charts_dir.resolve()}")
    for chart in charts_created:
        print(f" * {chart.name}")
    print("\nAll tasks completed successfully!")
    print("=" * 55)


if __name__ == "__main__":
    main()
