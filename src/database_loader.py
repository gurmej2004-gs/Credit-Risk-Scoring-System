"""
Database Loader Module for Credit Risk Scoring System
Loads cleaned data into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

def create_connection(host='localhost', user='root', password='', database='credit_risk_db'):
    """Create database connection"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("MySQL Database connection successful")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def load_cleaned_data(filepath):
    """Load cleaned CSV data"""
    print(f"Loading cleaned data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Cleaned data loaded. Shape: {df.shape}")
    return df

def insert_customers(connection, df):
    """Insert data into customers table"""
    cursor = connection.cursor()
    
    # Map columns from dataset to customers table
    customers_data = []
    for idx, row in df.iterrows():
        customers_data.append((
            int(idx),
            int(row['age']),
            float(row['MonthlyIncome']),
            int(row['NumberOfDependents'])
        ))
    
    query = """
    INSERT INTO customers (customer_id, age, monthly_income, dependents)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        age = VALUES(age),
        monthly_income = VALUES(monthly_income),
        dependents = VALUES(dependents)
    """
    
    try:
        cursor.executemany(query, customers_data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records into customers table")
    except Error as e:
        print(f"Error inserting customers: {e}")
        connection.rollback()
    finally:
        cursor.close()

def insert_credit_profile(connection, df):
    """Insert data into credit_profile table"""
    cursor = connection.cursor()
    
    credit_profile_data = []
    for idx, row in df.iterrows():
        credit_profile_data.append((
            int(idx),
            float(row['DebtRatio']),
            float(row['RevolvingUtilizationOfUnsecuredLines']),
            int(row['NumberOfOpenCreditLinesAndLoans']),
            int(row['NumberRealEstateLoansOrLines'])
        ))
    
    query = """
    INSERT INTO credit_profile (customer_id, debt_ratio, credit_utilization, open_credit_lines, real_estate_loans)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        debt_ratio = VALUES(debt_ratio),
        credit_utilization = VALUES(credit_utilization),
        open_credit_lines = VALUES(open_credit_lines),
        real_estate_loans = VALUES(real_estate_loans)
    """
    
    try:
        cursor.executemany(query, credit_profile_data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records into credit_profile table")
    except Error as e:
        print(f"Error inserting credit_profile: {e}")
        connection.rollback()
    finally:
        cursor.close()

def insert_payment_history(connection, df):
    """Insert data into payment_history table"""
    cursor = connection.cursor()
    
    payment_history_data = []
    for idx, row in df.iterrows():
        payment_history_data.append((
            int(idx),
            int(row['NumberOfTime30-59DaysPastDueNotWorse']),
            int(row['NumberOfTime60-89DaysPastDueNotWorse']),
            int(row['NumberOfTimes90DaysLate'])
        ))
    
    query = """
    INSERT INTO payment_history (customer_id, late_30_59, late_60_89, late_90)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        late_30_59 = VALUES(late_30_59),
        late_60_89 = VALUES(late_60_89),
        late_90 = VALUES(late_90)
    """
    
    try:
        cursor.executemany(query, payment_history_data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records into payment_history table")
    except Error as e:
        print(f"Error inserting payment_history: {e}")
        connection.rollback()
    finally:
        cursor.close()

def insert_risk_scores(connection, df):
    """Insert risk scores into risk_scores table"""
    cursor = connection.cursor()
    
    risk_scores_data = []
    for _, row in df.iterrows():
        risk_scores_data.append((
            int(row['customer_id']),
            int(row['risk_score']),
            str(row['risk_category'])
        ))
    
    query = """
    INSERT INTO risk_scores (customer_id, risk_score, risk_category)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        risk_score = VALUES(risk_score),
        risk_category = VALUES(risk_category)
    """
    
    try:
        cursor.executemany(query, risk_scores_data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} records into risk_scores table")
    except Error as e:
        print(f"Error inserting risk_scores: {e}")
        connection.rollback()
    finally:
        cursor.close()

def generate_insert_sql_file(df, output_path):
    """Generate SQL insert statements file"""
    print(f"Generating SQL insert file at {output_path}...")
    
    with open(output_path, 'w') as f:
        f.write("-- ============================================\n")
        f.write("-- Insert Data into Credit Risk Database\n")
        f.write("-- ============================================\n")
        f.write("USE credit_risk_db;\n\n")
        
        # Customers insert
        f.write("-- ============================================\n")
        f.write("-- Insert into customers table\n")
        f.write("-- ============================================\n")
        f.write("INSERT INTO customers (customer_id, age, monthly_income, dependents) VALUES\n")
        customer_values = []
        for idx, row in df.iterrows():
            customer_values.append(
                f"    ({int(idx)}, "
                f"{int(row['age'])}, "
                f"{float(row['MonthlyIncome'])}, "
                f"{int(row['NumberOfDependents'])})"
            )
        f.write(",\n".join(customer_values) + ";\n\n")
        
        # Credit profile insert
        f.write("-- ============================================\n")
        f.write("-- Insert into credit_profile table\n")
        f.write("-- ============================================\n")
        f.write("INSERT INTO credit_profile (customer_id, debt_ratio, credit_utilization, open_credit_lines, real_estate_loans) VALUES\n")
        credit_values = []
        for idx, row in df.iterrows():
            credit_values.append(
                f"    ({int(idx)}, "
                f"{float(row['DebtRatio'])}, "
                f"{float(row['RevolvingUtilizationOfUnsecuredLines'])}, "
                f"{int(row['NumberOfOpenCreditLinesAndLoans'])}, "
                f"{int(row['NumberRealEstateLoansOrLines'])})"
            )
        f.write(",\n".join(credit_values) + ";\n\n")
        
        # Payment history insert
        f.write("-- ============================================\n")
        f.write("-- Insert into payment_history table\n")
        f.write("-- ============================================\n")
        f.write("INSERT INTO payment_history (customer_id, late_30_59, late_60_89, late_90) VALUES\n")
        payment_values = []
        for idx, row in df.iterrows():
            payment_values.append(
                f"    ({int(idx)}, "
                f"{int(row['NumberOfTime30-59DaysPastDueNotWorse'])}, "
                f"{int(row['NumberOfTime60-89DaysPastDueNotWorse'])}, "
                f"{int(row['NumberOfTimes90DaysLate'])})"
            )
        f.write(",\n".join(payment_values) + ";\n\n")
    
    print(f"SQL insert file generated successfully")

def main():
    """Main function to load data into database"""
    # Configuration - Update these with your MySQL credentials
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Add your MySQL password
        'database': 'credit_risk_db'
    }
    
    # Load cleaned data
    cleaned_data_path = '../data/cleaned_data.csv'
    df = load_cleaned_data(cleaned_data_path)
    
    # Generate SQL insert file
    insert_sql_path = '../database/insert_data.sql'
    generate_insert_sql_file(df, insert_sql_path)
    
    # Connect to database and insert data
    connection = create_connection(**DB_CONFIG)
    
    if connection:
        try:
            print("\n" + "="*50)
            print("LOADING DATA INTO DATABASE")
            print("="*50)
            
            insert_customers(connection, df)
            insert_credit_profile(connection, df)
            insert_payment_history(connection, df)
            
            print("\n" + "="*50)
            print("DATA LOADED SUCCESSFULLY")
            print("="*50)
            
        except Exception as e:
            print(f"Error during data loading: {e}")
        finally:
            connection.close()
            print("\nDatabase connection closed")
    else:
        print("\nNote: Database connection failed. SQL insert file has been generated.")
        print("You can manually run the SQL file in MySQL Workbench or command line.")

if __name__ == "__main__":
    main()
