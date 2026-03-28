import streamlit as st
import pandas as pd
import os
import plotly.express as px
from pathlib import Path
from frontend.layout import inject_css
# Setup path for imports
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(project_root))

from analytics.trend_analysis import aggregate_daily_trends, aggregate_category_time_series
from visualization.trend_charts import plot_sales_trend


def load_sales_data():
    """Load sales data with error handling."""
    sales_path = "data/processed/clean_sales.csv"
    
    try:
        if os.path.exists(sales_path):
            sales_df = pd.read_csv(sales_path)
            if not sales_df.empty:
                # Ensure date column is datetime
                if "date" in sales_df.columns:
                    sales_df["date"] = pd.to_datetime(sales_df["date"], errors="coerce")
                return sales_df
    except Exception as e:
        st.warning(f" Could not load sales data: {str(e)}")
    
    return None


def calculate_moving_average(data, column, window=7):
    """Calculate moving average for a column."""
    try:
        if column in data.columns:
            return data[column].rolling(window=window, min_periods=1).mean()
    except:
        pass
    return None


def show_trends():
    """Display sales trends and time-series analysis."""
    inject_css()
    
    # Page header
    st.markdown("""
    <div class='page-header'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            <div>
                <div class='page-header-title' style='margin: 0;'>Sales Trends & Analysis</div>
            </div>
        </div>
        <div class='page-header-subtitle'>Analyze sales patterns, trends, and seasonality over time</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    sales_df = load_sales_data()
    
    if sales_df is None or sales_df.empty:
        st.error("Cannot load sales data. Please upload CSV files first.")
        st.info("Go to Upload page to upload sales data.")
        return
    
    # ========== TIME RANGE METRICS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Time Period Overview</div>", unsafe_allow_html=True)
    
    try:
        if "date" in sales_df.columns:
            min_date = pd.to_datetime(sales_df["date"]).min()
            max_date = pd.to_datetime(sales_df["date"]).max()
            date_range = (max_date - min_date).days
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Date Range", f"{date_range} days")
            col2.metric("Total Revenue", f"₹ {sales_df['revenue'].sum():,.0f}")
            col3.metric("Total Units", f"{int(sales_df['quantity'].sum()):,}")
        else:
            st.warning("Date column not found")
    except Exception as e:
        st.warning(f"Error computing metrics: {str(e)}")
    
    st.divider()
    
    # ========== DAILY SALES TREND ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Daily Sales Trend</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Daily revenue and quantity movement</div>", unsafe_allow_html=True)
    
    try:
        if not sales_df.empty:
            daily_trend = aggregate_daily_trends(sales_df)
            
            if daily_trend is not None and not daily_trend.empty:
                # Plot using visualization function
                plot_sales_trend(daily_trend, chart_key="daily_sales_trend")
                
                # Statistics
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                col_stat1.metric("Avg Daily Revenue", f"₹ {daily_trend['revenue'].mean():,.0f}")
                col_stat2.metric("Peak Daily Revenue", f"₹ {daily_trend['revenue'].max():,.0f}")
                col_stat3.metric("Avg Daily Units", f"{daily_trend['quantity'].mean():.0f}")
            else:
                st.info("No daily trend data available")
        else:
            st.info("No sales data available")
    except Exception as e:
        st.warning(f"Could not generate daily trend: {str(e)}")
    
    st.divider()
    
    # ========== CATEGORY-WISE TREND ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Category-wise Revenue Trend</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Revenue breakdown by product category over time</div>", unsafe_allow_html=True)
    
    try:
        if "category" in sales_df.columns:
            category_trend = aggregate_category_time_series(sales_df)
            
            if category_trend and "data" in category_trend and len(category_trend["data"]) > 0:
                # Convert to DataFrame for easier plotting
                trend_df = pd.DataFrame(category_trend["data"])
                
                # Create Plotly figure
                fig = px.line(
                    trend_df,
                    x="date",
                    y=category_trend["categories"],
                    title="Revenue by Category Over Time",
                    markers=True,
                    labels={"value": "Revenue (₹)", "date": "Date"},
                )
                
                fig.update_layout(
                    hovermode="x unified",
                    template="plotly_white",
                    height=450,
                    margin=dict(l=50, r=50, t=80, b=80),
                )
                
                st.plotly_chart(fig, use_container_width=True, key="category_revenue_trend")
            else:
                st.info("No category trend data available")
        else:
            st.info("Category column not found in data")
    except Exception as e:
        st.warning(f" Could not generate category trend: {str(e)}")
    
    st.divider()
    
    # ========== MONTH-WISE SUMMARY ==========
    st.subheader(" Monthly Sales Summary")
    st.caption("Aggregated monthly performance")
    
    try:
        if "date" in sales_df.columns:
            sales_df_copy = sales_df.copy()
            sales_df_copy["date"] = pd.to_datetime(sales_df_copy["date"])
            sales_df_copy["year_month"] = sales_df_copy["date"].dt.to_period("M")
            
            monthly_summary = sales_df_copy.groupby("year_month").agg({
                "revenue": "sum",
                "quantity": "sum",
                "product": "nunique"
            }).reset_index()
            
            monthly_summary.columns = ["Month", "Revenue (₹)", "Quantity", "Unique Products"]
            monthly_summary["Month"] = monthly_summary["Month"].astype(str)
            
            # Chart
            fig = px.bar(
                monthly_summary,
                x="Month",
                y="Revenue (₹)",
                title="Monthly Revenue",
                color="Revenue (₹)",
                color_continuous_scale="Greens",
                text="Revenue (₹)"
            )
            
            fig.update_traces(texttemplate="₹ %{text:,.0f}", textposition="outside")
            fig.update_layout(
                template="plotly_white",
                height=400,
                showlegend=False,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True, key="monthly_revenue_summary")
            
            # Table
            with st.expander(" Monthly Details", expanded=False):
                display_monthly = monthly_summary.copy()
                display_monthly["Revenue (₹)"] = display_monthly["Revenue (₹)"].apply(lambda x: f"₹ {x:,.2f}")
                st.dataframe(display_monthly, use_container_width=True, hide_index=True, key="monthly_summary_table")
        else:
            st.warning(" Date column not found")
    except Exception as e:
        st.warning(f" Could not generate monthly summary: {str(e)}")
    
    st.divider()
    
    # ========== INTERACTIVE FILTERS ==========
    st.subheader(" Custom Analysis")
    st.caption("Filter and analyze specific segments")
    
    try:
        col_filter1, col_filter2 = st.columns(2)
        
        # Category filter
        with col_filter1:
            if "category" in sales_df.columns:
                categories = sales_df["category"].unique()
                selected_categories = st.multiselect(
                    "Filter by Category",
                    options=categories,
                    default=list(categories)[:3] if len(categories) > 0 else [],
                    key="category_filter"
                )
            else:
                selected_categories = []
                st.info("Category column not found")
        
        # Date range filter
        with col_filter2:
            if "date" in sales_df.columns:
                min_date = pd.to_datetime(sales_df["date"]).min()
                max_date = pd.to_datetime(sales_df["date"]).max()
                
                date_range = st.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_range_filter"
                )
            else:
                date_range = None
        
        # Apply filters
        filtered_df = sales_df.copy()
        
        if selected_categories and "category" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
        
        if date_range and len(date_range) == 2 and "date" in filtered_df.columns:
            filtered_df["date"] = pd.to_datetime(filtered_df["date"])
            filtered_df = filtered_df[
                (filtered_df["date"].dt.date >= date_range[0]) &
                (filtered_df["date"].dt.date <= date_range[1])
            ]
        
        # Display filtered results
        if not filtered_df.empty:
            col_f1, col_f2, col_f3 = st.columns(3)
            col_f1.metric(" Records", len(filtered_df))
            col_f2.metric(" Revenue", f"₹ {filtered_df['revenue'].sum():,.0f}")
            col_f3.metric(" Quantity", f"{int(filtered_df['quantity'].sum()):,}")
            
            # Chart
            filtered_daily = aggregate_daily_trends(filtered_df)
            if filtered_daily is not None and not filtered_daily.empty:
                st.markdown("#### Filtered Period Trend")
                plot_sales_trend(filtered_daily, chart_key="filtered_period_trend")
        else:
            st.warning("No data matches the selected filters")
    
    except Exception as e:
        st.warning(f" Error in filtering: {str(e)}")