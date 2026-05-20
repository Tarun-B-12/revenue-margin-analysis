# ============================================
# Project: Revenue Margin Analysis
# Script: 01_data_exploration.py
# Purpose: Load and explore the Superstore dataset
# ============================================

# --- IMPORTS ---
# pandas helps us load and work with data in tables
import pandas as pd

# os helps us work with file paths
import os

# ============================================
# STEP 1 — LOAD THE DATA
# ============================================

# Define the path to your raw data file
# This tells Python exactly where to find your file
file_path = os.path.join('data', 'raw', 'Sample - Superstore.csv')

# Load the CSV file into a pandas DataFrame
# A DataFrame is like an Excel table inside Python
# encoding='latin1' handles special characters in the file
df = pd.read_csv(file_path, encoding='latin1')

print("✅ Data loaded successfully")
print(f"📊 Total rows: {len(df)}")
print(f"📋 Total columns: {len(df.columns)}")

# ============================================
# STEP 2 — PREVIEW THE DATA
# ============================================

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
print(df.dtypes)

# ============================================
# STEP 3 — BASIC DATA QUALITY CHECKS
# ============================================

print("\n--- MISSING VALUES PER COLUMN ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(f"Number of duplicate rows: {df.duplicated().sum()}")

print("\n--- BASIC STATISTICS ---")
print(df.describe())

# ============================================
# STEP 4 — UNDERSTAND KEY BUSINESS COLUMNS
# ============================================

print("\n--- UNIQUE CATEGORIES ---")
print(df['Category'].unique())

print("\n--- UNIQUE SEGMENTS ---")
print(df['Segment'].unique())

print("\n--- UNIQUE REGIONS ---")
print(df['Region'].unique())

print("\n--- DATE RANGE ---")
print(f"Earliest order: {df['Order Date'].min()}")
print(f"Latest order: {df['Order Date'].max()}")

print("\n--- KEY FINANCIAL COLUMNS ---")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Total Discount Given: ${df['Discount'].sum():,.2f}")
print(f"Average Margin %: {(df['Profit'].sum() / df['Sales'].sum() * 100):.2f}%")