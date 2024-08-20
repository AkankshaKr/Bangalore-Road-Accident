from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import pandas as pd
import numpy as np
import streamlit as st
from dateutil import parser

st.set_page_config(
page_title="Bangalore Accident",
page_icon="🔎",
layout="wide",
initial_sidebar_state="auto",
)
st.title("Motor Vechicle Collisions in Bangalore City")
st.markdown("It is a Dashboard that can be used to analyse"
            " motor vehicle collision in Bangalore City 💥🚗💥")
@st.cache_data
def get_data():
    file_name = "bangalore-cas-alerts.csv"
    data = pd.read_csv(file_name, parse_dates=["deviceCode_time_recordedTime_$date"])
    data.drop_duplicates(inplace=True)

    # Renaming the columns
    columns = {
        "deviceCode_deviceCode": "deviceCode",
        "deviceCode_location_latitude": "latitude",
        "deviceCode_location_longitude": "longitude",
        "deviceCode_location_wardName": "wardName",
        "deviceCode_pyld_alarmType": "alarmType",
        "deviceCode_pyld_speed": "speed",
        "deviceCode_time_recordedTime_$date": "DateTime"
    }
    data.rename(columns=columns, inplace=True)
    data.dropna(subset=['latitude', 'longitude'])
    return data


df = get_data()

gb = GridOptionsBuilder()

# makes columns resizable, sortable and filterable by default
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

gb.configure_column(field="deviceCode", header_name="DeviceCode", width=130)
gb.configure_column(field="latitude", header_name="Latitude", width=90,
                    valueFormatter="value.toLocaleString()")
gb.configure_column(field="longitude", header_name="Longitude", width=90,
                    valueFormatter="value.toLocaleString()")
gb.configure_column(field="wardName", header_name="Ward Name", width=100, tooltipField="wardName")
gb.configure_column(field="alarmType", header_name="Alarm Type", width=100)
gb.configure_column(field="speed", header_name="Speed", width=50)
gb.configure_column(field="DateTime", header_name="DateTime", width=160)

gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=20)

go = gb.build()

st.header("Bangalore Accidents Record")
AgGrid(df, gridOptions=go, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)

df["Date/Time"] = df["DateTime"].apply(lambda x: parser.isoparse(x))
st.header("Select Month to view the Accident")
Month = st.slider("Month Number", 1, 12)
st.header("Type of Alarm during accident")
select = st.selectbox('Accidents Alarm Types', np.unique(df["alarmType"]))
df = df[df['Date/Time'].dt.month == Month]
st.map(df.query('alarmType == @select')[['latitude', 'longitude']].dropna(how="any"))
