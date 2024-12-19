import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit App Title
st.title("Battery Data Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload Battery Data CSV File", type="csv")

if uploaded_file:
    # Load data
    battery_data = pd.read_csv(
        uploaded_file,
        header=None,
        names=["timestamp", "vin", "vbat", "charge_current", "temperature", "capacity"]
    )
    
    # Parse timestamps
    timestamp_formats = ["%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M"]
    for fmt in timestamp_formats:
        try:
            battery_data['timestamp'] = pd.to_datetime(battery_data['timestamp'], format=fmt, errors='coerce')
            if battery_data['timestamp'].notna().sum() > 0:
                break
        except Exception:
            continue
    
    # Drop invalid timestamps
    battery_data = battery_data.dropna(subset=['timestamp'])
    battery_data = battery_data.sort_values(by='timestamp')
    
    # Display Data
    st.subheader("Uploaded Data Sample")
    st.dataframe(battery_data.head())
    
    # Filter data by time range
    st.subheader("Filter Data by Time Range")
    start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)", value=str(battery_data['timestamp'].min()))
    end_time = st.text_input("End Time (YYYY-MM-DD HH:MM:SS)", value=str(battery_data['timestamp'].max()))
    
    if start_time and end_time:
        filtered_data = battery_data[
            (battery_data['timestamp'] >= start_time) & (battery_data['timestamp'] <= end_time)
        ]
    else:
        filtered_data = battery_data

    # Plot Parameters
    st.subheader("Parameter Plots")
    fig, axes = plt.subplots(5, 1, figsize=(15, 12), sharex=True)
    
    axes[0].plot(filtered_data['timestamp'], filtered_data['vbat'], label='vbat (Battery Voltage)', color='blue')
    axes[0].set_ylabel('Voltage (V)')
    axes[0].set_title('Battery Voltage (vbat) Over Time')
    axes[0].legend()
    
    axes[1].plot(filtered_data['timestamp'], filtered_data['charge_current'], label='Charge Current', color='green')
    axes[1].set_ylabel('Current (A)')
    axes[1].set_title('Charge Current Over Time')
    axes[1].legend()
    
    axes[2].plot(filtered_data['timestamp'], filtered_data['vin'], label='vin (Input Voltage)', color='red')
    axes[2].set_ylabel('Voltage (V)')
    axes[2].set_title('Input Voltage (vin) Over Time')
    axes[2].legend()

    axes[3].plot(filtered_data['timestamp'], filtered_data['capacity'], label='Capacity', color='purple')
    axes[3].set_ylabel('Capacity')
    axes[3].set_title('Battery Capacity Over Time')
    axes[3].set_xlabel('Timestamp')
    axes[3].legend()
    
    axes[4].plot(filtered_data['timestamp'], filtered_data['temperature'], label='Temperature', color='orange')
    axes[4].set_ylabel('Temperature (°C)')
    axes[4].set_title('Battery Temperature Over Time')
    axes[4].legend()
    

    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Display Filtered Data
    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    # Download Filtered Data
    st.subheader("Download Filtered Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download Filtered Data as CSV", data=csv, file_name="filtered_battery_data.csv", mime="text/csv")
