import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- LOAD & BASIC CLEANING -------------------------------------------------
df = pd.read_csv("startup_funding.csv", encoding="utf-8")

# Rename awkward columns once, so the rest of the code is cleaner
df.rename(
    columns={
        "Date dd/mm/yyyy": "Date",
        "City  Location": "City",            # remove double‑space
        "InvestmentnType": "Investment Type" # fix the typo
    },
    inplace=True,
)

print("First 5 rows:\n", df.head())

# ---------- EASY QUESTIONS --------------------------------------------------------

# 1. Missing‑value percentages
print("\n--- Missing Value Percentage ---")
missing_pct = df.isna().mean().mul(100).round(2)
print(missing_pct)

# 2. Data‑type check
print("\n--- Data Types Before Fix ---")
print(df.dtypes)

# 3. Standardise Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
date_corrections = df["Date"].isna().sum()
print(f"\nDates needing correction (could not parse): {date_corrections}")

# 4. Duplicate rows
dup_count = df.duplicated().sum()
print(f"\nDuplicate rows: {dup_count}")

# 5. Clean “Amount in USD”
df["Amount in USD"] = (
    df["Amount in USD"]
    .str.replace(",", "", regex=False)
    .str.strip()
    .pipe(pd.to_numeric, errors="coerce")
)

overall_avg = df["Amount in USD"].mean()
print(f"\nOverall Average Funding Amount: ${overall_avg:,.2f}")

# 5b. Mean by industry
avg_by_industry = (
    df.groupby("Industry Vertical")["Amount in USD"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
)
print("\nTop 5 Average Funding by Industry Vertical:")
print(avg_by_industry.head(5))

# 6. Bar chart – average funding (top 10 industries)
plt.figure(figsize=(12, 6))
avg_by_industry.head(10).plot(kind="bar", color="skyblue")
plt.title("Top 10 Industry Verticals by Average Funding")
plt.ylabel("Average Funding Amount (USD)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# ---------- MEDIUM QUESTIONS ------------------------------------------------------

# 1. Outlier detection via IQR
Q1, Q3 = df["Amount in USD"].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
outliers = df[(df["Amount in USD"] < lower) | (df["Amount in USD"] > upper)]

print(f"\nOutliers detected: {len(outliers)}")
print("Ten largest outlier values:")
print(outliers["Amount in USD"].sort_values(ascending=False).head(10))

# 2. Box plot for ‘Amount in USD’
plt.figure(figsize=(8, 4))
sns.boxplot(y=df["Amount in USD"])
plt.title("Funding Amounts – Box Plot (Outliers Visible)")
plt.tight_layout()
plt.show()

# 3. Unique industry‑vertical count
unique_industries = df["Industry Vertical"].nunique(dropna=True)
print(f"\nUnique Industry Verticals: {unique_industries}")

# 4. Investment‑type distribution
investment_counts = df["Investment Type"].value_counts(dropna=False)
print("\nInvestment Type Distribution:\n", investment_counts)

# 5. Bar chart – top 10 investment types
plt.figure(figsize=(10, 5))
investment_counts.head(10).plot(kind="bar", color="coral")
plt.title("Top 10 Investment Types")
plt.ylabel("Number of Fundings")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# 6. City with the highest funding count
df["City"] = df["City"].str.strip()
top_city = df["City"].value_counts().idxmax()
top_city_count = df["City"].value_counts().max()
print(f"\nCity with highest number of fundings: {top_city} ({top_city_count})")

# 7. Bar chart – top 10 cities
plt.figure(figsize=(12, 6))
df["City"].value_counts().head(10).plot(kind="bar", color="mediumseagreen")
plt.title("Top 10 Cities by Number of Fundings")
plt.ylabel("Count of Fundings")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y")
plt.tight_layout()
plt.show()

# 8. Funding trend over time
df["Year"] = df["Date"].dt.year
funding_by_year = (
    df.groupby("Year")["Amount in USD"]
    .sum()
    .dropna()
    .sort_index()
)

print("\nTotal Funding by Year:")
print(funding_by_year)

# 9. Line chart – total funding by year
plt.figure(figsize=(10, 5))
funding_by_year.plot(marker="o", linestyle="-")
plt.title("Total Startup Funding Over the Years")
plt.ylabel("Total Funding (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()
