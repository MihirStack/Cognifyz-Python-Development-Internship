import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Data Visualization Tool", layout="wide")

st.title("📊 Interactive Data Visualization Tool")
st.markdown("Upload your **CSV** file and choose how to visualize your data.")

# File Upload
uploaded_file = st.file_uploader("Upload CSV", type="csv")

# Main UI
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Dropdowns for plot config
        st.subheader("📈 Visualization Settings")
        chart_type = st.selectbox("Choose chart type", ["Bar", "Line", "Scatter", "Pie", "Histogram"])

        if chart_type == "Pie":
            label_col = st.selectbox("Select label column", df.columns)
            value_col = st.selectbox("Select value column", df.select_dtypes(include=['number']).columns)
        else:
            x_col = st.selectbox("X-axis", df.columns)
            y_col = st.selectbox("Y-axis", df.select_dtypes(include=['number']).columns)

        # Generate chart
        if st.button("Generate Chart"):
            st.subheader("📊 Output Visualization")

            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, title=f"{chart_type} Chart")
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, title=f"{chart_type} Chart")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{chart_type} Chart")
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_col, nbins=30, title="Histogram")
            elif chart_type == "Pie":
                fig = px.pie(df, names=label_col, values=value_col, title="Pie Chart")
            else:
                st.warning("Unsupported chart type selected.")

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📁 Please upload a CSV file to get started.")
