#!/usr/bin/env python
# coding: utf-8

# ## Exploring the data
# 

# ### Libraries Import

# In[10]:


# Importing necessary libraries
import pandas as pd  # For data manipulation and analysis
import seaborn as sns  # For visualization
import matplotlib.pyplot as plt  # Plotting library
import missingno as msno  # For visualizing missing data
import numpy as np  # Numerical operations


# ### Load Datasets

# In[11]:


# Load data from Desktop
users_df = pd.read_csv(r'C:\Users\sharm\OneDrive\Desktop\Test\USER_TAKEHOME.csv')
transactions_df = pd.read_csv(r'C:\Users\sharm\OneDrive\Desktop\Test\TRANSACTION_TAKEHOME.csv')
products_df = pd.read_csv(r'C:\Users\sharm\OneDrive\Desktop\Test\PRODUCTS_TAKEHOME.csv')


# ### Analyze Missing Values

# In[12]:


# Check for missing values
print("Users Dataset-Missing Values:")
print(users_df.isnull().sum())

print("\nTransactions Dataset-Missing Values:")
print(transactions_df.isnull().sum())

print("\nProducts Dataset-Missing Values:")
print(products_df.isnull().sum())


# ### Check unique values to identify inconsistencies

# In[13]:


print("\nUsers - Unique Values Per Column:")
print(users_df.nunique())

print("\nTransactions - Unique Values Per Column:")
print(transactions_df.nunique())

print("\nProducts - Unique Values Per Column:")
print(products_df.nunique())


# In[15]:


# Analyze future dates in BIRTH_DATE
if 'BIRTH_DATE' in users_df.columns:
    # Ensure BIRTH_DATE is parsed correctly
    users_df['BIRTH_DATE'] = pd.to_datetime(users_df['BIRTH_DATE'], errors='coerce')

    # Use a timezone-aware current timestamp
    now = pd.Timestamp.now().tz_localize('UTC')  # Make current time UTC

    # Compare with timezone-aware BIRTH_DATE
    future_birth_dates = users_df[users_df['BIRTH_DATE'] > now]
    print(f"\nFuture birth dates in Users Dataset: {len(future_birth_dates)}")
    print(future_birth_dates)

# Check for outliers in FINAL_SALE
if 'FINAL_SALE' in transactions_df.columns:
    transactions_df['FINAL_SALE'] = pd.to_numeric(transactions_df['FINAL_SALE'], errors='coerce')
    outlier_sales = transactions_df[transactions_df['FINAL_SALE'] > transactions_df['FINAL_SALE'].quantile(0.99)]
    print(f"\nOutliers in FINAL_SALE (top 1%): {len(outlier_sales)}")
    print(outlier_sales[['FINAL_SALE']].head())

# Check for inconsistent values in FINAL_QUANTITY
if 'FINAL_QUANTITY' in transactions_df.columns:
    # Convert FINAL_QUANTITY to string and check if all values are numeric
    transactions_df['FINAL_QUANTITY'] = transactions_df['FINAL_QUANTITY'].astype(str)
    inconsistent_quantities = transactions_df[~transactions_df['FINAL_QUANTITY'].str.isdigit()]
    print(f"\nInconsistent FINAL_QUANTITY values: {len(inconsistent_quantities)}")
    print(inconsistent_quantities[['FINAL_QUANTITY']].head())

# Analyze hierarchical product categories
hierarchical_columns = ['CATEGORY_1', 'CATEGORY_2', 'CATEGORY_3', 'CATEGORY_4']
if all(col in products_df.columns for col in hierarchical_columns):
    print("\nUnique values in hierarchical product categories:")
    for col in hierarchical_columns:
        unique_values = products_df[col].nunique()
        print(f"{col}: {unique_values} unique values")

# Analyze BARCODE formatting and missing
if 'BARCODE' in transactions_df.columns:
    missing_barcodes = transactions_df['BARCODE'].isnull().sum()
    print(f"\nMissing BARCODE values: {missing_barcodes}")
    # Scientific notation example
    transactions_df['BARCODE'] = transactions_df['BARCODE'].astype(str)
    scientific_barcodes = transactions_df['BARCODE'].str.contains(r'[eE][+-]?\d', na=False)
    print(f"Barcodes in scientific notation: {scientific_barcodes.sum()}")

