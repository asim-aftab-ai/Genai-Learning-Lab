import io
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# PROJECT 15: CSV DATA ANALYSIS TOOLKIT (STREAMLIT APP)
# ==============================================================================
# Core Workflow:
# UPLOAD -> INSPECT -> FILTER -> ANALYZE -> VISUALIZE -> DOWNLOAD
#
# Key Concepts Used:
# - st.set_page_config()
# - st.title(), st.write(), st.subheader(), st.caption(), st.info(), st.warning(), st.error()
# - st.sidebar
# - st.file_uploader()
# - st.columns()
# - st.dataframe()
# - st.selectbox(), st.slider()
# - st.expander()
# - st.plotly_chart() (using Plotly Express)
# - st.download_button()
# ==============================================================================

# Configure Streamlit page settings
st.set_page_config(
    page_title="CSV Data Analysis Toolkit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_csv_safely(uploaded_file) -> pd.DataFrame | None:
    """Safely reads an uploaded CSV file into a pandas DataFrame.
    Handles encoding issues, empty files, and corrupted data gracefully.
    """
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("⚠️ The uploaded CSV file contains no data rows.")
            return None
        return df
    except pd.errors.EmptyDataError:
        st.error("⚠️ The uploaded file is completely empty.")
        return None
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if UTF-8 fails
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="latin-1")
            if df.empty:
                st.error("⚠️ The uploaded CSV file contains no data rows.")
                return None
            return df
        except Exception as e:
            st.error(f"⚠️ Could not decode CSV with UTF-8 or Latin-1: {e}")
            return None
    except Exception as e:
        st.error(f"⚠️ Failed to read CSV file: {e}")
        return None


# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS
# ------------------------------------------------------------------------------
st.sidebar.title("🛠️ Analysis Controls")

# File Uploader
st.sidebar.markdown("### 1. Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"],
    help="Select a local CSV file to begin analysis.",
)

# If no file is uploaded, render the welcoming landing screen
if uploaded_file is None:
    st.title("📊 CSV Data Analysis Toolkit")
    st.write(
        """
        Welcome to the **CSV Data Analysis Toolkit**! This local interactive application 
        allows you to explore, filter, analyze, visualize, and export any CSV dataset.
        """
    )

    st.info("👈 **Get started by uploading a CSV file in the sidebar.**")

    st.markdown("---")
    st.subheader("🚀 How It Works")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 1. Upload & Inspect")
        st.write(
            "Upload any CSV dataset to instantly view row/column counts, missing value summaries, "
            "data types, and raw records."
        )

    with col2:
        st.markdown("#### 2. Filter & Analyze")
        st.write(
            "Interactively isolate categories or numeric ranges. View descriptive statistics "
            "that update automatically based on your filtered view."
        )

    with col3:
        st.markdown("#### 3. Visualize & Export")
        st.write(
            "Generate interactive Plotly charts (Bar, Line, Scatter, Histogram, Pie) on the "
            "filtered data and download your clean subset as a new CSV."
        )

    st.stop()


# ------------------------------------------------------------------------------
# DATA INGESTION (ORIGINAL DATA)
# ------------------------------------------------------------------------------
df_raw = load_csv_safely(uploaded_file)

if df_raw is None:
    st.stop()

# Cache column types from original data
all_cols = df_raw.columns.tolist()
numeric_cols = df_raw.select_dtypes(include=["number"]).columns.tolist()
categorical_cols = df_raw.select_dtypes(exclude=["number"]).columns.tolist()

# ------------------------------------------------------------------------------
# SIDEBAR: DATA FILTERING
# ------------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 2. Interactive Filters")
st.sidebar.caption("Filters create a non-destructive view of your data.")

# Start with a full view of the original data
df_filtered = df_raw.copy()

# Categorical Filter
# Select candidate categorical columns (or columns with manageable unique counts <= 200)
cat_filter_candidates = [c for c in all_cols if df_raw[c].nunique() <= 200]
selected_cat_col = st.sidebar.selectbox(
    "Filter by Category Column",
    options=["(None)"] + cat_filter_candidates,
    help="Select a column to filter by specific categorical values.",
)

