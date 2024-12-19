import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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
        names=["timestamp", "vbat", "discharge_current", "charge_current", "temperature", "capacity_percentage"]
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

    # Plot Parameters - Default Matplotlib
    st.subheader("Default Plots")
    fig, axes = plt.subplots(5, 1, figsize=(15, 15), sharex=True)

    # Plot vbat (Battery Voltage)
    axes[0].plot(filtered_data['timestamp'], filtered_data['vbat'], label='Battery Voltage (vbat)', color='blue')
    axes[0].set_ylabel('Voltage (V)')
    axes[0].set_title('Battery Voltage (vbat) Over Time')
    axes[0].legend()
    
    # Plot charge_current
    axes[1].plot(filtered_data['timestamp'], filtered_data['charge_current'], label='Charge Current', color='green')
    axes[1].set_ylabel('Current (A)')
    axes[1].set_title('Charge Current Over Time')
    axes[1].legend()
    
    # Plot capacity_percentage
    axes[2].plot(filtered_data['timestamp'], filtered_data['capacity_percentage'], label='Capacity Percentage', color='purple')
    axes[2].set_ylabel('Capacity (%)')
    axes[2].set_title('Battery Capacity Over Time')
    axes[2].legend()
    
    # Plot discharge_current
    axes[3].plot(filtered_data['timestamp'], filtered_data['discharge_current'], label='Discharge Current', color='cyan')
    axes[3].set_ylabel('Current (A)')
    axes[3].set_title('Discharge Current Over Time')
    axes[3].legend()
    



    
    # Plot temperature
    axes[4].plot(filtered_data['timestamp'], filtered_data['temperature'], label='Temperature', color='orange')
    axes[4].set_ylabel('Temperature (°C)')
    axes[4].set_title('Battery Temperature Over Time')
    axes[4].legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plots in Streamlit
    st.pyplot(fig)
    
    # Add Checkbox for Interactive Plot
    if st.checkbox("Show Interactive Plot"):
        st.subheader("Interactive Parameter Plots")

        # Create subplots for each parameter
        fig = go.Figure()

        # Add vbat (Battery Voltage)
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['vbat'],
            mode='lines+markers',
            name='Battery Voltage (vbat)',
            hovertemplate="Time: %{x}<br>Voltage: %{y} V"
        ))

        # Add discharge_current
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['discharge_current'],
            mode='lines+markers',
            name='Discharge Current',
            hovertemplate="Time: %{x}<br>Discharge Current: %{y} A"
        ))

        # Add charge_current
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['charge_current'],
            mode='lines+markers',
            name='Charge Current',
            hovertemplate="Time: %{x}<br>Charge Current: %{y} A"
        ))

        # Add capacity_percentage
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['capacity_percentage'],
            mode='lines+markers',
            name='Capacity Percentage',
            hovertemplate="Time: %{x}<br>Capacity: %{y} %"
        ))

        # Add temperature
        fig.add_trace(go.Scatter(
            x=filtered_data['timestamp'],
            y=filtered_data['temperature'],
            mode='lines+markers',
            name='Temperature',
            hovertemplate="Time: %{x}<br>Temperature: %{y} °C"
        ))

        # Customize layout
        fig.update_layout(
            title="Battery Data Parameters Over Time",
            xaxis_title="Timestamp",
            yaxis_title="Values",
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Display the interactive plot
        st.plotly_chart(fig, use_container_width=True)

    # Display Filtered Data
    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    # Download Filtered Data
    st.subheader("Download Filtered Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download Filtered Data as CSV", data=csv, file_name="filtered_battery_data.csv", mime="text/csv")
