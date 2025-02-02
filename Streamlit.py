import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('./data-cumulative/cumulative.csv')
print(f'{df.shape}')
df['day'] = pd.to_datetime(df['day'])

# --------------------------------------------------------------------------------------

# My Streamlit App
st.title("Date Range Filter Example")

# 1. Date Inputs
min_date = df['day'].min()
max_date = df['day'].max()

# Create two columns for side-by-side date inputs
col1, col2 = st.columns(2)

# Date Inputs in separate columns
with col1:
    date_from = st.date_input("Date From", min_value=min_date, max_value=max_date, value=min_date)

with col2:
    date_to = st.date_input("Date To", min_value=min_date, max_value=max_date, value=max_date)

st.columns(1)
#date_from = st.date_input("Date From", min_value=min_date, max_value=max_date, value=min_date)
#date_to = st.date_input("Date To", min_value=min_date, max_value=max_date, value=max_date)
df_filtered = df[(df['day'] >= pd.to_datetime(date_from)) & (df['day'] <= pd.to_datetime(date_to))]

# Ensure 'Date From' is before 'Date To'
if date_from > date_to:
    st.error("'Date From' must be earlier than 'Date To'")
else:
    # 2. Filter DataFrame
    df_filtered = df[(df['day'] >= pd.to_datetime(date_from)) & (df['day'] <= pd.to_datetime(date_to))]

# --------------------------------------------------------------------------------------

# Create the plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_filtered['x_label'], 
    y=df_filtered['electricity_consumption'], 
    mode='lines+markers', 
    name='Electricity', 
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=df_filtered['x_label'], 
    y=df_filtered['gas_consumption'], 
    mode='lines+markers', 
    name='Gas', 
    line=dict(color='red')
))

# Update layout
fig.update_layout(
    title="Energy Consumption Over Time",
    xaxis_title="Time Interval (Start)",
    yaxis_title="Consumption",
    xaxis=dict(tickangle=45),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Display the filtered data
st.write(f"Showing data from **{date_from}** to **{date_to}**")
st.dataframe(df_filtered)
