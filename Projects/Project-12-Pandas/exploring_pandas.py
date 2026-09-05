import pandas as pd


# ============================================================
# PROJECT 12 - PANDAS DATA ANALYSIS
# Dataset: Titanic train.csv
# ============================================================
#
# Questions this project answers:
# 1. What does the dataset look like?
# 2. Where is data missing?
# 3. How many passengers are in each passenger class?
# 4. What is the total fare collected in each class?
# 5. What is the survival rate for each class?
# 6. What are the top 5 most expensive tickets?
# 7. How is survival distributed by gender?
# 8. How can missing values be handled?
# 9. How can a custom category be created?
# 10. How can a summary be merged back into the main dataset?
# ============================================================


# ------------------------------------------------------------
# 1. LOAD THE DATA
# ------------------------------------------------------------

df = pd.read_csv("train.csv")

print("\n" + "=" * 60)
print("1. DATASET OVERVIEW")
print("=" * 60)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())


# ------------------------------------------------------------
# 2. IDENTIFY MISSING DATA
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("2. MISSING DATA")
print("=" * 60)

missing_data = df.isna().sum().sort_values(ascending=False)

print(missing_data)

print("\nColumns with missing data:")
print(missing_data[missing_data > 0])

print("\nMissing percentage:")
missing_percentage = (df.isna().mean() * 100).sort_values(ascending=False)
print(missing_percentage.round(2))


# ------------------------------------------------------------
# 3. GROUP BY PASSENGER CLASS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("3. PASSENGERS BY CLASS")
print("=" * 60)

class_summary = (
    df.groupby("Pclass")
      .agg(
          Passengers=("PassengerId", "count"),
          Total_Fare=("Fare", "sum"),
          Average_Fare=("Fare", "mean"),
          Survival_Rate=("Survived", "mean")
      )
      .sort_values("Passengers", ascending=False)
)

class_summary["Survival_Rate"] = (
    class_summary["Survival_Rate"] * 100
).round(2)

class_summary["Total_Fare"] = class_summary["Total_Fare"].round(2)
class_summary["Average_Fare"] = class_summary["Average_Fare"].round(2)

print(class_summary)


# ------------------------------------------------------------
# 4. TOTALS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("4. OVERALL TOTALS")
print("=" * 60)

print("Total passengers:", df["PassengerId"].count())
print("Total fare:", round(df["Fare"].sum(), 2))
print("Total survivors:", df["Survived"].sum())

print("\nSurvival counts:")
print(df["Survived"].value_counts())


# ------------------------------------------------------------
# 5. TOP 5 MOST EXPENSIVE TICKETS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("5. TOP 5 MOST EXPENSIVE TICKETS")
print("=" * 60)

top_5 = (
    df.sort_values("Fare", ascending=False)
      [["Name", "Pclass", "Fare", "Survived"]]
      .head(5)
)

print(top_5.to_string(index=False))


# ------------------------------------------------------------
# 6. VALUE COUNTS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("6. PASSENGERS BY GENDER")
print("=" * 60)

print(df["Sex"].value_counts())


print("\nPassenger count by embarkation port:")
print(df["Embarked"].value_counts(dropna=False))


# ------------------------------------------------------------
# 7. GROUP BY GENDER
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("7. SURVIVAL BY GENDER")
print("=" * 60)

gender_summary = (
    df.groupby("Sex")
      .agg(
          Passengers=("PassengerId", "count"),
          Survivors=("Survived", "sum"),
          Survival_Rate=("Survived", "mean")
      )
)

gender_summary["Survival_Rate"] = (
    gender_summary["Survival_Rate"] * 100
).round(2)

print(gender_summary)


# ------------------------------------------------------------
# 8. FILL MISSING VALUES
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("8. HANDLING MISSING VALUES")
print("=" * 60)

clean_df = df.copy()

# Age has missing values.
# Median age is used here because it is less affected by extreme ages.
age_median = clean_df["Age"].median()
clean_df["Age"] = clean_df["Age"].fillna(age_median)

# Embarked has only a few missing values.
# The most common port is used as a simple replacement.
embarked_mode = clean_df["Embarked"].mode()[0]
clean_df["Embarked"] = clean_df["Embarked"].fillna(embarked_mode)

# Cabin has many missing values.
# Instead of pretending that a missing cabin is a real cabin number,
# mark it as Unknown.
clean_df["Cabin"] = clean_df["Cabin"].fillna("Unknown")

print("Missing Age values after fillna():", clean_df["Age"].isna().sum())
print("Missing Embarked values after fillna():", clean_df["Embarked"].isna().sum())
print("Missing Cabin values after fillna():", clean_df["Cabin"].isna().sum())


# ------------------------------------------------------------
# 9. DROP MISSING DATA FOR A SPECIFIC ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("9. DROP MISSING DATA")
print("=" * 60)

# For an age-based analysis, passengers without an age cannot be used.
age_analysis = df.dropna(subset=["Age"])

print("Rows before dropping missing Age:", len(df))
print("Rows after dropping missing Age:", len(age_analysis))
print("Rows removed:", len(df) - len(age_analysis))


# ------------------------------------------------------------
# 10. APPLY - CREATE A CUSTOM FARE CATEGORY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("10. CUSTOM FARE CATEGORY")
print("=" * 60)

def classify_fare(fare):
    if fare < 10:
        return "Low"
    elif fare < 50:
        return "Medium"
    else:
        return "High"


clean_df["Fare_Category"] = clean_df["Fare"].apply(classify_fare)

print(clean_df["Fare_Category"].value_counts())


# ------------------------------------------------------------
# 11. MERGE - ADD CLASS SURVIVAL RATE BACK TO EACH PASSENGER
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("11. MERGE SUMMARY BACK INTO DATA")
print("=" * 60)

class_survival = (
    df.groupby("Pclass", as_index=False)["Survived"]
      .mean()
      .rename(columns={"Survived": "Class_Survival_Rate"})
)

merged_df = df.merge(
    class_survival,
    on="Pclass",
    how="left"
)

merged_df["Class_Survival_Rate"] = (
    merged_df["Class_Survival_Rate"] * 100
).round(2)

print(
    merged_df[
        ["PassengerId", "Name", "Pclass", "Survived", "Class_Survival_Rate"]
    ].head(10).to_string(index=False)
)


# ------------------------------------------------------------
# 12. FINAL FINDINGS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("12. FINAL FINDINGS")
print("=" * 60)

highest_class = class_summary["Survival_Rate"].idxmax()
highest_class_rate = class_summary.loc[highest_class, "Survival_Rate"]

most_common_gender = df["Sex"].value_counts().idxmax()

print(f"Most passengers were in class: {df['Pclass'].value_counts().idxmax()}")
print(f"Class with highest survival rate: {highest_class}")
print(f"Highest class survival rate: {highest_class_rate}%")
print(f"Most common gender in the dataset: {most_common_gender}")
print(f"Top ticket fare: {df['Fare'].max():.2f}")

print("\nProject analysis complete.")