# Analyze LANGUAGE codes
if 'LANGUAGE' in users_df.columns:
    language_codes = users_df['LANGUAGE'].unique()
    print(f"\nUnique LANGUAGE codes in Users Dataset: {language_codes}")

# Analyze varying date formats
date_columns = ['CREATED_DATE', 'PURCHASE_DATE']
for col in date_columns:
    if col in users_df.columns:
        try:
            pd.to_datetime(users_df[col], errors='raise')
            print(f"\n{col}: All values are consistent date formats.")
        except Exception as e:
            print(f"\n{col}: Inconsistent date formats detected. Error: {e}")


# ## Dataset Observations
# ### Users Dataset:
# - Columns include `ID`, `CREATED_DATE`, `BIRTH_DATE`, `STATE`, `LANGUAGE`, and `GENDER`.
# - Significant missing data in:
#   - `BIRTH_DATE`: 3.7% missing values.
#   - `STATE`: 4.8% missing values.
#   - `LANGUAGE`: 30.5% missing values.
#   - `GENDER`: 5.9% missing values.
# 
# ### Transactions Dataset:
# - Columns include purchase-related details such as `RECEIPT_ID`, `PURCHASE_DATE`, and `STORE_NAME`.
# - Observed issues:
#   - `BARCODE` has 11.5% missing values.
#   - Inconsistent values in `FINAL_QUANTITY` (`"zero"`).
#   - Empty `FINAL_SALE` values for some records.
# 
# ### Products Dataset:
# - Product categorization details include `CATEGORY_1`, `CATEGORY_2`, and `CATEGORY_3`.
# - Notable missing data in:
#   - `CATEGORY_4`: 92% missing.
#   - `MANUFACTURER`: 26.8% missing.
#   - `BRAND`: 26.8% missing.
# 

# ## Data Visualization to examine the data

# In[19]:


# Convert 'FINAL_SALE' to numeric and drop NaN values
transactions_df['FINAL_SALE'] = pd.to_numeric(transactions_df['FINAL_SALE'], errors='coerce')
transactions_df = transactions_df.dropna(subset=['FINAL_SALE'])


# In[29]:


