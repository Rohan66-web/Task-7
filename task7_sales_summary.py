
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
csv_file = "Online Sales.csv"
df = pd.read_csv(csv_file)

# Rename columns for simplicity
df = df.rename(columns={'Category': 'product', 'Sales': 'sales', 'Quantity': 'quantity'})

# Connect to SQLite database (or create it)
conn = sqlite3.connect("sales_data.db")

# Save relevant data to SQLite
df[['product', 'quantity', 'sales']].to_sql("sales", conn, if_exists="replace", index=False)

# Query: total quantity and revenue by product
query = '''
SELECT product, 
       SUM(quantity) AS total_qty, 
       SUM(sales) AS revenue
FROM sales
GROUP BY product
'''

# Run query and load into DataFrame
summary_df = pd.read_sql_query(query, conn)
print("Sales Summary:")
print(summary_df)

# Plot revenue by product
summary_df.plot(kind='bar', x='product', y='revenue', title="Revenue by Category", legend=False)
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Close connection
conn.close()
