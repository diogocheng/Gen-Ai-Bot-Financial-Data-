import pandas as pd


# Load CSV
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


# Debugging: Check available companies and years
print("Available companies and years in dataset:")
print(df[['Company', 'Year']].drop_duplicates())

def simplechatbot(company, year, question):
    company = company.strip()
    question = question.strip().lower()
    
    try:
        year = int(year)  # Convert user input to integer
    except ValueError:
        return "Please enter a valid year (e.g., 2024)."

    # Filter the data
    data = df[(df["Company"] == company) & (df["Year"] == year)]

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

# Interactive chatbot loop
while True:
    question = input("\nWhat do you want to know? (Type 'exit' to quit)\n")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    company = input("From which company? ").strip()
    year = input("From which year? ").strip()

    response = simplechatbot(company, year, question)
    print(response)

