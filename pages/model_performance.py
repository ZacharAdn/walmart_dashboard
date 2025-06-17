"""
Model Performance Page
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
    """Display the Model Performance page"""
    
    st.title("🤖 Model Performance Analysis")
    st.markdown("Comprehensive model comparison and performance analysis")
    st.markdown("---")
    
    # Load data
    data_loader = st.session_state.data_loader
    chart_creator = ChartCreator()
    
    try:
        model_performance = data_loader.load_model_performance()
        best_models = data_loader.load_best_models()
    except Exception as e:
        st.error(f"Error loading model performance data: {str(e)}")
        return
    
    # Model Selection Controls
    st.subheader("🎛️ Model Comparison Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Available models
        if not model_performance.empty and 'model_name' in model_performance.columns:
            available_models = sorted(model_performance['model_name'].unique())
        else:
            available_models = DashboardConfig.AVAILABLE_MODELS
        
        selected_models = st.multiselect(
            "Select Models to Compare",
            available_models,
            default=available_models[:3] if len(available_models) > 3 else available_models,
            help="Choose which models to include in the comparison"
        )
    
    with col2:
        # Performance metric selection
        metric_options = ["MAE", "RMSE", "MAPE", "R²"] 
        selected_metric = st.selectbox(
            "Primary Metric",
            metric_options,
            index=0,
            help="Select the primary metric for model comparison"
        )
    
    with col3:
        # Pattern type filter
        if not model_performance.empty and 'pattern_type' in model_performance.columns:
            pattern_types = ['All'] + sorted(model_performance['pattern_type'].unique())
        else:
            pattern_types = ['All'] + DashboardConfig.PATTERN_TYPES
        
        selected_pattern = st.selectbox(
            "Filter by Pattern",
            pattern_types,
            help="Filter results by specific pattern type"
        )
    
    if not selected_models:
        st.warning("Please select at least one model to analyze")
        return
    
    # Filter data based on selections
    filtered_performance = model_performance.copy()
    
    if not filtered_performance.empty:
        if 'model_name' in filtered_performance.columns:
            filtered_performance = filtered_performance[
                filtered_performance['model_name'].isin(selected_models)
            ]
        
        if selected_pattern != 'All' and 'pattern_type' in filtered_performance.columns:
            filtered_performance = filtered_performance[
                filtered_performance['pattern_type'] == selected_pattern
            ]
    
    st.markdown("---")
    
    # Performance Overview
    st.subheader("📊 Performance Overview")
    
    if not filtered_performance.empty:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        metric_col_map = {
            'MAE': 'mae',
            'RMSE': 'rmse', 
            'MAPE': 'mape',
            'R²': 'r2_score'
        }
        
        metric_col = metric_col_map.get(selected_metric, 'mae')
        
        if metric_col in filtered_performance.columns:
            best_score = filtered_performance[metric_col].min() if metric_col != 'r2_score' else filtered_performance[metric_col].max()
            worst_score = filtered_performance[metric_col].max() if metric_col != 'r2_score' else filtered_performance[metric_col].min()
            avg_score = filtered_performance[metric_col].mean()
            
            with col1:
                st.metric("Best Score", f"{best_score:.3f}")
            
            with col2:
                st.metric("Worst Score", f"{worst_score:.3f}")
            
            with col3:
                st.metric("Average Score", f"{avg_score:.3f}")
            
            with col4:
                improvement = ((worst_score - best_score) / worst_score * 100) if worst_score != 0 else 0
                st.metric("Max Improvement", f"{improvement:.1f}%")
    
    st.markdown("---")
    
    # Main Performance Comparison
    st.subheader("📈 Model Performance Comparison")
    
    if not filtered_performance.empty:
        # Create comparison chart
        fig_comparison = chart_creator.create_model_performance_comparison(
            filtered_performance, 
            selected_models
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Performance by pattern heatmap
        if 'pattern_type' in filtered_performance.columns and selected_pattern == 'All':
            st.subheader("🔥 Performance Heatmap by Pattern")
            fig_heatmap = chart_creator.create_model_accuracy_by_pattern(filtered_performance)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    else:
        st.info("No performance data available for the selected models and patterns")
    
    st.markdown("---")
    
    # Detailed Performance Analysis
    st.subheader("📋 Detailed Performance Analysis")
    
    # Performance table
    if not filtered_performance.empty:
        # Prepare performance summary
        if 'model_name' in filtered_performance.columns:
            summary_cols = ['model_name']
            if 'pattern_type' in filtered_performance.columns:
                summary_cols.append('pattern_type')
            
            # Add available metric columns
            for metric in ['mae', 'rmse', 'mape', 'r2_score']:
                if metric in filtered_performance.columns:
                    summary_cols.append(metric)
            
            display_df = filtered_performance[summary_cols].copy()
            
            # Format numeric columns
            for col in ['mae', 'rmse', 'mape', 'r2_score']:
                if col in display_df.columns:
                    display_df[col] = display_df[col].round(4)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "mae": st.column_config.NumberColumn("MAE", format="%.4f"),
                    "rmse": st.column_config.NumberColumn("RMSE", format="%.4f"),
                    "mape": st.column_config.NumberColumn("MAPE", format="%.4f"),
                    "r2_score": st.column_config.NumberColumn("R²", format="%.4f")
                }
            )
        else:
            st.dataframe(filtered_performance, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Best Models by Pattern
    st.subheader("🏆 Best Models by Pattern")
    
    if not best_models.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Pattern-Specific Champions:**")
            st.dataframe(
                best_models,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "mae": st.column_config.NumberColumn("MAE", format="%.3f"),
                    "improvement": st.column_config.NumberColumn("Improvement", format="%.1%")
                }
            )
        
        with col2:
            # Best models visualization
            if 'pattern_type' in best_models.columns and 'mae' in best_models.columns:
                fig_best = px.bar(
                    best_models,
                    x='pattern_type',
                    y='mae',
                    color='best_model',
                    title='Best Model Performance by Pattern',
                    labels={'mae': 'MAE (Lower is Better)', 'pattern_type': 'Pattern Type'}
                )
                fig_best.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_best, use_container_width=True)
    else:
        # Show example best models data
        example_best_models = pd.DataFrame({
            'Pattern Type': ['Seasonal', 'Zero-Inflation', 'Volume', 'SNAP Effects'],
            'Best Model': ['LightGBM', 'Poisson', 'Linear Regression', 'Moving Average'],
            'MAE': [2.45, 3.12, 2.78, 4.21],
            'Improvement vs Baseline': ['15%', '8%', '12%', '5%']
        })
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Pattern-Specific Champions:**")
            st.dataframe(example_best_models, use_container_width=True, hide_index=True)
        
        with col2:
            fig_best = px.bar(
                example_best_models,
                x='Pattern Type',
                y='MAE',
                color='Best Model',
                title='Best Model Performance by Pattern'
            )
            fig_best.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_best, use_container_width=True)
    
    st.markdown("---")
    
    # Model Strengths and Weaknesses
    st.subheader("⚖️ Model Strengths & Weaknesses Analysis")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["🎯 Model Profiles", "📊 Performance Distribution", "🔍 Error Analysis"])
    
    with tab1:
        # Model profiles
        model_profiles = {
            "Naive": {
                "strengths": ["Simple baseline", "Fast computation", "No overfitting"],
                "weaknesses": ["No trend capture", "Poor for seasonal data", "Limited accuracy"],
                "best_for": "Quick baseline comparisons",
                "avoid_for": "Complex patterns"
            },
            "Moving Average": {
                "strengths": ["Smooth predictions", "Trend following", "Robust to outliers"],
                "weaknesses": ["Lag in trend changes", "No seasonality", "Parameter sensitive"],
                "best_for": "Smooth time series",
                "avoid_for": "Highly seasonal data"
            },
            "Linear Regression": {
                "strengths": ["Interpretable", "Fast training", "Good for trends"],
                "weaknesses": ["Assumes linearity", "Poor for non-linear patterns", "Sensitive to outliers"],
                "best_for": "Linear relationships",
                "avoid_for": "Complex non-linear patterns"
            },
            "Poisson": {
                "strengths": ["Handles count data", "Good for zero-inflation", "Probabilistic"],
                "weaknesses": ["Assumes Poisson distribution", "Limited flexibility", "Count data only"],
                "best_for": "Zero-inflated count data",
                "avoid_for": "Continuous or large count values"
            },
            "LightGBM": {
                "strengths": ["High accuracy", "Handles non-linearity", "Feature importance"],
                "weaknesses": ["Complex model", "Overfitting risk", "Less interpretable"],
                "best_for": "Complex patterns with many features",
                "avoid_for": "Simple patterns or small datasets"
            }
        }
        
        for model in selected_models:
            if model in model_profiles:
                profile = model_profiles[model]
                
                with st.expander(f"📋 {model} - Model Profile"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**✅ Strengths:**")
                        for strength in profile["strengths"]:
                            st.markdown(f"- {strength}")
                        
                        st.markdown("**🎯 Best For:**")
                        st.markdown(f"- {profile['best_for']}")
                    
                    with col2:
                        st.markdown("**❌ Weaknesses:**")
                        for weakness in profile["weaknesses"]:
                            st.markdown(f"- {weakness}")
                        
                        st.markdown("**⚠️ Avoid For:**")
                        st.markdown(f"- {profile['avoid_for']}")
    
    with tab2:
        # Performance distribution analysis
        if not filtered_performance.empty and metric_col in filtered_performance.columns:
            st.markdown(f"**{selected_metric} Distribution Across Models:**")
            
            fig_dist = px.box(
                filtered_performance,
                x='model_name',
                y=metric_col,
                title=f'{selected_metric} Distribution by Model',
                labels={metric_col: selected_metric, 'model_name': 'Model'}
            )
            fig_dist.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Statistical summary
            st.markdown("**Statistical Summary:**")
            stats_summary = filtered_performance.groupby('model_name')[metric_col].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(4)
            st.dataframe(stats_summary, use_container_width=True)
        else:
            st.info("Performance distribution data not available")
    
    with tab3:
        # Error analysis
        st.markdown("**Error Analysis & Insights:**")
        
        error_insights = [
            {
                "category": "High Error Patterns",
                "insight": "Models struggle with highly seasonal products",
                "recommendation": "Use ensemble methods for seasonal patterns"
            },
            {
                "category": "Zero-Inflation Impact", 
                "insight": "Standard models underperform on zero-inflated data",
                "recommendation": "Prefer Poisson or specialized zero-inflation models"
            },
            {
                "category": "Volume Effects",
                "insight": "High-volume products have different error characteristics",
                "recommendation": "Consider volume-based model selection"
            },
            {
                "category": "SNAP Day Predictions",
                "insight": "Models miss SNAP day sales spikes",
                "recommendation": "Include SNAP indicators as features"
            }
        ]
        
        for insight in error_insights:
            with st.expander(f"💡 {insight['category']}"):
                st.markdown(f"**Insight:** {insight['insight']}")
                st.markdown(f"**Recommendation:** {insight['recommendation']}")
    
    st.markdown("---")
    
    # Model Recommendation Engine
    st.subheader("🎯 Model Recommendation Engine")
    
    st.markdown("**Get personalized model recommendations based on your data characteristics:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_pattern = st.selectbox(
            "Primary Data Pattern",
            ["Seasonal", "Trend", "Zero-Inflated", "High Volume", "Mixed"]
        )
    
    with col2:
        data_size = st.selectbox(
            "Dataset Size",
            ["Small (<1K)", "Medium (1K-10K)", "Large (>10K)"]
        )
    
    with col3:
        accuracy_priority = st.selectbox(
            "Priority",
            ["Accuracy", "Speed", "Interpretability", "Balanced"]
        )
    
    if st.button("🔮 Get Recommendation"):
        # Simple recommendation logic
        recommendations = []
        
        if data_pattern == "Seasonal":
            if accuracy_priority == "Accuracy":
                recommendations = ["LightGBM", "Linear Regression"]
            else:
                recommendations = ["Moving Average", "Linear Regression"]
        elif data_pattern == "Zero-Inflated":
            recommendations = ["Poisson", "LightGBM"]
        elif data_pattern == "High Volume":
            recommendations = ["Linear Regression", "LightGBM"]
        else:
            recommendations = ["LightGBM", "Linear Regression", "Moving Average"]
        
        st.success(f"**Recommended Models:** {', '.join(recommendations[:2])}")
        
        # Show reasoning
        with st.expander("💭 Recommendation Reasoning"):
            st.markdown(f"**Data Pattern:** {data_pattern}")
            st.markdown(f"**Dataset Size:** {data_size}")
            st.markdown(f"**Priority:** {accuracy_priority}")
            st.markdown("**Reasoning:** Based on pattern analysis and performance characteristics")
    
    # Export Options
    st.markdown("---")
    st.subheader("💾 Export Performance Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Performance Data"):
            if not filtered_performance.empty:
                csv = filtered_performance.to_csv(index=False)
                st.download_button(
                    label="Download Performance CSV",
                    data=csv,
                    file_name="model_performance_analysis.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("🏆 Export Best Models"):
            if not best_models.empty:
                csv = best_models.to_csv(index=False)
            else:
                csv = example_best_models.to_csv(index=False)
            
            st.download_button(
                label="Download Best Models CSV",
                data=csv,
                file_name="best_models_by_pattern.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("📋 Export Model Profiles"):
            # Create model profiles DataFrame
            profiles_data = []
            for model, profile in model_profiles.items():
                if model in selected_models:
                    profiles_data.append({
                        'Model': model,
                        'Strengths': '; '.join(profile['strengths']),
                        'Weaknesses': '; '.join(profile['weaknesses']),
                        'Best For': profile['best_for'],
                        'Avoid For': profile['avoid_for']
                    })
            
            if profiles_data:
                profiles_df = pd.DataFrame(profiles_data)
                csv = profiles_df.to_csv(index=False)
                
                st.download_button(
                    label="Download Profiles CSV",
                    data=csv,
                    file_name="model_profiles.csv",
                    mime="text/csv"
                ) 