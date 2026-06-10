"""
Data Cleaning Module for Credit Risk Scoring System
Loads, cleans, and processes the credit risk dataset
"""

import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """Load the CSV dataset"""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Dataset loaded successfully. Shape: {df.shape}")
    return df

def remove_unnamed_column(df):
    """Remove 'Unnamed: 0' column if present"""
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
        print("Removed 'Unnamed: 0' column")
    return df

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print("\nHandling missing values...")
    print(f"Missing values before cleaning:\n{df.isnull().sum()}")
    
    # Fill missing MonthlyIncome with median
    if 'MonthlyIncome' in df.columns:
        median_income = df['MonthlyIncome'].median()
        df['MonthlyIncome'] = df['MonthlyIncome'].fillna(median_income)
        print(f"Filled missing MonthlyIncome with median: {median_income}")
    
    # Fill missing NumberOfDependents with 0
    if 'NumberOfDependents' in df.columns:
        df['NumberOfDependents'] = df['NumberOfDependents'].fillna(0)
        print("Filled missing NumberOfDependents with 0")
    
    print(f"Missing values after cleaning:\n{df.isnull().sum()}")
    return df

def remove_duplicates(df):
    """Remove duplicate records"""
    initial_count = len(df)
    df = df.drop_duplicates()
    removed_count = initial_count - len(df)
    print(f"\nRemoved {removed_count} duplicate records")
    return df

def check_invalid_values(df):
    """Check for invalid values"""
    print("\nChecking for invalid values...")
    
    # Check for negative values in columns that should be positive
    numeric_cols = ['age', 'MonthlyIncome', 'NumberOfDependents', 
                    'DebtRatio', 'RevolvingUtilizationOfUnsecuredLines',
                    'NumberOfOpenCreditLinesAndLoans', 'NumberRealEstateLoansOrLines',
                    'NumberOfTimes90DaysLate', 'NumberOfTime30-59DaysPastDueNotWorse',
                    'NumberOfTime60-89DaysPastDueNotWorse']
    
    for col in numeric_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                print(f"Warning: {negative_count} negative values found in {col}")
                # Replace negative values with 0
                df[col] = df[col].abs()
    
    print("Invalid value check completed")
    return df

def generate_summary_statistics(df):
    """Generate and display summary statistics"""
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    print(df.describe())
    print("\n" + "="*50)
    print("DATA INFO")
    print("="*50)
    print(df.info())
    print("\n" + "="*50)
    print("DATA TYPES")
    print("="*50)
    print(df.dtypes)

def save_cleaned_data(df, output_path):
    """Save the cleaned dataset"""
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to {output_path}")
    print(f"Final dataset shape: {df.shape}")

def main():
    """Main function to execute data cleaning pipeline"""
    # Define paths
    input_path = '../data/cs-training.csv'
    output_path = '../data/cleaned_data.csv'
    
    # Load data
    df = load_data(input_path)
    
    # Clean data
    df = remove_unnamed_column(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = check_invalid_values(df)
    
    # Generate summary
    generate_summary_statistics(df)
    
    # Save cleaned data
    save_cleaned_data(df, output_path)
    
    print("\n" + "="*50)
    print("DATA CLEANING COMPLETED SUCCESSFULLY")
    print("="*50)
    
    return df

if __name__ == "__main__":
    main()
