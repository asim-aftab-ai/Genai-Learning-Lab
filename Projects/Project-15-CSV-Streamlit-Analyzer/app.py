import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PROJECT 15 - CSV DATA ANALYZER & VISUALIZER (STREAMLIT APP)
# ============================================================
# Learning Concepts:
# 1. Streamlit web application basics:
#    - st.set_page_config()
#    - st.title(), st.write(), st.info(), st.warning(), st.error()
# 2. File uploading with st.file_uploader()
# 3. Interactive DataFrames with st.dataframe()
# 4. Metric summary cards with st.metric()
# 5. Sidebar controls with st.sidebar
# 6. Interactive user actions with st.button()
# 7. Embedding Matplotlib figures using st.pyplot()
# ============================================================

# Configure page settings
st.set_page_config(
    page_title="CSV Data Analyzer",
    page_icon="📊",
    layout="wide"
)

# 1. Header & Introduction
st.title("📊 CSV Data Analyzer & Visualizer")
st.write(
    """
    Welcome! This interactive web app allows you to upload any CSV dataset, inspect its 
    structure, explore summary statistics, and generate clear visual charts.
    """
)

# 2. File Uploader
# st.file_uploader allows users to upload local files directly through the browser
uploaded_file = st.file_uploader("Choose a CSV file to analyze", type=["csv"])


def load_uploaded_csv(file):
    """Safely loads an uploaded CSV file into a pandas DataFrame."""
    try:
        df = pd.read_csv(file)
        if df.empty:
            st.error("Uploaded CSV file contains no data (empty table).")
            return None
        return df
    except pd.errors.EmptyDataError:
        st.error("Uploaded file is completely empty.")
        return None
    except Exception as e:
        st.error(f"Failed to read CSV file: {e}")
        return None


if uploaded_file is None:
    st.info("👋 Please upload a CSV file above to begin analysis.")
