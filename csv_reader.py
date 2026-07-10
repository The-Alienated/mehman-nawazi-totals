import pandas as pd
import streamlit as st

#upload the data into the python file
uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=False, type="csv"
)

#Take Out the Overall Consumptions for Bottom Summary
if uploaded_files != None:
    df = pd.read_csv(uploaded_files)

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

#st.dataframe