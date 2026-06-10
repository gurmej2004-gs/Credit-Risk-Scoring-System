# Credit Risk Scoring & Banking Analytics System

A comprehensive banking analytics system that analyzes customer financial data and assigns credit risk scores using rule-based business logic. This project demonstrates data processing, database management, SQL analytics, and visualization skills suitable for banking and financial sector applications.

## 📋 Project Overview

This system provides a complete end-to-end solution for credit risk assessment without using machine learning. Instead, it employs transparent, rule-based scoring logic that is easy to understand and explain - making it ideal for interviews and regulatory compliance.

### Key Features

- **Data Cleaning & Processing**: Automated data cleaning with missing value handling and duplicate removal
- **Rule-Based Risk Scoring**: Transparent credit risk scoring using predefined business rules
- **MySQL Database Integration**: Complete database schema with normalized tables
- **SQL Analytics**: Comprehensive SQL queries for business insights
- **Excel Reporting**: Automated Excel reports with pivot tables and charts
- **Power BI Dashboard**: Interactive visualization dashboard (instructions included)

## 🎯 Objective

Develop a banking analytics system that analyzes customer financial data and assigns a credit risk score using predefined business rules instead of machine learning, making the scoring logic transparent and explainable.

## 🛠 Technology Stack

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **MySQL**: Relational database management
- **SQL**: Database queries and analytics
- **Power BI**: Data visualization dashboard
- **Excel**: Reporting and pivot tables
- **Git**: Version control
- **GitHub**: Code repository

## 📊 Dataset Description

The dataset contains customer credit information with the following columns:

- `Unnamed: 0`: Customer ID
- `RevolvingUtilizationOfUnsecuredLines`: Credit utilization ratio
- `age`: Customer age
- `NumberOfTime30-59DaysPastDueNotWorse`: Number of times 30-59 days late
- `DebtRatio`: Debt to income ratio
- `MonthlyIncome`: Monthly income
- `NumberOfOpenCreditLinesAndLoans`: Number of open credit lines
- `NumberOfTimes90DaysLate`: Number of times 90+ days late
- `NumberRealEstateLoansOrLines`: Number of real estate loans
- `NumberOfTime60-89DaysPastDueNotWorse`: Number of times 60-89 days late
- `NumberOfDependents`: Number of dependents

**Dataset Location**: `data/cs-training.csv`

## 🗄 Database Design

The system uses a normalized MySQL database with the following tables:

### customers
Stores basic customer information
- `customer_id` (PRIMARY KEY)
- `age`
- `monthly_income`
- `dependents`

### credit_profile
Stores credit-related information
- `customer_id` (PRIMARY KEY, FOREIGN KEY)
- `debt_ratio`
- `credit_utilization`
- `open_credit_lines`
- `real_estate_loans`

### payment_history
Stores late payment history
- `customer_id` (PRIMARY KEY, FOREIGN KEY)
- `late_30_59`
- `late_60_89`
- `late_90`

### risk_scores
Stores calculated risk scores and categories
- `customer_id` (PRIMARY KEY, FOREIGN KEY)
- `risk_score`
- `risk_category`

## 📈 Risk Scoring Logic

The system uses a rule-based scoring approach starting from 100 points:

### Starting Score: 100

### Deductions

| Factor | Condition | Deduction |
|--------|-----------|-----------|
| Debt Ratio | DebtRatio > 0.50 | -20 |
| Credit Utilization | Credit Utilization > 0.80 | -15 |
| Late Payments (30-59 days) | > 0 | -15 |
| Late Payments (60-89 days) | > 0 | -15 |
| Late Payments (90+ days) | > 0 | -20 |
| Income | MonthlyIncome < 25000 | -10 |
| Dependents | Dependents > 3 | -5 |

### Risk Categories

| Score Range | Category |
|-------------|----------|
| 80-100 | Low Risk |
| 50-79 | Medium Risk |
| 0-49 | High Risk |

## 📁 Project Structure

```
Credit-Risk-Scoring-System/
│
├── data/
│   ├── cs-training.csv          # Original dataset
│   └── cleaned_data.csv         # Cleaned dataset
│
├── database/
│   ├── schema.sql               # Database schema
│   ├── insert_data.sql          # Data insertion script
│   └── queries.sql              # SQL analytics queries
│
├── src/
│   ├── data_cleaning.py         # Data cleaning module
│   ├── database_loader.py       # Database loading module
│   ├── risk_scoring.py          # Risk scoring module
│   ├── analytics.py             # SQL analytics module
│   └── excel_report.py          # Excel report generator
│
├── reports/
│   ├── risk_scores.csv          # Calculated risk scores
│   └── excel_report.xlsx        # Excel report with charts
│
├── dashboard/
│   └── powerbi_instructions.md  # Power BI dashboard guide
│
├── README.md                    # This file
├── requirements.txt             # Python dependencies
└── .gitignore                   # Git ignore rules
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Power BI Desktop (optional, for dashboard)

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd Credit-Risk-Scoring-System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up MySQL database**
```bash
# Login to MySQL
mysql -u root -p