else:
    # 3. Read & Validate Uploaded Data
    df = load_uploaded_csv(uploaded_file)

    if df is not None:
        st.success(f"Successfully loaded **{uploaded_file.name}**!")

        # ----------------------------------------------------
        # Basic Dataset Information & Summary Cards
        # ----------------------------------------------------
        st.subheader("📋 Dataset Overview")
        rows, cols = df.shape
        missing_count = int(df.isna().sum().sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", f"{rows:,}")
        col2.metric("Total Columns", f"{cols:,}")
        col3.metric("Total Missing Values", f"{missing_count:,}")

        # Data preview
        st.write("### Data Preview")
        st.dataframe(df.head(50), use_container_width=True)

        # ----------------------------------------------------
        # Column Details & Statistics
        # ----------------------------------------------------
        st.subheader("🔍 Column Details & Statistics")

        col_left, col_right = st.columns(2)

        with col_left:
            st.write("**Column Data Types & Missing Counts:**")
            dtype_df = pd.DataFrame({
                "Column Name": df.columns,
                "Data Type": [str(t) for t in df.dtypes],
                "Missing Values": df.isna().sum().values,
                "Missing (%)": [(val / rows) * 100 for val in df.isna().sum().values]
            })
            st.dataframe(dtype_df, use_container_width=True)

        with col_right:
            st.write("**Numerical Summary Statistics:**")
            numeric_df = df.select_dtypes(include=["number"])
            if not numeric_df.empty:
                st.dataframe(numeric_df.describe().T, use_container_width=True)
            else:
                st.info("No numeric columns found for statistical summary.")

        # Categorical columns check
        cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
        num_cols = numeric_df.columns.tolist()

        # ----------------------------------------------------
        # Interactive Visualizations Section
        # ----------------------------------------------------
        st.subheader("📈 Data Visualizations")

        # Sidebar controls for chart configuration
        st.sidebar.header("🎨 Visualization Controls")
        chart_type = st.sidebar.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Pie Chart"]
        )

        # 1. Line Chart
        if chart_type == "Line Chart":
            st.write("#### Line Chart (Trend Analysis)")
            if not num_cols:
                st.warning("No numeric columns available in this dataset to generate a line chart.")
            else:
                selected_num = st.sidebar.selectbox("Select Numeric Column", num_cols)
                max_samples = min(rows, 200)
                sample_limit = st.sidebar.slider(
                    "Sample Limit (First N rows)",
                    min_value=10,
                    max_value=max(10, max_samples),
                    value=min(60, max_samples)
                )

                if st.button("Generate Line Chart", key="btn_line"):
                    series = df[selected_num].dropna().head(sample_limit).reset_index(drop=True)
                    if series.empty:
                        st.warning(f"No valid numeric data in column '{selected_num}'.")
                    else:
                        fig, ax = plt.subplots(figsize=(9, 4.5))
                        ax.plot(
                            series.index,
                            series.values,
                            color="#1f77b4",
                            marker="o",
                            markersize=4,
                            linestyle="-",
                            linewidth=1.5
                        )
                        ax.set_title(f"{selected_num} Trend (First {len(series)} Samples)", fontsize=13, pad=10)
                        ax.set_xlabel("Sample Index", fontsize=11)
                        ax.set_ylabel(selected_num, fontsize=11)
                        ax.grid(True, linestyle="--", alpha=0.6)
                        fig.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)

        # 2. Bar Chart
        elif chart_type == "Bar Chart":
            st.write("#### Bar Chart (Category Comparison)")
            # Filter candidate categorical columns or low cardinality columns
            bar_cat_options = [c for c in df.columns if df[c].nunique() <= 30]

            if not bar_cat_options:
                st.warning("No suitable category/group column (with <= 30 unique values) found.")
            else:
                selected_cat = st.sidebar.selectbox("Select Category Column", bar_cat_options)
                aggregation_mode = st.sidebar.radio(
                    "Aggregation Mode",
                    ["Frequency (Count)", "Average of Numeric Column"]
                )

                measure_col = None
                if aggregation_mode == "Average of Numeric Column":
                    if not num_cols:
                        st.warning("No numeric columns available to compute averages. Defaulting to Count.")
                        aggregation_mode = "Frequency (Count)"
                    else:
                        measure_col = st.sidebar.selectbox("Select Value Column to Average", num_cols)

                if st.button("Generate Bar Chart", key="btn_bar"):
                    fig, ax = plt.subplots(figsize=(9, 4.5))

                    if aggregation_mode == "Average of Numeric Column" and measure_col:
                        grouped = df.groupby(selected_cat)[measure_col].mean().dropna().sort_values(ascending=False).head(15)
                        categories = [str(c) for c in grouped.index]
                        values = grouped.values
                        ax.bar(categories, values, color="#2ca02c", edgecolor="#1b611b", width=0.55)
                        ax.set_title(f"Average {measure_col} by {selected_cat}", fontsize=13, pad=10)
                        ax.set_ylabel(f"Average {measure_col}", fontsize=11)
                    else:
                        counts = df[selected_cat].value_counts().head(15)
                        categories = [str(c) for c in counts.index]
                        values = counts.values
                        ax.bar(categories, values, color="#2ca02c", edgecolor="#1b611b", width=0.55)
                        ax.set_title(f"Distribution of {selected_cat}", fontsize=13, pad=10)
                        ax.set_ylabel("Count", fontsize=11)

                    ax.set_xlabel(selected_cat, fontsize=11)
                    plt.xticks(rotation=30, ha="right")
                    ax.grid(axis="y", linestyle="--", alpha=0.6)
                    fig.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

        # 3. Pie Chart
        elif chart_type == "Pie Chart":
            st.write("#### Pie Chart (Category Proportions)")
            pie_cat_options = [c for c in df.columns if 2 <= df[c].nunique() <= 12]

            if not pie_cat_options:
                st.warning("No suitable categorical column with 2 to 12 unique categories found for a pie chart.")
            else:
                selected_pie_cat = st.sidebar.selectbox("Select Category Column", pie_cat_options)

                if st.button("Generate Pie Chart", key="btn_pie"):
                    val_counts = df[selected_pie_cat].dropna().value_counts()
                    # Aggregate small slices into "Other" if more than 5 categories
                    if len(val_counts) > 5:
                        top_4 = val_counts.iloc[:4]
                        other_sum = val_counts.iloc[4:].sum()
                        val_counts = pd.concat([top_4, pd.Series({"Other": other_sum})])

                    labels = [str(lbl) for lbl in val_counts.index]
                    sizes = val_counts.values
                    colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948"]

                    fig, ax = plt.subplots(figsize=(6.5, 5.5))
                    ax.pie(
                        sizes,
                        labels=labels,
                        autopct="%1.1f%%",
                        startangle=140,
                        colors=colors[: len(sizes)],
                        wedgeprops={"edgecolor": "white", "linewidth": 1.5}
                    )
                    ax.set_title(f"Proportions of {selected_pie_cat}", fontsize=13, pad=12)
                    ax.axis("equal")
                    fig.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