if selected_cat_col != "(None)":
    unique_vals = sorted(
        [str(val) for val in df_raw[selected_cat_col].dropna().unique()]
    )
    selected_val = st.sidebar.selectbox(
        f"Value for '{selected_cat_col}'",
        options=["All"] + unique_vals,
    )
    if selected_val != "All":
        df_filtered = df_filtered[
            df_filtered[selected_cat_col].astype(str) == selected_val
        ]

# Numeric Range Filter
selected_num_col = st.sidebar.selectbox(
    "Filter by Numeric Column Range",
    options=["(None)"] + numeric_cols,
    help="Select a numeric column to filter by minimum and maximum values.",
)

if selected_num_col != "(None)":
    col_series = df_raw[selected_num_col].dropna()
    if col_series.empty:
        st.sidebar.warning(f"Column '{selected_num_col}' contains only missing values.")
    else:
        min_v = float(col_series.min())
        max_v = float(col_series.max())

        if min_v == max_v:
            st.sidebar.info(
                f"Column '{selected_num_col}' has a single constant value: {min_v}"
            )
        else:
            slider_range = st.sidebar.slider(
                f"Range for '{selected_num_col}'",
                min_value=min_v,
                max_value=max_v,
                value=(min_v, max_v),
            )
            df_filtered = df_filtered[
                (df_filtered[selected_num_col] >= slider_range[0])
                & (df_filtered[selected_num_col] <= slider_range[1])
            ]

# Filter Summary in Sidebar
total_raw_rows = len(df_raw)
filtered_rows = len(df_filtered)
pct_remaining = (
    (filtered_rows / total_raw_rows * 100) if total_raw_rows > 0 else 0.0
)
st.sidebar.metric(
    label="Active Filtered Rows",
    value=f"{filtered_rows:,} / {total_raw_rows:,}",
    delta=f"{pct_remaining:.1f}% kept",
)

# ------------------------------------------------------------------------------
# SIDEBAR: VISUALIZATION CONTROLS
# ------------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 3. Visualization Setup")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart"],
)

# Dynamic Chart Parameters
bar_cat_col = None
bar_mode = None
bar_val_col = None

line_x_col = None
line_y_col = None

scatter_x_col = None
scatter_y_col = None
scatter_color_col = None

hist_col = None
hist_bins = 30

pie_cat_col = None

if chart_type == "Bar Chart":
    bar_cat_candidates = [c for c in all_cols if df_raw[c].nunique() <= 50]
    if bar_cat_candidates:
        bar_cat_col = st.sidebar.selectbox("Category Column (X-axis)", bar_cat_candidates)
        bar_mode = st.sidebar.radio(
            "Bar Value Calculation",
            ["Record Count (Frequency)", "Average of Numeric Column"],
        )
        if bar_mode == "Average of Numeric Column":
            if numeric_cols:
                bar_val_col = st.sidebar.selectbox("Value Column (to Average)", numeric_cols)
            else:
                st.sidebar.warning("No numeric columns available to compute an average.")

elif chart_type == "Line Chart":
    if numeric_cols:
        line_y_col = st.sidebar.selectbox("Value Column (Y-axis)", numeric_cols)
        line_x_options = ["(Row Index)"] + all_cols
        line_x_col = st.sidebar.selectbox("Sequence / Time Column (X-axis)", line_x_options)

elif chart_type == "Scatter Plot":
    if len(numeric_cols) >= 2:
        scatter_x_col = st.sidebar.selectbox("X-axis Numeric Column", numeric_cols, index=0)
        # Default Y to second numeric column if available
        default_y_idx = 1 if len(numeric_cols) > 1 else 0
        scatter_y_col = st.sidebar.selectbox("Y-axis Numeric Column", numeric_cols, index=default_y_idx)
        color_candidates = ["(None)"] + [c for c in all_cols if df_raw[c].nunique() <= 30]
        scatter_color_col = st.sidebar.selectbox("Color By (Optional)", color_candidates)
    elif len(numeric_cols) == 1:
        st.sidebar.info("Scatter plot requires at least two numeric columns.")

