"""
Data Explorer Page
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.visualization import ChartCreator
from config.settings import DashboardConfig

def show():
    """Display the Data Explorer page"""
    
    st.title("📈 Data Explorer")
    st.markdown("Interactive exploration of Walmart M5 data")
    st.markdown("---")
    
    # Load data
    data_loader = st.session_state.data_loader
    chart_creator = ChartCreator()
    
    # Dataset Selection
    st.subheader("📊 Dataset Selection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dataset_options = [
            "Calendar Data",
            "Sales Data (Training)",
            "Sales Data (Evaluation)", 
            "Pricing Data",
            "Test Results",
            "Model Performance"
        ]
        
        selected_dataset = st.selectbox(
            "Choose Dataset to Explore",
            dataset_options,
            help="Select which dataset you want to explore in detail"
        )
    
    with col2:
        # Data refresh button
        if st.button("🔄 Refresh Data", help="Reload data from source"):
            data_loader.clear_cache()
            st.rerun()
    
    # Load selected dataset
    try:
        if selected_dataset == "Calendar Data":
            df = data_loader.load_calendar()
            st.subheader("📅 Calendar Data Overview")
            
        elif selected_dataset == "Sales Data (Training)":
            df = data_loader.load_sales_data(evaluation=False)
            st.subheader("🛒 Sales Training Data Overview")
            
        elif selected_dataset == "Sales Data (Evaluation)":
            df = data_loader.load_sales_data(evaluation=True)
            st.subheader("🛒 Sales Evaluation Data Overview")
            
        elif selected_dataset == "Pricing Data":
            df = data_loader.load_prices_data()
            st.subheader("💰 Pricing Data Overview")
            
        elif selected_dataset == "Test Results":
            df = data_loader.load_test_results()
            st.subheader("🔍 Test Results Overview")
            
        elif selected_dataset == "Model Performance":
            df = data_loader.load_model_performance()
            st.subheader("🤖 Model Performance Overview")
        
        if df.empty:
            st.info("No data available for the selected dataset")
            return
            
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return
    
    # Dataset Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{len(df):,}")
    
    with col2:
        st.metric("Columns", len(df.columns))
    
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        st.metric("Numeric Columns", len(numeric_cols))
    
    with col4:
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("Memory Usage", f"{memory_usage:.1f} MB")
    
    st.markdown("---")
    
    # Interactive Filtering
    st.subheader("🔧 Interactive Filtering")
    
    # Create filters based on dataset type
    filtered_df = df.copy()
    
    if selected_dataset in ["Sales Data (Training)", "Sales Data (Evaluation)"]:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'store_id' in df.columns:
                stores = sorted(df['store_id'].unique())
                selected_stores = st.multiselect(
                    "Select Stores",
                    stores,
                    default=stores[:3] if len(stores) > 3 else stores
                )
                if selected_stores:
                    filtered_df = filtered_df[filtered_df['store_id'].isin(selected_stores)]
        
        with col2:
            if 'dept_id' in df.columns:
                departments = sorted(df['dept_id'].unique())
                selected_depts = st.multiselect(
                    "Select Departments",
                    departments,
                    default=departments[:2] if len(departments) > 2 else departments
                )
                if selected_depts:
                    filtered_df = filtered_df[filtered_df['dept_id'].isin(selected_depts)]
        
        with col3:
            # Sample size control
            max_rows = len(filtered_df)
            sample_size = st.slider(
                "Sample Size",
                min_value=100,
                max_value=min(max_rows, 10000),
                value=min(1000, max_rows),
                step=100,
                help="Number of rows to display for performance"
            )
            
            if sample_size < max_rows:
                filtered_df = filtered_df.sample(n=sample_size, random_state=42)
    
    elif selected_dataset == "Calendar Data":
        if 'date' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                min_date = df['date'].min().date()
                max_date = df['date'].max().date()
                
                date_range = st.date_input(
                    "Select Date Range",
                    value=[min_date, max_date],
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_df = filtered_df[
                        (filtered_df['date'].dt.date >= start_date) &
                        (filtered_df['date'].dt.date <= end_date)
                    ]
            
            with col2:
                if 'year' in df.columns:
                    years = sorted(df['year'].unique())
                    selected_years = st.multiselect(
                        "Select Years",
                        years,
                        default=years[-2:] if len(years) > 2 else years
                    )
                    if selected_years:
                        filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
    
    # Display filtered dataset info
    if len(filtered_df) != len(df):
        st.info(f"Showing {len(filtered_df):,} of {len(df):,} rows after filtering")
    
    st.markdown("---")
    
    # Data Preview
    st.subheader("👀 Data Preview")
    
    # Display options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_head = st.checkbox("Show First 10 Rows", value=True)
    
    with col2:
        show_tail = st.checkbox("Show Last 10 Rows", value=False)
    
    with col3:
        show_sample = st.checkbox("Show Random Sample", value=False)
    
    # Display data based on selection
    if show_head:
        st.markdown("**First 10 Rows:**")
        st.dataframe(filtered_df.head(10), use_container_width=True)
    
    if show_tail:
        st.markdown("**Last 10 Rows:**")
        st.dataframe(filtered_df.tail(10), use_container_width=True)
    
    if show_sample:
        st.markdown("**Random Sample (10 Rows):**")
        sample_df = filtered_df.sample(n=min(10, len(filtered_df)), random_state=42)
        st.dataframe(sample_df, use_container_width=True)
    
    st.markdown("---")
    
    # Statistical Summary
    st.subheader("📊 Statistical Summary")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Numeric Summary", "📝 Categorical Summary", "🔍 Missing Values"])
    
    with tab1:
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.markdown("**Numeric Columns Statistics:**")
            numeric_summary = filtered_df[numeric_cols].describe()
            st.dataframe(numeric_summary, use_container_width=True)
            
            # Distribution plots for numeric columns
            if len(numeric_cols) > 0:
                st.markdown("**Distribution Plots:**")
                
                selected_numeric_col = st.selectbox(
                    "Select column for distribution plot",
                    numeric_cols,
                    key="numeric_dist"
                )
                
                if selected_numeric_col:
                    fig = px.histogram(
                        filtered_df,
                        x=selected_numeric_col,
                        nbins=30,
                        title=f'Distribution of {selected_numeric_col}'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns found in the dataset")
    
    with tab2:
        categorical_cols = filtered_df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            st.markdown("**Categorical Columns Summary:**")
            
            for col in categorical_cols[:5]:  # Show first 5 categorical columns
                unique_values = filtered_df[col].nunique()
                st.markdown(f"**{col}:** {unique_values} unique values")
                
                if unique_values <= 20:  # Show value counts for columns with few unique values
                    value_counts = filtered_df[col].value_counts().head(10)
                    
                    # Create bar chart
                    fig = px.bar(
                        x=value_counts.index,
                        y=value_counts.values,
                        title=f'Top Values in {col}',
                        labels={'x': col, 'y': 'Count'}
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"Too many unique values ({unique_values}) to display")
        else:
            st.info("No categorical columns found in the dataset")
    
    with tab3:
        # Missing values analysis
        missing_data = filtered_df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) > 0:
            st.markdown("**Columns with Missing Values:**")
            
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing Percentage': (missing_data.values / len(filtered_df) * 100).round(2)
            })
            
            st.dataframe(missing_df, use_container_width=True, hide_index=True)
            
            # Visualization of missing data
            if len(missing_data) <= 20:
                fig = px.bar(
                    missing_df,
                    x='Column',
                    y='Missing Percentage',
                    title='Missing Data by Column (%)',
                    labels={'Missing Percentage': 'Missing %'}
                )
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No missing values found in the dataset!")
    
    st.markdown("---")
    
    # Advanced Visualizations
    st.subheader("📈 Advanced Visualizations")
    
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["🔗 Correlations", "📊 Time Series", "🎯 Custom Plot"])
    
    with viz_tab1:
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            st.markdown("**Correlation Analysis:**")
            
            # Select columns for correlation
            selected_corr_cols = st.multiselect(
                "Select columns for correlation analysis",
                numeric_cols,
                default=list(numeric_cols[:5]) if len(numeric_cols) >= 5 else list(numeric_cols)
            )
            
            if len(selected_corr_cols) >= 2:
                corr_matrix = filtered_df[selected_corr_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    title='Correlation Matrix',
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Select at least 2 columns for correlation analysis")
        else:
            st.info("Need at least 2 numeric columns for correlation analysis")
    
    with viz_tab2:
        # Time series visualization
        date_cols = []
        for col in filtered_df.columns:
            if 'date' in col.lower() or filtered_df[col].dtype == 'datetime64[ns]':
                date_cols.append(col)
        
        if date_cols:
            st.markdown("**Time Series Analysis:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_date_col = st.selectbox("Select Date Column", date_cols)
            
            with col2:
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    selected_value_col = st.selectbox("Select Value Column", numeric_cols)
                else:
                    selected_value_col = None
            
            if selected_date_col and selected_value_col:
                # Create time series plot
                ts_data = filtered_df[[selected_date_col, selected_value_col]].dropna()
                
                if len(ts_data) > 0:
                    fig = px.line(
                        ts_data,
                        x=selected_date_col,
                        y=selected_value_col,
                        title=f'{selected_value_col} over Time'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected columns")
        else:
            st.info("No date columns found for time series analysis")
    
    with viz_tab3:
        st.markdown("**Custom Plot Builder:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            plot_type = st.selectbox(
                "Plot Type",
                ["Scatter", "Bar", "Box", "Violin", "Histogram"]
            )
        
        with col2:
            all_cols = list(filtered_df.columns)
            x_col = st.selectbox("X-axis", all_cols, key="custom_x")
        
        with col3:
            y_col = st.selectbox("Y-axis", all_cols, key="custom_y")
        
        # Color column (optional)
        color_col = st.selectbox(
            "Color by (optional)",
            ["None"] + all_cols,
            key="custom_color"
        )
        
        if x_col and y_col:
            try:
                color_param = None if color_col == "None" else color_col
                
                if plot_type == "Scatter":
                    fig = px.scatter(filtered_df, x=x_col, y=y_col, color=color_param)
                elif plot_type == "Bar":
                    fig = px.bar(filtered_df, x=x_col, y=y_col, color=color_param)
                elif plot_type == "Box":
                    fig = px.box(filtered_df, x=x_col, y=y_col, color=color_param)
                elif plot_type == "Violin":
                    fig = px.violin(filtered_df, x=x_col, y=y_col, color=color_param)
                elif plot_type == "Histogram":
                    fig = px.histogram(filtered_df, x=x_col, color=color_param)
                
                fig.update_layout(height=400, title=f'{plot_type} Plot: {x_col} vs {y_col}')
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating plot: {str(e)}")
    
    # Export Options
    st.markdown("---")
    st.subheader("💾 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_dataset.lower().replace(' ', '_')}_export.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Summary"):
            summary = filtered_df.describe()
            summary_csv = summary.to_csv()
            st.download_button(
                label="Download Summary",
                data=summary_csv,
                file_name=f"{selected_dataset.lower().replace(' ', '_')}_summary.csv",
                mime="text/csv"
            )
    
    with col3:
        st.info("💡 More export options coming soon!") 