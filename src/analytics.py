"""
Analytics Module for Credit Risk Scoring System
Performs SQL analytics on the database
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd

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

def execute_query(connection, query):
    """Execute a SQL query and return results as DataFrame"""
    try:
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def run_analytics(connection):
    """Run all analytics queries"""
    print("\n" + "="*50)
    print("RUNNING ANALYTICS QUERIES")
    print("="*50)
    
    # Query 1: Total Customers
    print("\n1. Total Customers")
    query1 = "SELECT COUNT(*) AS total_customers FROM customers"
    result1 = execute_query(connection, query1)
    if result1 is not None:
        print(result1)
    
    # Query 2: Average Monthly Income
    print("\n2. Average Monthly Income")
    query2 = "SELECT AVG(monthly_income) AS avg_income FROM customers"
    result2 = execute_query(connection, query2)
    if result2 is not None:
        print(result2)
    
    # Query 3: Risk Category Distribution
    print("\n3. Risk Category Distribution")
    query3 = """
    SELECT risk_category, COUNT(*) AS total
    FROM risk_scores
    GROUP BY risk_category
    """
    result3 = execute_query(connection, query3)
    if result3 is not None:
        print(result3)
    
    # Query 4: Average Debt Ratio
    print("\n4. Average Debt Ratio")
    query4 = "SELECT AVG(debt_ratio) AS avg_debt_ratio FROM credit_profile"
    result4 = execute_query(connection, query4)
    if result4 is not None:
        print(result4)
    
    # Query 5: Risk Score Statistics
    print("\n5. Risk Score Statistics")
    query5 = """
    SELECT 
        MIN(risk_score) AS min_risk_score,
        MAX(risk_score) AS max_risk_score,
        AVG(risk_score) AS avg_risk_score,
        COUNT(*) AS total_customers
    FROM risk_scores
    """
    result5 = execute_query(connection, query5)
    if result5 is not None:
        print(result5)
    
    # Query 6: High Risk Customers (Top 10)
    print("\n6. High Risk Customers (Top 10)")
    query6 = """
    SELECT * FROM risk_scores
    WHERE risk_category = 'High Risk'
    LIMIT 10
    """
    result6 = execute_query(connection, query6)
    if result6 is not None:
        print(result6)
    
    # Query 7: Top 10 Highest Income Customers
    print("\n7. Top 10 Highest Income Customers")
    query7 = """
    SELECT customer_id, monthly_income
    FROM customers
    ORDER BY monthly_income DESC
    LIMIT 10
    """
    result7 = execute_query(connection, query7)
    if result7 is not None:
        print(result7)
    
    # Query 8: Age Distribution
    print("\n8. Age Distribution")
    query8 = """
    SELECT 
        CASE 
            WHEN age < 25 THEN 'Under 25'
            WHEN age BETWEEN 25 AND 34 THEN '25-34'
            WHEN age BETWEEN 35 AND 44 THEN '35-44'
            WHEN age BETWEEN 45 AND 54 THEN '45-54'
            WHEN age BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS age_group,
        COUNT(*) AS total_customers
    FROM customers
    GROUP BY age_group
    ORDER BY age_group
    """
    result8 = execute_query(connection, query8)
    if result8 is not None:
        print(result8)
    
    # Query 9: Average Credit Utilization by Risk Category
    print("\n9. Average Credit Utilization by Risk Category")
    query9 = """
    SELECT 
        rs.risk_category,
        AVG(cp.credit_utilization) AS avg_credit_utilization
    FROM risk_scores rs
    JOIN credit_profile cp ON rs.customer_id = cp.customer_id
    GROUP BY rs.risk_category
    ORDER BY rs.risk_category
    """
    result9 = execute_query(connection, query9)
    if result9 is not None:
        print(result9)
    
    # Query 10: Income Distribution by Risk Category
    print("\n10. Income Distribution by Risk Category")
    query10 = """
    SELECT 
        rs.risk_category,
        AVG(c.monthly_income) AS avg_income,
        MIN(c.monthly_income) AS min_income,
        MAX(c.monthly_income) AS max_income
    FROM risk_scores rs
    JOIN customers c ON rs.customer_id = c.customer_id
    GROUP BY rs.risk_category
    ORDER BY rs.risk_category
    """
    result10 = execute_query(connection, query10)
    if result10 is not None:
        print(result10)

def save_analytics_report(connection, output_path):
    """Save analytics results to CSV"""
    print(f"\nSaving analytics report to {output_path}...")
    
    # Get all analytics results
    queries = {
        'total_customers': "SELECT COUNT(*) AS total_customers FROM customers",
        'avg_income': "SELECT AVG(monthly_income) AS avg_income FROM customers",
        'risk_distribution': """
            SELECT risk_category, COUNT(*) AS total
            FROM risk_scores
            GROUP BY risk_category
        """,
        'risk_stats': """
            SELECT 
                MIN(risk_score) AS min_risk_score,
                MAX(risk_score) AS max_risk_score,
                AVG(risk_score) AS avg_risk_score,
                COUNT(*) AS total_customers
            FROM risk_scores
        """,
        'age_distribution': """
            SELECT 
                CASE 
                    WHEN age < 25 THEN 'Under 25'
                    WHEN age BETWEEN 25 AND 34 THEN '25-34'
                    WHEN age BETWEEN 35 AND 44 THEN '35-44'
                    WHEN age BETWEEN 45 AND 54 THEN '45-54'
                    WHEN age BETWEEN 55 AND 64 THEN '55-64'
                    ELSE '65+'
                END AS age_group,
                COUNT(*) AS total_customers
            FROM customers
            GROUP BY age_group
            ORDER BY age_group
        """,
        'income_by_risk': """
            SELECT 
                rs.risk_category,
                AVG(c.monthly_income) AS avg_income,
                MIN(c.monthly_income) AS min_income,
                MAX(c.monthly_income) AS max_income
            FROM risk_scores rs
            JOIN customers c ON rs.customer_id = c.customer_id
            GROUP BY rs.risk_category
            ORDER BY rs.risk_category
        """
    }
    
    results = {}
    for name, query in queries.items():
        df = execute_query(connection, query)
        if df is not None:
            results[name] = df
    
    # Save each result to separate sheets in Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for name, df in results.items():
            df.to_excel(writer, sheet_name=name, index=False)
    
    print(f"Analytics report saved successfully")

def main():
    """Main function to execute analytics"""
    # Configuration - Update these with your MySQL credentials
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Add your MySQL password
        'database': 'credit_risk_db'
    }
    
    # Connect to database
    connection = create_connection(**DB_CONFIG)
    
    if connection:
        try:
            # Run analytics
            run_analytics(connection)
            
            # Save analytics report
            report_path = '../reports/analytics_report.xlsx'
            save_analytics_report(connection, report_path)
            
            print("\n" + "="*50)
            print("ANALYTICS COMPLETED SUCCESSFULLY")
            print("="*50)
            
        except Exception as e:
            print(f"Error during analytics: {e}")
        finally:
            connection.close()
            print("\nDatabase connection closed")
    else:
        print("\nNote: Database connection failed.")
        print("Please ensure MySQL is running and credentials are correct.")

if __name__ == "__main__":
    main()
