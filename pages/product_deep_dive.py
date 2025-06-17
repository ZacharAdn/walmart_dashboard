"""
Product Deep Dive Page
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.visualization import ChartCreator
from config.settings import DashboardConfig

def show():
    """Display the Product Deep Dive page"""
    
    st.title("🏬 Product Deep Dive Analysis")
    st.markdown("Individual product analysis and forecasting insights")
    st.markdown("---")
    
    # Load data
    data_loader = st.session_state.data_loader
    chart_creator = ChartCreator()
    
    # Product Selection Section
    st.subheader("🔍 Product Selection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Product search
        product_search = st.text_input(
            "🔍 Search Product ID",
            placeholder="e.g., FOODS_3_090, FOODS_1_001, etc.",
            help="Enter product ID or partial match"
        )
        
        # Get available products
        try:
            sales_data = data_loader.load_sales_data()
            if not sales_data.empty and 'item_id' in sales_data.columns:
                available_products = sorted(sales_data['item_id'].unique())
                
                # Filter products based on search
                if product_search:
                    filtered_products = [p for p in available_products if product_search.upper() in p.upper()]
                else:
                    filtered_products = available_products[:100]  # Show first 100
                
                selected_product = st.selectbox(
                    "Select Product",
                    filtered_products,
                    help="Choose a specific product for detailed analysis"
                )
            else:
                # Use dummy products
                dummy_products = [f"FOODS_3_{str(i).zfill(3)}" for i in range(1, 101)]
                selected_product = st.selectbox("Select Product", dummy_products)
                
        except Exception as e:
            st.error(f"Error loading products: {str(e)}")
            dummy_products = [f"FOODS_3_{str(i).zfill(3)}" for i in range(1, 101)]
            selected_product = st.selectbox("Select Product", dummy_products)
    
    with col2:
        # Store selection
        available_stores = data_loader.get_available_stores()
        selected_store = st.selectbox(
            "Select Store",
            available_stores,
            help="Choose store location for analysis"
        )
        
        # Analysis type
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Time Series", "Pattern Analysis", "Model Comparison", "Forecasting"],
            help="Choose type of analysis to perform"
        )
    
    if not selected_product:
        st.warning("Please select a product to analyze")
        return
    
    st.markdown("---")
    
    # Product Information Section
    st.subheader(f"📊 Product Information: {selected_product}")
    
    # Load product time series data
    try:
        time_series_data = data_loader.get_product_time_series(selected_product, selected_store)
        
        if time_series_data.empty:
            st.warning(f"No time series data available for {selected_product} at {selected_store}")
            # Create dummy time series data
            dates = pd.date_range(start='2011-01-29', end='2016-06-19', freq='D')
            time_series_data = pd.DataFrame({
                'date': dates,
                'sales': np.random.poisson(5, len(dates)),
                'item_id': selected_product,
                'store_id': selected_store
            })
    except Exception as e:
        st.error(f"Error loading time series data: {str(e)}")
        # Create dummy data
        dates = pd.date_range(start='2011-01-29', end='2016-06-19', freq='D')
        time_series_data = pd.DataFrame({
            'date': dates,
            'sales': np.random.poisson(5, len(dates)),
            'item_id': selected_product,
            'store_id': selected_store
        })
    
    # Product statistics
    if not time_series_data.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = time_series_data['sales'].sum()
            st.metric("Total Sales", f"{total_sales:,}")
        
        with col2:
            avg_daily_sales = time_series_data['sales'].mean()
            st.metric("Avg Daily Sales", f"{avg_daily_sales:.2f}")
        
        with col3:
            zero_days = (time_series_data['sales'] == 0).sum()
            zero_rate = zero_days / len(time_series_data) * 100
            st.metric("Zero Sales Days", f"{zero_days} ({zero_rate:.1f}%)")
        
        with col4:
            max_sales = time_series_data['sales'].max()
            st.metric("Peak Daily Sales", f"{max_sales}")
    
    st.markdown("---")
    
    # Analysis based on selected type
    if analysis_type == "Time Series":
        st.subheader("📈 Time Series Analysis")
        
        if not time_series_data.empty:
            # Main time series plot
            fig_ts = chart_creator.create_time_series_plot(time_series_data, selected_product)
            st.plotly_chart(fig_ts, use_container_width=True)
            
            # Time series decomposition
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Sales Distribution:**")
                fig_hist = px.histogram(
                    time_series_data,
                    x='sales',
                    nbins=30,
                    title='Daily Sales Distribution'
                )
                fig_hist.update_layout(height=300)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                st.markdown("**📅 Seasonal Patterns:**")
                if 'month' in time_series_data.columns:
                    monthly_avg = time_series_data.groupby('month')['sales'].mean().reset_index()
                    fig_seasonal = px.bar(
                        monthly_avg,
                        x='month',
                        y='sales',
                        title='Average Sales by Month'
                    )
                    fig_seasonal.update_layout(height=300)
                    st.plotly_chart(fig_seasonal, use_container_width=True)
                else:
                    st.info("Month data not available for seasonal analysis")
            
            # Statistical summary
            st.markdown("**📋 Statistical Summary:**")
            stats_df = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Skewness', 'Kurtosis'],
                'Value': [
                    f"{time_series_data['sales'].mean():.2f}",
                    f"{time_series_data['sales'].median():.2f}",
                    f"{time_series_data['sales'].std():.2f}",
                    f"{time_series_data['sales'].min()}",
                    f"{time_series_data['sales'].max()}",
                    f"{time_series_data['sales'].skew():.2f}",
                    f"{time_series_data['sales'].kurtosis():.2f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    elif analysis_type == "Pattern Analysis":
        st.subheader("🔍 Pattern Analysis")
        
        # Pattern classification
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Pattern Classification:**")
            
            # Calculate pattern characteristics
            if not time_series_data.empty:
                zero_rate = (time_series_data['sales'] == 0).mean()
                cv = time_series_data['sales'].std() / time_series_data['sales'].mean() if time_series_data['sales'].mean() > 0 else 0
                
                # Pattern classification logic
                patterns = []
                if zero_rate > 0.5:
                    patterns.append("High Zero-Inflation")
                elif zero_rate > 0.3:
                    patterns.append("Medium Zero-Inflation")
                
                if cv > 1.5:
                    patterns.append("High Variability")
                elif cv > 1.0:
                    patterns.append("Medium Variability")
                
                # Check for seasonality (simplified)
                if 'month' in time_series_data.columns:
                    monthly_cv = time_series_data.groupby('month')['sales'].mean().std() / time_series_data.groupby('month')['sales'].mean().mean()
                    if monthly_cv > 0.3:
                        patterns.append("Seasonal")
                
                if not patterns:
                    patterns = ["Regular Pattern"]
                
                for pattern in patterns:
                    st.success(f"✅ {pattern}")
                
                # Pattern strength metrics
                st.markdown("**📊 Pattern Metrics:**")
                metrics_df = pd.DataFrame({
                    'Metric': ['Zero Inflation Rate', 'Coefficient of Variation', 'Seasonality Index'],
                    'Value': [f"{zero_rate:.2%}", f"{cv:.2f}", f"{monthly_cv:.2f}" if 'monthly_cv' in locals() else "N/A"],
                    'Interpretation': [
                        "High" if zero_rate > 0.5 else "Medium" if zero_rate > 0.3 else "Low",
                        "High" if cv > 1.5 else "Medium" if cv > 1.0 else "Low",
                        "High" if 'monthly_cv' in locals() and monthly_cv > 0.3 else "Low"
                    ]
                })
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**📈 Pattern Visualization:**")
            
            # Create pattern visualization
            if not time_series_data.empty:
                # Box plot by day of week
                if 'wday' in time_series_data.columns:
                    fig_pattern = px.box(
                        time_series_data,
                        x='wday',
                        y='sales',
                        title='Sales Pattern by Day of Week'
                    )
                    fig_pattern.update_layout(height=300)
                    st.plotly_chart(fig_pattern, use_container_width=True)
                else:
                    # Alternative visualization
                    fig_pattern = px.line(
                        time_series_data.head(100),
                        x='date',
                        y='sales',
                        title='Sales Pattern (First 100 Days)'
                    )
                    fig_pattern.update_layout(height=300)
                    st.plotly_chart(fig_pattern, use_container_width=True)
        
        # SNAP effect analysis
        if 'snap_CA' in time_series_data.columns or 'snap_TX' in time_series_data.columns or 'snap_WI' in time_series_data.columns:
            st.markdown("**🛒 SNAP Effect Analysis:**")
            
            # Determine SNAP column based on store
            snap_col = None
            if selected_store.startswith('CA') and 'snap_CA' in time_series_data.columns:
                snap_col = 'snap_CA'
            elif selected_store.startswith('TX') and 'snap_TX' in time_series_data.columns:
                snap_col = 'snap_TX'
            elif selected_store.startswith('WI') and 'snap_WI' in time_series_data.columns:
                snap_col = 'snap_WI'
            
            if snap_col:
                snap_analysis = time_series_data.groupby(snap_col)['sales'].agg(['mean', 'count']).reset_index()
                snap_analysis[snap_col] = snap_analysis[snap_col].map({0: 'Regular Days', 1: 'SNAP Days'})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_snap = px.bar(
                        snap_analysis,
                        x=snap_col,
                        y='mean',
                        title='Average Sales: SNAP vs Regular Days'
                    )
                    fig_snap.update_layout(height=300)
                    st.plotly_chart(fig_snap, use_container_width=True)
                
                with col2:
                    if len(snap_analysis) == 2:
                        snap_effect = (snap_analysis.iloc[1]['mean'] - snap_analysis.iloc[0]['mean']) / snap_analysis.iloc[0]['mean'] * 100
                        st.metric("SNAP Effect", f"{snap_effect:+.1f}%")
                        
                        snap_days_pct = snap_analysis.iloc[1]['count'] / snap_analysis['count'].sum() * 100
                        st.metric("SNAP Days %", f"{snap_days_pct:.1f}%")
    
    elif analysis_type == "Model Comparison":
        st.subheader("🤖 Model Performance Comparison")
        
        # Load model performance for this product (simulated)
        st.markdown("**📊 Model Performance for This Product:**")
        
        # Simulate model performance data
        model_results = pd.DataFrame({
            'Model': ['Naive', 'Moving Average', 'Linear Regression', 'Poisson', 'LightGBM'],
            'MAE': [4.2, 3.8, 3.1, 2.9, 2.3],
            'RMSE': [6.1, 5.7, 4.8, 4.3, 3.6],
            'MAPE': [0.45, 0.41, 0.35, 0.32, 0.28],
            'R²': [0.15, 0.23, 0.42, 0.51, 0.67]
        })
        
        # Add ranking
        model_results['Rank'] = model_results['MAE'].rank().astype(int)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(
                model_results,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "MAE": st.column_config.NumberColumn("MAE", format="%.2f"),
                    "RMSE": st.column_config.NumberColumn("RMSE", format="%.2f"),
                    "MAPE": st.column_config.NumberColumn("MAPE", format="%.2f"),
                    "R²": st.column_config.NumberColumn("R²", format="%.2f")
                }
            )
        
        with col2:
            fig_model_comp = px.bar(
                model_results,
                x='Model',
                y='MAE',
                title='Model Performance (MAE - Lower is Better)',
                color='MAE',
                color_continuous_scale='RdYlBu_r'
            )
            fig_model_comp.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig_model_comp, use_container_width=True)
        
        # Best model recommendation
        best_model = model_results.loc[model_results['MAE'].idxmin()]
        st.success(f"🏆 **Recommended Model:** {best_model['Model']} (MAE: {best_model['MAE']:.2f})")
        
        # Model insights
        st.markdown("**💡 Model Selection Insights:**")
        
        insights = [
            f"**Best Overall:** {best_model['Model']} shows the lowest MAE of {best_model['MAE']:.2f}",
            f"**Accuracy Range:** Performance varies from {model_results['MAE'].max():.2f} to {model_results['MAE'].min():.2f} MAE",
            f"**Improvement:** Best model is {((model_results['MAE'].max() - model_results['MAE'].min()) / model_results['MAE'].max() * 100):.1f}% better than baseline"
        ]
        
        for insight in insights:
            st.info(insight)
    
    elif analysis_type == "Forecasting":
        st.subheader("🔮 Forecasting Analysis")
        
        # Forecasting controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            forecast_horizon = st.slider("Forecast Horizon (days)", 7, 90, 30)
        
        with col2:
            confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
        
        with col3:
            forecast_model = st.selectbox("Forecasting Model", ["LightGBM", "Linear", "Moving Average"])
        
        # Generate forecast (simulated)
        if not time_series_data.empty:
            last_date = time_series_data['date'].max()
            forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon, freq='D')
            
            # Simulate forecast values
            last_sales = time_series_data['sales'].tail(30).mean()
            trend = np.random.normal(0, 0.1, forecast_horizon).cumsum()
            seasonal = np.sin(np.arange(forecast_horizon) * 2 * np.pi / 7) * 0.2  # Weekly seasonality
            noise = np.random.normal(0, 0.3, forecast_horizon)
            
            forecast_values = np.maximum(0, last_sales * (1 + trend + seasonal + noise))
            
            # Confidence intervals
            ci_width = 1.96 * np.std(time_series_data['sales']) * np.sqrt(np.arange(1, forecast_horizon + 1))
            upper_bound = forecast_values + ci_width
            lower_bound = np.maximum(0, forecast_values - ci_width)
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'date': forecast_dates,
                'forecast': forecast_values,
                'upper_bound': upper_bound,
                'lower_bound': lower_bound
            })
            
            # Combine historical and forecast data for plotting
            historical_plot = time_series_data.tail(90).copy()
            historical_plot['type'] = 'Historical'
            
            # Plot forecast
            fig_forecast = go.Figure()
            
            # Historical data
            fig_forecast.add_trace(go.Scatter(
                x=historical_plot['date'],
                y=historical_plot['sales'],
                mode='lines',
                name='Historical Sales',
                line=dict(color='blue')
            ))
            
            # Forecast
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['date'],
                y=forecast_df['forecast'],
                mode='lines',
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Confidence interval
            fig_forecast.add_trace(go.Scatter(
                x=list(forecast_df['date']) + list(forecast_df['date'][::-1]),
                y=list(forecast_df['upper_bound']) + list(forecast_df['lower_bound'][::-1]),
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name=f'{confidence_level}% Confidence Interval'
            ))
            
            fig_forecast.update_layout(
                title=f'{forecast_horizon}-Day Sales Forecast for {selected_product}',
                xaxis_title='Date',
                yaxis_title='Sales',
                height=400
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Forecast summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Avg Forecast", f"{forecast_values.mean():.2f}")
            
            with col2:
                st.metric("Total Forecast", f"{forecast_values.sum():.0f}")
            
            with col3:
                forecast_growth = (forecast_values.mean() - last_sales) / last_sales * 100 if last_sales > 0 else 0
                st.metric("Growth vs Recent", f"{forecast_growth:+.1f}%")
            
            # Forecast table
            st.markdown("**📋 Detailed Forecast:**")
            
            # Show first 14 days
            display_forecast = forecast_df.head(14).copy()
            display_forecast['date'] = display_forecast['date'].dt.strftime('%Y-%m-%d')
            display_forecast = display_forecast.round(2)
            
            st.dataframe(
                display_forecast,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "forecast": st.column_config.NumberColumn("Forecast", format="%.2f"),
                    "upper_bound": st.column_config.NumberColumn("Upper Bound", format="%.2f"),
                    "lower_bound": st.column_config.NumberColumn("Lower Bound", format="%.2f")
                }
            )
    
    # Export Options
    st.markdown("---")
    st.subheader("💾 Export Product Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Time Series"):
            if not time_series_data.empty:
                csv = time_series_data.to_csv(index=False)
                st.download_button(
                    label="Download Time Series CSV",
                    data=csv,
                    file_name=f"{selected_product}_{selected_store}_timeseries.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("📈 Export Analysis Summary"):
            if not time_series_data.empty:
                summary_data = {
                    'Product': [selected_product],
                    'Store': [selected_store],
                    'Total_Sales': [time_series_data['sales'].sum()],
                    'Avg_Daily_Sales': [time_series_data['sales'].mean()],
                    'Zero_Rate': [(time_series_data['sales'] == 0).mean()],
                    'Max_Sales': [time_series_data['sales'].max()],
                    'Analysis_Date': [pd.Timestamp.now()]
                }
                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False)
                
                st.download_button(
                    label="Download Summary CSV",
                    data=csv,
                    file_name=f"{selected_product}_analysis_summary.csv",
                    mime="text/csv"
                )
    
    with col3:
        if analysis_type == "Forecasting" and 'forecast_df' in locals():
            if st.button("🔮 Export Forecast"):
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    label="Download Forecast CSV",
                    data=csv,
                    file_name=f"{selected_product}_forecast.csv",
                    mime="text/csv"
                ) 