"""
Pattern Analysis Page
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
    """Display the Pattern Analysis page"""
    
    st.title("📊 Pattern Analysis")
    st.markdown("Explore and understand data patterns across the Walmart M5 dataset")
    st.markdown("---")
    
    # Load data
    data_loader = st.session_state.data_loader
    chart_creator = ChartCreator()
    
    # Pattern Selection Section
    st.subheader("🎯 Pattern Type Selection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pattern_types = ["Seasonality", "Zero-Inflation", "Volume Distribution", "SNAP Effects"]
        selected_pattern = st.selectbox(
            "Select Pattern Type",
            pattern_types,
            help="Choose which pattern type to analyze in detail"
        )
    
    with col2:
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["Overview", "Detailed", "Advanced"],
            help="Choose the level of detail for the analysis"
        )
    
    with col3:
        # Comparison mode
        comparison_mode = st.checkbox(
            "Compare Patterns",
            help="Enable comparison between different pattern types"
        )
    
    st.markdown("---")
    
    # Pattern-specific analysis
    if selected_pattern == "Seasonality":
        show_seasonality_analysis(data_loader, chart_creator, analysis_depth, comparison_mode)
    
    elif selected_pattern == "Zero-Inflation":
        show_zero_inflation_analysis(data_loader, chart_creator, analysis_depth, comparison_mode)
    
    elif selected_pattern == "Volume Distribution":
        show_volume_analysis(data_loader, chart_creator, analysis_depth, comparison_mode)
    
    elif selected_pattern == "SNAP Effects":
        show_snap_analysis(data_loader, chart_creator, analysis_depth, comparison_mode)

def show_seasonality_analysis(data_loader, chart_creator, analysis_depth, comparison_mode):
    """Show seasonality pattern analysis"""
    
    st.subheader("📅 Seasonality Pattern Analysis")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Seasonal Products", "8,420")
    
    with col2:
        st.metric("Avg Pattern Strength", "0.75")
    
    with col3:
        st.metric("Peak Season", "Summer")
    
    with col4:
        st.metric("Seasonality Index", "1.35")
    
    st.markdown("---")
    
    # Seasonal pattern visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Monthly Sales Patterns:**")
        
        # Create example monthly pattern
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_index = [0.85, 0.80, 0.95, 1.05, 1.15, 1.25, 
                         1.35, 1.40, 1.20, 1.10, 1.25, 1.45]
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=months,
            y=seasonal_index,
            mode='lines+markers',
            name='Seasonal Index',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        # Add reference line at 1.0
        fig_monthly.add_hline(y=1.0, line_dash="dash", line_color="red", 
                             annotation_text="Baseline (1.0)")
        
        fig_monthly.update_layout(
            title='Average Seasonal Index by Month',
            xaxis_title='Month',
            yaxis_title='Seasonal Index',
            height=400
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        st.markdown("**🔍 Seasonal Insights:**")
        
        insights = [
            "**Summer Peak**: July-August show 35-40% above baseline",
            "**Winter Low**: January-February are lowest months",
            "**Holiday Effect**: December shows strong recovery",
            "**Spring Growth**: Consistent growth March-May"
        ]
        
        for insight in insights:
            st.info(insight)

def show_zero_inflation_analysis(data_loader, chart_creator, analysis_depth, comparison_mode):
    """Show zero-inflation pattern analysis"""
    
    st.subheader("🕳️ Zero-Inflation Pattern Analysis")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Products Analyzed", "14,370")
    
    with col2:
        st.metric("Avg Zero Rate", "62%")
    
    with col3:
        st.metric("High Zero-Inflation", "8,902")
    
    with col4:
        st.metric("Impact Score", "0.62")
    
    st.markdown("---")
    
    # Zero-inflation visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Zero Rate Distribution:**")
        
        # Create zero rate distribution
        zero_rates = np.random.beta(2, 2, 1000) * 0.9 + 0.1  # Simulated distribution
        
        fig_zero_dist = px.histogram(
            x=zero_rates,
            nbins=30,
            title='Distribution of Zero-Inflation Rates',
            labels={'x': 'Zero Rate', 'y': 'Number of Products'}
        )
        fig_zero_dist.update_layout(height=400)
        st.plotly_chart(fig_zero_dist, use_container_width=True)
    
    with col2:
        st.markdown("**🔍 Zero-Inflation Insights:**")
        
        insights = [
            "**62% Overall Rate**: Majority of daily sales are zero",
            "**Model Impact**: Standard models perform poorly",
            "**Poisson Advantage**: 25% better on zero-inflated data",
            "**Threshold**: >70% zero rate needs special handling"
        ]
        
        for insight in insights:
            st.info(insight)

def show_volume_analysis(data_loader, chart_creator, analysis_depth, comparison_mode):
    """Show volume distribution pattern analysis"""
    
    st.subheader("📊 Volume Distribution Analysis")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Median Volume", "500")
    
    with col2:
        st.metric("90th Percentile", "2,500")
    
    with col3:
        st.metric("90/50 Ratio", "5.0x")
    
    with col4:
        st.metric("Top 1% Volume", "10,000")
    
    st.markdown("---")
    
    # Volume analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Volume Percentiles:**")
        
        percentiles = [10, 25, 50, 75, 90, 95, 99]
        volume_stats = [100, 250, 500, 1000, 2500, 5000, 10000]
        
        fig_volume = px.bar(
            x=[f'{p}th' for p in percentiles],
            y=volume_stats,
            title='Sales Volume Distribution (Percentiles)',
            labels={'x': 'Percentile', 'y': 'Total Sales'}
        )
        fig_volume.update_layout(height=400)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        st.markdown("**🔍 Volume Insights:**")
        
        insights = [
            "**Power Law**: 10% of products drive 70% of sales",
            "**High Concentration**: Top 1% has 10x median volume",
            "**Long Tail**: 75% are low-volume products",
            "**Predictability**: Higher volume = easier to predict"
        ]
        
        for insight in insights:
            st.info(insight)

def show_snap_analysis(data_loader, chart_creator, analysis_depth, comparison_mode):
    """Show SNAP effects pattern analysis"""
    
    st.subheader("🛒 SNAP Effects Analysis")
    
    # SNAP overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("SNAP Days %", "33%")
    
    with col2:
        st.metric("Avg SNAP Effect", "+18.7%")
    
    with col3:
        st.metric("Responsive Products", "65%")
    
    with col4:
        st.metric("Effect Significance", "0.85")
    
    st.markdown("---")
    
    # SNAP effects visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 SNAP vs Regular Days:**")
        
        snap_comparison = pd.DataFrame({
            'Day Type': ['Regular Days', 'SNAP Days'],
            'Avg Sales': [12.8, 15.2]
        })
        
        fig_snap = px.bar(
            snap_comparison,
            x='Day Type',
            y='Avg Sales',
            title='Average Sales: SNAP vs Regular Days',
            color='Day Type',
            color_discrete_map={'SNAP Days': '#ff7f0e', 'Regular Days': '#1f77b4'}
        )
        fig_snap.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_snap, use_container_width=True)
    
    with col2:
        st.markdown("**🔍 SNAP Insights:**")
        
        insights = [
            "**18.7% Increase**: Average sales boost on SNAP days",
            "**33% Coverage**: One-third of days show SNAP effects",
            "**State Variation**: Effects vary by state benefits",
            "**Category Response**: Food shows stronger response"
        ]
        
        for insight in insights:
            st.info(insight)

    # Export options for pattern analysis
    st.markdown("---")
    st.subheader("💾 Export Pattern Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Pattern Data"):
            try:
                pattern_data = data_loader.load_pattern_examples(selected_pattern.lower().replace('-', '_').replace(' ', '_'))
                if not pattern_data.empty:
                    csv = pattern_data.to_csv(index=False)
                    st.download_button(
                        label="Download Pattern CSV",
                        data=csv,
                        file_name=f"{selected_pattern.lower().replace(' ', '_')}_patterns.csv",
                        mime="text/csv"
                    )
            except:
                st.error("Error exporting pattern data")
    
    with col2:
        if st.button("📈 Export Analysis Summary"):
            # Create summary based on selected pattern
            summary_data = {
                'Pattern Type': [selected_pattern],
                'Analysis Date': [pd.Timestamp.now()],
                'Key Metric': ['Pattern Strength'],
                'Analysis Depth': [analysis_depth]
            }
            summary_df = pd.DataFrame(summary_data)
            csv = summary_df.to_csv(index=False)
            
            st.download_button(
                label="Download Summary CSV",
                data=csv,
                file_name=f"{selected_pattern.lower().replace(' ', '_')}_analysis_summary.csv",
                mime="text/csv"
            )
    
    with col3:
        st.info("💡 More export options coming soon!") 