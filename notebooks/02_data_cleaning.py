# ============================================
# Project: Revenue Margin Analysis
# Script: 02_data_cleaning.py
# Purpose: Clean data and add business columns
# ============================================

import pandas as pd
import os

# ============================================
# STEP 1 — LOAD RAW DATA
# ============================================

file_path = os.path.join('data', 'raw', 'Sample - Superstore.csv')
df = pd.read_csv(file_path, encoding='latin1')

print("✅ Raw data loaded")
print(f"Shape: {df.shape}")

# ============================================
# STEP 2 — FIX DATE COLUMNS
# ============================================

# Convert Order Date and Ship Date from text to actual dates
# This lets us do time-based analysis later
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Extract useful date parts
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
df['Order Quarter'] = df['Order Date'].dt.quarter

print("✅ Dates fixed and date parts extracted")
print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")

# ============================================
# STEP 3 — ADD BUSINESS CALCULATION COLUMNS
# ============================================

# Gross Margin % — how much profit we make per dollar of sales
# Formula: Profit / Sales * 100
df['Gross Margin %'] = (df['Profit'] / df['Sales'] * 100).round(2)

# Cost — how much the product cost us
# Formula: Sales - Profit
df['Cost'] = (df['Sales'] - df['Profit']).round(2)

# Discount Amount — actual dollar value of discount given
# Formula: Sales / (1 - Discount) * Discount
# This calculates the original price and finds the discount amount
df['Discount Amount'] = ((df['Sales'] / (1 - df['Discount'].replace(0, 1))) * df['Discount']).round(2)

# Revenue at Risk flag — transactions where margin is below 10%
# In a healthy business, we want margin above 10%
df['Is Low Margin'] = df['Gross Margin %'] < 10

# Loss flag — transactions where we actually lost money
df['Is Loss'] = df['Profit'] < 0

# High discount flag — transactions where discount is above 30%
df['Is High Discount'] = df['Discount'] > 0.30

print("✅ Business columns added")

# ============================================
# STEP 4 — VALIDATE OUR NEW COLUMNS
# ============================================

print("\n--- MARGIN DISTRIBUTION ---")
print(df['Gross Margin %'].describe().round(2))

print("\n--- LOSS MAKING TRANSACTIONS ---")
loss_count = df['Is Loss'].sum()
loss_revenue = df[df['Is Loss']]['Sales'].sum()
print(f"Number of loss transactions: {loss_count}")
print(f"Revenue from loss transactions: ${loss_revenue:,.2f}")

print("\n--- HIGH DISCOUNT TRANSACTIONS ---")
high_disc = df['Is High Discount'].sum()
print(f"Number of high discount transactions: {high_disc}")
print(f"Percentage of all transactions: {high_disc/len(df)*100:.1f}%")

print("\n--- LOW MARGIN TRANSACTIONS ---")
low_margin = df['Is Low Margin'].sum()
print(f"Number of low margin transactions: {low_margin}")
print(f"Percentage of all transactions: {low_margin/len(df)*100:.1f}%")

# ============================================
# STEP 5 — SAVE CLEAN DATA
# ============================================

output_path = os.path.join('data', 'processed', 'superstore_clean.csv')
df.to_csv(output_path, index=False)

print(f"\n✅ Clean data saved to {output_path}")
print(f"Final shape: {df.shape}")
print(f"Total columns now: {len(df.columns)}")
print(f"\nAll columns: {df.columns.tolist()}")