elif chart_type == "Histogram":
    if numeric_cols:
        hist_col = st.sidebar.selectbox("Numeric Column to Distribute", numeric_cols)
        hist_bins = st.sidebar.slider("Number of Bins", min_value=5, max_value=100, value=30)

elif chart_type == "Pie Chart":
    pie_candidates = [c for c in all_cols if 2 <= df_raw[c].nunique() <= 15]
    if pie_candidates:
        pie_cat_col = st.sidebar.selectbox("Category Column", pie_candidates)


# ==============================================================================
# MAIN PAGE CONTENT
# ==============================================================================
st.title("📊 CSV Data Analysis Toolkit")
st.caption(f"Active File: **{uploaded_file.name}** | Original Records: **{total_raw_rows:,}**")

# ------------------------------------------------------------------------------
# SECTION 1 — DATA OVERVIEW
# ------------------------------------------------------------------------------
st.markdown("---")
st.subheader("1. 📋 Data Overview")

total_cols = len(all_cols)
total_missing = int(df_raw.isna().sum().sum())
total_duplicates = int(df_raw.duplicated().sum())

# Metrics Cards
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Total Rows", f"{total_raw_rows:,}")
m_col2.metric("Total Columns", f"{total_cols:,}")
m_col3.metric("Missing Values", f"{total_missing:,}")
m_col4.metric("Duplicate Rows", f"{total_duplicates:,}")

# Preview of original data
st.write("#### Original Dataset Preview (First 20 Rows)")
st.dataframe(df_raw.head(20), width="stretch")

# Detailed column breakdown in an expander
with st.expander("📋 Detailed Column Structure & Missing Data Breakdown", expanded=False):
    col_breakdown = pd.DataFrame({
        "Column Name": all_cols,
        "Data Type": [str(df_raw[c].dtype) for c in all_cols],
        "Non-Null Count": [int(df_raw[c].notna().sum()) for c in all_cols],
        "Missing Count": [int(df_raw[c].isna().sum()) for c in all_cols],
        "Missing (%)": [
            round((df_raw[c].isna().sum() / total_raw_rows) * 100, 2)
            if total_raw_rows > 0
            else 0.0
            for c in all_cols
        ],
        "Unique Values": [int(df_raw[c].nunique()) for c in all_cols],
    })
    st.dataframe(col_breakdown, width="stretch")


# ------------------------------------------------------------------------------
# SECTION 2 — DATA FILTERING & FILTERED VIEW
# ------------------------------------------------------------------------------
st.markdown("---")
st.subheader("2. 🔍 Filtered Dataset View")

# Row count indicator
if filtered_rows == 0:
    st.warning(
        "⚠️ **No rows match your current filter criteria.** "
        "Please adjust or reset the filters in the sidebar."
    )
    st.stop()
elif filtered_rows < total_raw_rows:
    st.info(
        f"Filtered view: Showing **{filtered_rows:,}** of **{total_raw_rows:,}** records "
        f"({pct_remaining:.1f}% of original dataset)."
    )
else:
    st.success("Showing all original records (No restrictive filters currently applied).")

# Display the interactive filtered dataframe
st.dataframe(df_filtered.head(100), width="stretch")
if filtered_rows > 100:
    st.caption(f"Displaying first 100 of {filtered_rows:,} filtered records above.")


# ------------------------------------------------------------------------------
# SECTION 3 — STATISTICS (ON FILTERED DATA)
# ------------------------------------------------------------------------------
st.markdown("---")
st.subheader("3. 📊 Summary Statistics (Filtered Data)")

# Numerical Statistics
if numeric_cols:
    with st.expander("🔢 Numerical Statistics (Descriptive)", expanded=True):
        st.write("Summary statistics computed on the **active filtered data**:")
        num_stats = df_filtered[numeric_cols].describe().T
        st.dataframe(num_stats, width="stretch")
