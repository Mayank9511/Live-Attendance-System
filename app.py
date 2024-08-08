import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")
file_path = "Attendance/Attendance_" + date + ".csv"

st.title('Harcourt Butler Technical University')
if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    def style_df(df):
        return df.style.set_properties(
            **{'text-align': 'center', 'padding': '10px'}
        ).set_table_styles(
            [
                {'selector': 'th', 'props': [('text-align', 'center'), ('width', '150px')]},
                {'selector': 'td', 'props': [('width', '200px')]}
            ]
        )
    st.header("Attendance Sheet: " + date)
    st.write(style_df(df).hide(axis='index').to_html(), unsafe_allow_html=True)    

    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    # Add download button
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Attendance Sheet",
        data=csv,
        file_name=f'Attendance_{date}.csv',
        mime='text/csv',
    )
else:
    st.error("No attendance data available for today.")
