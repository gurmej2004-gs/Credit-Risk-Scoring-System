"""
Risk Scoring Module for Credit Risk Scoring System
Calculates credit risk scores using rule-based business logic
"""

import pandas as pd
import numpy as np

def calculate_risk_score(row):
    """
    Calculate risk score for a single customer based on business rules
    
    Starting Score: 100
    
    Deductions:
    - Debt Ratio > 0.50 → -20
    - Credit Utilization > 0.80 → -15
    - 30-59 Days Late > 0 → -15
    - 60-89 Days Late > 0 → -15
    - 90+ Days Late > 0 → -20
    - Monthly Income < 25000 → -10
    - Dependents > 3 → -5
    """
    score = 100
    
    # Debt Ratio deduction
    if row['DebtRatio'] > 0.50:
        score -= 20
    
    # Credit Utilization deduction
    if row['RevolvingUtilizationOfUnsecuredLines'] > 0.80:
        score -= 15
    
    # Late Payments deductions
    if row['NumberOfTime30-59DaysPastDueNotWorse'] > 0:
        score -= 15
    
    if row['NumberOfTime60-89DaysPastDueNotWorse'] > 0:
        score -= 15
    
    if row['NumberOfTimes90DaysLate'] > 0:
        score -= 20
    
    # Income deduction
    if row['MonthlyIncome'] < 25000:
        score -= 10
    
    # Dependents deduction
    if row['NumberOfDependents'] > 3:
        score -= 5
    
    # Ensure score doesn't go below 0
    score = max(0, score)
    
    return score

def determine_risk_category(score):
    """
    Determine risk category based on score
    
    80-100  → Low Risk
    50-79   → Medium Risk
    0-49    → High Risk
    """
    if score >= 80:
        return 'Low Risk'
    elif score >= 50:
        return 'Medium Risk'
    else:
        return 'High Risk'

def load_cleaned_data(filepath):
    """Load cleaned CSV data"""
    print(f"Loading cleaned data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Data loaded. Shape: {df.shape}")
    return df

def calculate_all_risk_scores(df):
    """Calculate risk scores for all customers"""
    print("\nCalculating risk scores...")
    
    # Calculate risk score for each customer
    df['risk_score'] = df.apply(calculate_risk_score, axis=1)
    
    # Determine risk category
    df['risk_category'] = df['risk_score'].apply(determine_risk_category)
    
    print("Risk scores calculated successfully")
    return df

def generate_risk_summary(df):
    """Generate summary statistics of risk scores"""
    print("\n" + "="*50)
    print("RISK SCORE SUMMARY")
    print("="*50)
    
    print(f"Total Customers: {len(df)}")
    print(f"Average Risk Score: {df['risk_score'].mean():.2f}")
    print(f"Min Risk Score: {df['risk_score'].min()}")
    print(f"Max Risk Score: {df['risk_score'].max()}")
    
    print("\n" + "="*50)
    print("RISK CATEGORY DISTRIBUTION")
    print("="*50)
    print(df['risk_category'].value_counts())
    
    print("\n" + "="*50)
    print("RISK CATEGORY PERCENTAGES")
    print("="*50)
    print(df['risk_category'].value_counts(normalize=True) * 100)

def save_risk_scores(df, output_path):
    """Save risk scores to CSV"""
    # Create output dataframe with only relevant columns
    if 'Unnamed: 0' in df.columns:
        customer_ids = df['Unnamed: 0']
    else:
        customer_ids = df.index
    
    risk_scores_df = pd.DataFrame({
        'customer_id': customer_ids,
        'risk_score': df['risk_score'],
        'risk_category': df['risk_category']
    })
    
    risk_scores_df.to_csv(output_path, index=False)
    print(f"\nRisk scores saved to {output_path}")
    print(f"Output shape: {risk_scores_df.shape}")

def main():
    """Main function to execute risk scoring pipeline"""
    # Define paths
    input_path = '../data/cleaned_data.csv'
    output_path = '../reports/risk_scores.csv'
    
    # Load cleaned data
    df = load_cleaned_data(input_path)
    
    # Calculate risk scores
    df = calculate_all_risk_scores(df)
    
    # Generate summary
    generate_risk_summary(df)
    
    # Save risk scores
    save_risk_scores(df, output_path)
    
    print("\n" + "="*50)
    print("RISK SCORING COMPLETED SUCCESSFULLY")
    print("="*50)
    
    return df

if __name__ == "__main__":
    main()