else:
    st.info("No numeric columns found in this dataset for numerical statistics.")

# Categorical Statistics
if categorical_cols:
    with st.expander("🔤 Categorical Columns Summary", expanded=False):
        cat_summary_list = []
        for c in categorical_cols:
            series_non_null = df_filtered[c].dropna()
            if not series_non_null.empty:
                top_val = series_non_null.mode().iloc[0]
                top_freq = int((series_non_null == top_val).sum())
                top_pct = round((top_freq / len(series_non_null)) * 100, 1)
            else:
                top_val = "N/A"
                top_freq = 0
                top_pct = 0.0

            cat_summary_list.append({
                "Column Name": c,
                "Unique Values": int(series_non_null.nunique()),
                "Most Common Value": str(top_val),
                "Top Value Frequency": top_freq,
                "Top Value (% of Non-Null)": f"{top_pct}%",
            })

        st.dataframe(pd.DataFrame(cat_summary_list), width="stretch")


# ------------------------------------------------------------------------------
# SECTION 4 — VISUALIZATION (PLOTLY EXPRESS ON FILTERED DATA)
# ------------------------------------------------------------------------------
st.markdown("---")
st.subheader("4. 📈 Interactive Visualization (Filtered Data)")

if df_filtered.empty:
    st.warning("⚠️ No data available to visualize. Adjust your filters to include data.")
