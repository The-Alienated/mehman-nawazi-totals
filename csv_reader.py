import pandas as pd
import streamlit as st

uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=False, type="csv"
)

if uploaded_files is not None:
    df = pd.read_csv(uploaded_files)

    # 1. Add a dropdown sidebar to filter by Day
    if 'day' in df.columns:
        all_days = ["All Days"] + list(df['day'].unique())
        selected_day = st.sidebar.selectbox("Select Day to View", all_days)
        
        # Filter dataframe based on selection
        if selected_day != "All Days":
            df = df[df['day'] == selected_day]
    else:
        st.warning("To filter by day, add a 'day' column to your CSV file!")

    # 2. Pivot table calculation (remains the same)
    pivot = pd.pivot_table(
        df,
        index="station_id",
        columns="item_name",
        values="used",
        aggfunc="sum",
        fill_value=0
    )
    pivot.loc["Total"] = pivot.sum(axis=0)

    st.dataframe(pivot)

    itemInQuestion = ["Cups", "Plates", "Bowls", "Spoons", "Tissues"]
    
    st.divider()
    st.subheader("Overall Consumption of Items")
    for x in range(5):
        mask = df['item_name'] == itemInQuestion[x]
        total_used = df.loc[mask, 'used'].sum()
        st.write((f"Total {itemInQuestion[x]} used: {total_used}"))
