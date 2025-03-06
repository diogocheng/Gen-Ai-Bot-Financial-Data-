import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load CSV - This will run once when the app starts
df = pd.read_csv('data/datafinal.csv', sep=';', thousands=',')
df.columns = df.columns.str.strip()  # Remove spaces from column names

# Ensure no extra spaces in 'Company' names
df['Company'] = df['Company'].str.strip()

# Convert Year to integer if it's not already
df['Year'] = df['Year'].astype(int)

# Sort values
df = df.sort_values(['Company', 'Year'])
df['Revenue Growth (%)'] = df.groupby(['Company'])['Total Revenue'].pct_change() * 100
df['Net Income Growth (%)'] = df.groupby(['Company'])['Net Income'].pct_change() * 100
df['ROA (%)'] = (df['Net Income'] / df['Total Assets']) * 100  # Return on Assets
df['Profit Margin (%)'] = (df['Net Income'] / df['Total Revenue']) * 100  # Profit Margin
df['Debt to Assets Ratio'] = df['Total Liabilities'] / df['Total Assets']
df = df.sort_values(['Company', 'Year'], ascending=[True, False])

# Get available companies and years for dropdown menus
available_companies = sorted(df['Company'].unique())
available_years = sorted(df['Year'].unique(), reverse=True)

def financial_chatbot(company, year, question):
    try:
        year = int(year)  # Convert user input to integer
    except ValueError:
        return "Please enter a valid year (e.g., 2024)."

    # Filter the data (case-insensitive company matching)
    data = df[(df["Company"].str.lower() == company.lower()) & (df["Year"] == year)]

    if data.empty:
        return f"Sorry, no data found for {company} in {year}. Please check the company name and year."

    # Answer predefined questions
    if question.lower() == "what is the total revenue?":
        return f"The total revenue for {company} in {year} was {data['Total Revenue'].values[0]} million."

    elif question.lower() == "how has net income changed over the last year?":
        return f"The net income changed by {data['Net Income Growth (%)'].values[0]:.2f}% from the previous year."

    elif question.lower() == "what are the total assets?":
        return f"The total assets for {company} in {year} were {data['Total Assets'].values[0]} million."

    elif question.lower() == "what is the cash flow from operating activities?":
        return f"The cash flow from operations for {company} in {year} was {data['Cash Flow from Operating Activities'].values[0]} million."

    else:
        return "Sorry, I can only provide information on predefined queries."

# Routes
@app.route('/')
def index():
    return render_template('index.html', 
                          companies=available_companies, 
                          years=available_years,
                          questions=[
                              "What is the total revenue?",
                              "How has net income changed over the last year?",
                              "What are the total assets?",
                              "What is the cash flow from operating activities?"
                          ])

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    company = data.get('company', '')
    year = data.get('year', '')
    question = data.get('question', '')
    
    response = financial_chatbot(company, year, question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)