# Distribution of FINAL_SAL
#normal scale
plt.figure(figsize=(12, 6))
plt.hist(transactions_df['FINAL_SALE'], bins=50, color='skyblue', edgecolor='black')
plt.title('Bar Chart of Final Sale Amounts', fontsize=16, fontweight='bold')
plt.xlabel('Final Sale Amount', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(visible=True, alpha=0.3)
plt.show()


# ### 
# This showed the distribution of numeric variables like FINAL_SALE. Any outliers or extreme values could be spotted easily (e.g., unrealistically large or small sales values).

# In[28]:


#log Scale
plt.figure(figsize=(12, 6))
plt.hist(transactions_df['FINAL_SALE'], bins=50, color='skyblue', edgecolor='black', log=True)
plt.title('Bar Chart of Final Sale Amounts', fontsize=16, fontweight='bold')
plt.xlabel('Final Sale Amount', fontsize=12)
plt.ylabel('Frequency (Log Scale)', fontsize=12)
plt.grid(visible=True, alpha=0.3)
plt.show()


# ### 
# Used log scale for FINAL_SALE to get better understanding of the distribution

# In[30]:


# Filter the top 1% outliers
filtered_sales = transactions_df[transactions_df['FINAL_SALE'] < transactions_df['FINAL_SALE'].quantile(0.99)]

plt.figure(figsize=(12, 6))
plt.hist(filtered_sales['FINAL_SALE'], bins=50, color='green', edgecolor='black')
plt.title('Bar Chart of Final Sale Amounts (Without Outliers)', fontsize=16, fontweight='bold')
plt.xlabel('Final Sale Amount', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(visible=True, alpha=0.3)
plt.show()


# ### 
# To visualize after removing the outliers to get clear understanding of the data 

# In[6]:


# State-Wise Distribution of Users:
plt.figure(figsize=(16, 8))
sns.barplot(x=users_state_counts.index, y=users_state_counts.values, palette='viridis')
plt.title('State-Wise Distribution of Users', fontsize=16, fontweight='bold')
plt.xlabel('State', fontsize=12)
plt.ylabel('Number of Users', fontsize=12)
plt.xticks(rotation=45, fontsize=10, ha='right')
plt.yticks(fontsize=10)
plt.grid(visible=True, alpha=0.3)
plt.tight_layout()
plt.show()


# ### 
# Bar chart highlighted the geographic spread of users, showing concentrated user clusters in specific states.

# In[3]:


# Missing Data Heatmap
msno.matrix(users_df)
plt.title('Missing Data in Users Dataset')
plt.show()

msno.matrix(transactions_df)
plt.title('Missing Data in Transactions Dataset')
plt.show()

msno.matrix(products_df)
plt.title('Missing Data in Products Dataset')
plt.show()


# ### 
# Above heatmap provided an overview of missing data across datasets, revealing which columns had a significant number of missing entries.Visualized gaps across datasets to prioritize cleaning efforts.

# In[36]:


# Function to calculate and plot missing data percentage (including columns with 0% missing values)
def plot_missing_data_all_columns(df, title):
    # Calculate percentage of missing values
    missing_percentage = df.isnull().sum() * 100 / len(df)
    
    # Sort by percentage (descending)
    missing_percentage = missing_percentage.sort_values(ascending=False)
    
    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(missing_percentage.index, missing_percentage, color="skyblue", edgecolor="black")
    plt.xlabel("Columns", fontsize=12)
    plt.ylabel("Percentage of Missing Values", fontsize=12)
    plt.title(f"{title} - Missing Data Percentage (All Columns)", fontsize=16, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Plot missing data percentage for Users Dataset
plot_missing_data_all_columns(users_df, "Users Dataset")

# Plot missing data percentage for Transactions Dataset
plot_missing_data_all_columns(transactions_df, "Transactions Dataset")

# Plot missing data percentage for Products Dataset
plot_missing_data_all_columns(products_df, "Products Dataset")


# ### 
# To quantify and visually highlight the extent of missing data in percentage terms, making prioritization of column cleaning easier.

# ### 1. Data Quality Issues Identified
# Missing Data Across Datasets:
# Users Dataset: High percentages of missing values in columns like LANGUAGE (30.5%) and moderate gaps in STATE (4.8%) and BIRTH_DATE (3.7%).
# 
# Transactions Dataset: FINAL_SALE contains null values; BARCODE has 11.5% missing.
# 
# Products Dataset: CATEGORY_4 is mostly missing (92%), with gaps in MANUFACTURER and BRAND (26.8% each).
# 
# Inconsistent or Dirty Data:
# Users Dataset: Future dates in BIRTH_DATE and inconsistent formats in categorical data (GENDER).
# 
# Transactions Dataset: Outliers in FINAL_SALE values, invalid or inconsistent FINAL_QUANTITY data ("zero" for some rows).
# 
# Products Dataset: CATEGORY hierarchy lacks clear definitions/documentation, leading to confusion.
# 
# ### 2. Fields That Are Challenging to Understand
# Hierarchical Product Categories: CATEGORY_1, CATEGORY_2, CATEGORY_3, and CATEGORY_4 are difficult to interpret without explicit labels.
# 
# BARCODE: Scientific notation and inconsistent matching with PRODUCTS data.
# 
# LANGUAGE Column in Users Data: Codes such as es-419 require external knowledge to interpret.
# 
# Date Columns: Varying formats in CREATED_DATE, PURCHASE_DATE, etc., impede seamless processing.
# 
# ## Conclusion
# With thorough cleaning (handling missing and inconsistent data), simplifying ambiguous fields (e.g., flattening product hierarchies), and addressing outliers, the datasets can be improved for meaningful analysis.
# 
