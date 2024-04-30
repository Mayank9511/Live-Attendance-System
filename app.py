# import streamlit as st
# import pandas as pd
# import time
# from datetime import datetime


# ts=time.time()
# date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
# timestamp=datetime.fromtimestamp(ts).strftime("%H-%M-%S")
# df = pd.read_csv("Attendance/Attendance_" + date + ".csv") 
# st.title("Attendance Sheet: "+ date)

# st.dataframe(df, hide_index=false)
import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H-%M-%S")
file_path = "Attendance/Attendance_" + date + ".csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df.index = df.index + 1 
    df.index.name = "Serial No."
    st.title("Attendance Sheet: " + date)
    st.dataframe(df, hide_index=False, width=1800)
else:
    st.error("No attendance data available for today.")