else:
    # 1. Bar Chart
    if chart_type == "Bar Chart":
        if not bar_cat_col:
            st.warning(
                "⚠️ Bar chart requires a categorical or low-cardinality column (<= 50 unique values). "
                "None was found in this dataset."
            )
        else:
            if bar_mode == "Average of Numeric Column":
                if not bar_val_col:
                    st.warning("Please select a numeric column to calculate the average.")
                else:
                    grouped = (
                        df_filtered.groupby(bar_cat_col)[bar_val_col]
                        .mean()
                        .dropna()
                        .reset_index()
                        .sort_values(by=bar_val_col, ascending=False)
                    )
                    if grouped.empty:
                        st.warning("No valid data available after grouping.")
                    else:
                        fig = px.bar(
                            grouped,
                            x=bar_cat_col,
                            y=bar_val_col,
                            title=f"Average {bar_val_col} by {bar_cat_col}",
                            labels={bar_val_col: f"Mean {bar_val_col}", bar_cat_col: bar_cat_col},
                            template="plotly_white",
                            color_discrete_sequence=["#1f77b4"],
                        )
                        fig.update_layout(xaxis_tickangle=-30)
                        st.plotly_chart(fig, width="stretch")
            else:
                # Frequency Count mode
                val_counts = (
                    df_filtered[bar_cat_col]
                    .value_counts()
                    .reset_index()
                )
                val_counts.columns = [bar_cat_col, "Count"]
                if val_counts.empty:
                    st.warning("No categorical values found to plot.")
                else:
                    fig = px.bar(
                        val_counts,
                        x=bar_cat_col,
                        y="Count",
                        title=f"Frequency Distribution of {bar_cat_col}",
                        template="plotly_white",
                        color_discrete_sequence=["#2ca02c"],
                    )
                    fig.update_layout(xaxis_tickangle=-30)
                    st.plotly_chart(fig, width="stretch")

    # 2. Line Chart
    elif chart_type == "Line Chart":
        if not numeric_cols:
            st.warning("⚠️ Line chart requires at least one numeric column for the Y-axis.")
        elif not line_y_col:
            st.warning("Please select a numeric column for the Y-axis in the sidebar.")
        else:
            plot_df = df_filtered.dropna(subset=[line_y_col]).copy()
            if plot_df.empty:
                st.warning(f"No non-null data available in '{line_y_col}' to plot.")
            else:
                if line_x_col == "(Row Index)":
                    plot_df = plot_df.reset_index(drop=True)
                    x_axis_name = "Index"
                    plot_df[x_axis_name] = plot_df.index
                else:
                    x_axis_name = line_x_col

                fig = px.line(
                    plot_df,
                    x=x_axis_name,
                    y=line_y_col,
                    title=f"{line_y_col} Trend over {x_axis_name}",
                    markers=True if len(plot_df) <= 100 else False,
                    template="plotly_white",
                    color_discrete_sequence=["#ff7f0e"],
                )
                st.plotly_chart(fig, width="stretch")

    # 3. Scatter Plot
    elif chart_type == "Scatter Plot":
        if len(numeric_cols) < 2:
            st.warning(
                f"⚠️ Scatter plots require at least 2 numeric columns. "
                f"This dataset currently has {len(numeric_cols)}."
            )
        elif not scatter_x_col or not scatter_y_col:
            st.warning("Please select valid numeric columns for both X and Y axes in the sidebar.")
        else:
            scatter_df = df_filtered.dropna(subset=[scatter_x_col, scatter_y_col]).copy()
            if scatter_df.empty:
                st.warning("No rows with non-null values for both selected numeric columns.")
            else:
                color_arg = (
                    scatter_color_col
                    if scatter_color_col and scatter_color_col != "(None)"
                    else None
                )
                fig = px.scatter(
                    scatter_df,
                    x=scatter_x_col,
                    y=scatter_y_col,
                    color=color_arg,
                    title=f"{scatter_y_col} vs {scatter_x_col}",
                    template="plotly_white",
                )
                st.plotly_chart(fig, width="stretch")

    # 4. Histogram
    elif chart_type == "Histogram":
        if not numeric_cols:
            st.warning("⚠️ Histogram requires at least one numeric column. None found in this dataset.")
        elif not hist_col:
            st.warning("Please select a numeric column in the sidebar.")
        else:
            hist_df = df_filtered.dropna(subset=[hist_col])
            if hist_df.empty:
                st.warning(f"No non-null data available in '{hist_col}' for histogram.")
            else:
                fig = px.histogram(
                    hist_df,
                    x=hist_col,
                    nbins=hist_bins,
                    title=f"Distribution of {hist_col} ({hist_bins} Bins)",
                    template="plotly_white",
                    color_discrete_sequence=["#9467bd"],
                )
                st.plotly_chart(fig, width="stretch")

    # 5. Pie Chart
    elif chart_type == "Pie Chart":
        if not pie_cat_col:
            st.warning(
                "⚠️ Pie charts require a categorical column with 2 to 15 unique categories "
                "to ensure visual clarity. None was found in this dataset."
            )
        else:
            pie_counts = (
                df_filtered[pie_cat_col]
                .dropna()
                .value_counts()
                .reset_index()
            )
            pie_counts.columns = [pie_cat_col, "Count"]
            if pie_counts.empty:
                st.warning(f"No data available in '{pie_cat_col}' to construct a pie chart.")
            else:
                fig = px.pie(
                    pie_counts,
                    names=pie_cat_col,
                    values="Count",
                    title=f"Proportions of {pie_cat_col}",
                    template="plotly_white",
                )
                st.plotly_chart(fig, width="stretch")


# ------------------------------------------------------------------------------
# SECTION 5 — DOWNLOAD FILTERED DATA
# ------------------------------------------------------------------------------
st.markdown("---")
st.subheader("5. 📥 Export Filtered Data")
st.write(
    f"Download your active filtered dataset (**{filtered_rows:,}** rows) "
    f"as a clean CSV file directly to your local computer."
)

# Convert filtered DataFrame to CSV in memory (no disk file creation)
csv_buffer = io.StringIO()
df_filtered.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode("utf-8")

output_filename = (
    f"filtered_{uploaded_file.name}"
    if uploaded_file.name.endswith(".csv")
    else f"filtered_{uploaded_file.name}.csv"
)

st.download_button(
    label=f"📥 Download Filtered Data ({filtered_rows:,} rows)",
    data=csv_bytes,
    file_name=output_filename,
    mime="text/csv",
    help="Click to download the current filtered dataset as a CSV.",
)