# Execute schema
source database/schema.sql
```

5. **Run the pipeline**

```bash
# Step 1: Clean data
cd src
python data_cleaning.py

# Step 2: Load data into database
python database_loader.py

# Step 3: Calculate risk scores
python risk_scoring.py

# Step 4: Run analytics
python analytics.py

# Step 5: Generate Excel report
python excel_report.py
```

## 📊 SQL Analytics Queries

The system includes comprehensive SQL queries for business intelligence:

- Total customer count
- Average monthly income
- Risk category distribution
- High/Medium/Low risk customer lists
- Debt ratio analysis
- Income distribution by risk category
- Age distribution analysis
- Credit utilization by risk category

All queries are available in `database/queries.sql`

## 📊 Power BI Dashboard

### Dashboard Pages

#### 1. Overview
- Total Customers (KPI Card)
- Average Income (KPI Card)
- Average Risk Score (KPI Card)

#### 2. Risk Analysis
- Risk Category Distribution (Pie Chart)
- High Risk Customers (Table)
- Risk Score Distribution (Bar Chart)

#### 3. Financial Analysis
- Income Distribution (Bar Chart)
- Debt Ratio Distribution (Histogram)
- Credit Utilization Analysis (Bar Chart)

#### 4. Customer Analysis
- Age Distribution (Bar Chart)
- Dependents Analysis (Pie Chart)
- Income vs Risk Score (Scatter Plot)

### Dashboard Setup Instructions

See `dashboard/powerbi_instructions.md` for detailed Power BI setup guide.

## 📊 Excel Report Features

The automated Excel report includes:

- **KPI Summary Sheet**: Key performance indicators
- **Risk Summary Sheet**: Risk category distribution with pie chart
- **Income Summary Sheet**: Income analysis with bar chart
- **Customer Details Sheet**: Detailed customer information

## 🔧 Usage Examples

### Running Individual Modules

```bash
# Clean data only
python src/data_cleaning.py

# Calculate risk scores only
python src/risk_scoring.py

# Generate Excel report only
python src/excel_report.py
```

### Manual SQL Queries

```sql
-- Get high risk customers
SELECT * FROM risk_scores WHERE risk_category = 'High Risk';

-- Get average income by risk category
SELECT rs.risk_category, AVG(c.monthly_income) as avg_income
FROM risk_scores rs
JOIN customers c ON rs.customer_id = c.customer_id
GROUP BY rs.risk_category;
```

## 🎓 Learning Outcomes

This project demonstrates:

- **Data Engineering**: Data cleaning, transformation, and loading
- **Database Design**: Normalized schema design with foreign keys
- **SQL Skills**: Complex queries, joins, aggregations
- **Python Programming**: Modular code structure, error handling
- **Business Logic**: Rule-based decision making
- **Data Visualization**: Excel charts and Power BI dashboards
- **Version Control**: Git and GitHub workflow

## 💼 Suitable Roles

This project is ideal for interviews and portfolios for:

- Software Engineer
- Data Analyst
- Banking Analyst
- Business Analyst
- Graduate Trainee
- Financial Analyst
- Risk Analyst

## 🔮 Future Enhancements

- [ ] Web-based dashboard using Flask/Django
- [ ] Real-time risk scoring API
- [ ] Advanced analytics with trend analysis
- [ ] Customer segmentation analysis
- [ ] Automated alert system for high-risk customers
- [ ] Integration with credit bureau APIs
- [ ] Mobile application for risk monitoring

## 📝 Notes

- This system uses rule-based scoring for transparency and explainability
- No machine learning libraries are used as per requirements
- All scoring logic is documented and easily modifiable
- Database credentials should be stored in environment variables for production

## 🤝 Contributing

This is a portfolio project. Feel free to fork and customize for your needs.

## 📄 License

This project is for educational purposes.

## 👤 Author

Created as a portfolio project for banking and financial analytics roles.

---

**Note**: This project demonstrates fundamental data engineering, database management, and business analytics skills without using machine learning, making it perfect for explaining technical concepts in interviews.
