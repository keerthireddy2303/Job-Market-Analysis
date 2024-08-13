import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Example DataFrame with experience column in range format
df = pd.read_csv('ibm.csv')

df = pd.DataFrame(df)

# Extract numeric values from 'experience' column
def extract_experience_range(experience_str):
    try:
        # Extract numeric values from range like '2 - 5 yrs'
        parts = experience_str.split(' - ')
        min_experience = int(parts[0].split()[0])
        max_experience = int(parts[1].split()[0])
        return min_experience, max_experience
    except:
        return None, None

# Apply extraction to the DataFrame
df[['min_experience', 'max_experience']] = df['experience'].apply(extract_experience_range).apply(pd.Series)

# Title
st.title("Job Market Analysis :bar_chart: :chart_with_upwards_trend:")
st.markdown("Explore job market data and make predictions based on job parameters.")


# Streamlit app code
st.sidebar.title('Data Analysis of Company details based on Experience ')
st.sidebar.header("Filter Options")

# Create slider for experience filter
min_exp = int(df['min_experience'].min())
max_exp = int(df['max_experience'].max())
experience_filter = st.sidebar.slider(
    "Select Experience Range",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)

# Filter DataFrame based on experience
filtered_df = df[(df['min_experience'] >= experience_filter[0]) & (df['max_experience'] <= experience_filter[1])]
st.write("Filtered Data", filtered_df)


# Bar Chart of Number of Positions by Industry
st.subheader("Number of Positions by Industry")
industry_counts = filtered_df['industry'].value_counts()
st.bar_chart(industry_counts)

st.sidebar.title('Data Analysis of Pie chart')

top_n = st.sidebar.number_input("Enter the number of top industries to display", min_value=1, max_value=50, value=5)

# Filter data to get top N industries based on job positions
industry_counts = df['industry'].value_counts()
top_industries = industry_counts.head(top_n).index

# Ensure the DataFrame is filtered based on the top industries
top_industry_df = df[df['industry'].isin(top_industries)]

st.subheader(f"Pie Chart Analysis of Top {top_n} industries")
fig, ax = plt.subplots()
industry_counts = top_industry_df['industry'].value_counts()
ax.pie(industry_counts, labels=industry_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)

def clean_payrate(value):
    try:
        # Remove commas and convert to float
        return float(value.replace(',', ''))
    except:
        return None

df['payrate'] = df['payrate'].apply(clean_payrate)

# Drop rows with NaN payrate
df.dropna(subset=['payrate'], inplace=True)

# Sidebar input for the number of top companies
st.sidebar.title("Select Top N Companies")
top_n = st.sidebar.number_input("Enter the number of top companies:", min_value=1, max_value=100, value=20, step=1)

# Group by company and calculate the average payrate
company_avg_payrate = df.groupby('company')['payrate'].mean().reset_index()

# Sort the companies by average payrate in descending order and get the top N
top_companies = company_avg_payrate.sort_values(by='payrate', ascending=False).head(top_n)

# Reset the index of the top companies DataFrame
top_companies.reset_index(drop=True, inplace=True)

# Create a line chart for the top companies
fig = px.line(top_companies, x='company', y='payrate', title=f'Top {top_n} Companies by Average Salary')
fig.update_traces(mode='lines+markers', hovertemplate='<b>Company</b>: %{x}<br><b>Average Salary</b>: %{y}')
fig.update_layout(xaxis_title='Company', yaxis_title='Average Salary')

# Display the chart in Streamlit
st.plotly_chart(fig)