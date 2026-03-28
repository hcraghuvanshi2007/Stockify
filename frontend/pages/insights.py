import streamlit as st
import pandas as pd
import os
from pathlib import Path
from frontend.layout import inject_css
# Setup path for imports
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(project_root))

from decision_support.stock_alerts import generate_stock_alerts
from decision_support.reorder_logic import generate_reorder_recommendations
from analytics.demand_analysis import aggregate_product_demand
from visualization.alert_visuals import show_alerts


def load_data():
    """Load sales and inventory data with error handling."""
    sales_path = "data/processed/clean_sales.csv"
    inventory_path = "data/processed/clean_inventory.csv"
    
    sales_df = None
    inventory_df = None
    
    try:
        if os.path.exists(sales_path):
            sales_df = pd.read_csv(sales_path)
            if sales_df.empty:
                sales_df = None
    except Exception as e:
        st.warning(f" Could not load sales data: {str(e)}")
    
    try:
        if os.path.exists(inventory_path):
            inventory_df = pd.read_csv(inventory_path)
            if inventory_df.empty:
                inventory_df = None
    except Exception as e:
        st.warning(f" Could not load inventory data: {str(e)}")
    
    return sales_df, inventory_df


def get_most_profitable_products(sales_df, inventory_df):
    """Find most profitable products."""
    if sales_df is None or inventory_df is None:
        return None
    
    try:
        # Get product revenue
        product_revenue = sales_df.groupby("product").agg({
            "revenue": "sum"
        }).reset_index().sort_values("revenue", ascending=False)
        
        return product_revenue.head(5)
    except Exception as e:
        st.warning(f" Could not identify profitable products: {str(e)}")
        return None


def get_slow_moving_products(sales_df):
    """Identify slow-moving products (below average quantity)."""
    if sales_df is None or sales_df.empty:
        return None
    
    try:
        product_qty = sales_df.groupby("product").agg({
            "quantity": "sum"
        }).reset_index()
        
        avg_qty = product_qty["quantity"].mean()
        slow_movers = product_qty[product_qty["quantity"] < avg_qty].sort_values("quantity")
        
        return slow_movers.head(5)
    except Exception as e:
        st.warning(f" Could not identify slow-moving products: {str(e)}")
        return None


def display_alert_section(alerts_df, alert_type, emoji, color):
    """Display color-coded alert section."""
    if alerts_df is None or alerts_df.empty:
        return
    
    try:
        filtered = alerts_df[alerts_df["Alert Type"] == alert_type]
        
        if not filtered.empty:
            count = len(filtered)
            
            if color == "red":
                st.markdown(f':red[### {emoji} {alert_type.upper()} ({count})]')
                for _, row in filtered.iterrows():
                    product = row.get("Product Name", "Unknown")
                    stock = row.get("Current Stock", "N/A")
                    recommendation = row.get("Recommendation", "Take action")
                    
                    with st.container(border=True):
                        st.markdown(f"**{product}** ")
                        st.write(f"Current Stock: {stock}")
                        st.write(f" {recommendation}")
            
            elif color == "yellow":
                st.markdown(f':orange[### {emoji} {alert_type.upper()} ({count})]')
                for _, row in filtered.iterrows():
                    product = row.get("Product Name", "Unknown")
                    stock = row.get("Current Stock", "N/A")
                    recommendation = row.get("Recommendation", "Monitor closely")
                    
                    with st.container(border=True):
                        st.markdown(f"**{product}** ")
                        st.write(f"Current Stock: {stock}")
                        st.write(f" {recommendation}")
            
            elif color == "green":
                st.markdown(f':green[### {emoji} {alert_type.upper()} ({count})]')
                col_count = min(3, len(filtered))
                cols = st.columns(col_count)
                
                for idx, (_, row) in enumerate(filtered.iterrows()):
                    if idx >= col_count:
                        break
                    with cols[idx]:
                        product = row.get("Product Name", "Unknown")
                        st.markdown(f" **{product}**")
    
    except Exception as e:
        st.warning(f" Error displaying alerts: {str(e)}")


def show_insights():
    """Display smart insights and recommendations."""
    inject_css()
    
    # Page header
    st.markdown("""
    <div class='page-header'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path>
            </svg>
            <div>
                <div class='page-header-title' style='margin: 0;'>Smart Insights & Recommendations</div>
            </div>
        </div>
        <div class='page-header-subtitle'>AI-powered inventory insights and actionable recommendations</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    sales_df, inventory_df = load_data()
    
    if inventory_df is None:
        st.error("Cannot load inventory data. Please upload CSV files first.")
        st.info("Go to Upload page to upload inventory data.")
        return
    
    # ========== SUMMARY INSIGHT CARDS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Inventory Health Summary</div>", unsafe_allow_html=True)
    
    try:
        # Generate stock alerts
        alerts_df = generate_stock_alerts(inventory_df)
        reorder_df = generate_reorder_recommendations(inventory_df)
        
        # Calculate metrics
        low_stock_count = len(alerts_df[alerts_df["Alert Type"] == "Low Stock"]) if not alerts_df.empty else 0
        overstock_count = len(alerts_df[alerts_df["Alert Type"] == "Overstock"]) if not alerts_df.empty else 0
        healthy_count = len(alerts_df[alerts_df["Alert Type"] == "Healthy"]) if not alerts_df.empty else 0
        reorder_needed = len(reorder_df[reorder_df["Suggested Reorder Quantity"] > 0]) if not reorder_df.empty else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Healthy Stock", healthy_count)
        col2.metric("Overstock", overstock_count)
        col3.metric("Low Stock", low_stock_count)
        col4.metric("Reorder Needed", reorder_needed)
        
    except Exception as e:
        st.warning(f"Error computing summary: {str(e)}")
    
    st.divider()
    
    # ========== COLOR-CODED ALERTS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Alerts by Risk Level</div>", unsafe_allow_html=True)
    
    try:
        if not alerts_df.empty:
            # Critical (Low Stock)
            low_stock_items = alerts_df[alerts_df["Alert Type"] == "Low Stock"]
            if not low_stock_items.empty:
                st.markdown("<div style='color: #dc2626; font-weight: 600; font-size: 16px; margin-bottom: 12px;'>Low Stock Alert</div>", unsafe_allow_html=True)
                for _, row in low_stock_items.iterrows():
                    product = row.get("Product Name", "Unknown")
                    stock = row.get("Current Stock", "N/A")
                    st.markdown(f"""
                    <div style='background: rgba(254,242,242,0.7); border-left: 3px solid #dc2626; border-radius: 8px; padding: 12px; margin-bottom: 8px;'>
                        <div style='font-weight: 600; color: #0f172a;'>{product}</div>
                        <div style='color: #475569; font-size: 14px; margin-top: 4px;'>Current Stock: {stock}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.divider()
            
            # Warning (Overstock)
            overstock_items = alerts_df[alerts_df["Alert Type"] == "Overstock"]
            if not overstock_items.empty:
                st.markdown("<div style='color: #d97706; font-weight: 600; font-size: 16px; margin: 16px 0 12px 0;'>Overstock Alert</div>", unsafe_allow_html=True)
                for _, row in overstock_items.iterrows():
                    product = row.get("Product Name", "Unknown")
                    stock = row.get("Current Stock", "N/A")
                    st.markdown(f"""
                    <div style='background: rgba(255,251,235,0.7); border-left: 3px solid #d97706; border-radius: 8px; padding: 12px; margin-bottom: 8px;'>
                        <div style='font-weight: 600; color: #0f172a;'>{product}</div>
                        <div style='color: #475569; font-size: 14px; margin-top: 4px;'>Current Stock: {stock}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.divider()
            
            # Healthy
            healthy_items = alerts_df[alerts_df["Alert Type"] == "Healthy"]
            if not healthy_items.empty and healthy_count <= 5:
                st.markdown("<div style='color: #16a34a; font-weight: 600; font-size: 16px; margin: 16px 0 12px 0;'>Healthy Stock</div>", unsafe_allow_html=True)
                col_count = min(3, len(healthy_items))
                cols = st.columns(col_count)
                for idx, (_, row) in enumerate(healthy_items.iterrows()):
                    if idx >= col_count:
                        break
                    with cols[idx]:
                        product = row.get("Product Name", "Unknown")
                        stock = row.get("Current Stock", "N/A")
                        st.markdown(f"""
                        <div style='background: rgba(240,253,244,0.7); border-left: 3px solid #16a34a; border-radius: 8px; padding: 12px; text-align: center;'>
                            <div style='font-weight: 600; color: #0f172a;'>{product}</div>
                            <div style='color: #16a34a; font-size: 14px; margin-top: 4px;'>In Stock</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No alerts to display")
    except Exception as e:
        st.warning(f"Error displaying alerts: {str(e)}")
    
    st.divider()
    
    # ========== DETAILED RECOMMENDATIONS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Reorder Recommendations</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Products that need immediate restocking</div>", unsafe_allow_html=True)
    
    try:
        if not reorder_df.empty:
            # Filter items needing reorder
            reorder_needed = reorder_df[reorder_df["Suggested Reorder Quantity"] > 0]
            
            if not reorder_needed.empty:
                # Summary
                col_rec1, col_rec2, col_rec3 = st.columns(3)
                total_to_reorder = reorder_needed["Suggested Reorder Quantity"].sum()
                avg_per_item = total_to_reorder / len(reorder_needed)
                
                col_rec1.metric("Items to Reorder", len(reorder_needed))
                col_rec2.metric("Total Units", int(total_to_reorder))
                col_rec3.metric("Avg per Item", int(avg_per_item))
                
                # Detailed table
                with st.expander("Detailed Reorder List", expanded=True):
                    display_reorder = reorder_needed.copy()
                    st.dataframe(display_reorder, use_container_width=True, hide_index=True, key="reorder_recommendations_table")
            else:
                st.markdown("""
                <div style='background: rgba(240,253,244,0.7); border-left: 3px solid #16a34a; border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 12px;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <div>
                        <div style='font-weight: 600; color: #16a34a;'>All products are well-stocked</div>
                        <div style='color: #475569; font-size: 14px;'>No reorders needed at this time</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No reorder data available")
    except Exception as e:
        st.warning(f"Could not display recommendations: {str(e)}")
    
    st.divider()
    
    # ========== PROFITABILITY ANALYSIS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Most Profitable Products</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Top-performing products by revenue</div>", unsafe_allow_html=True)
    
    try:
        profitable = get_most_profitable_products(sales_df, inventory_df)
        
        if profitable is not None and not profitable.empty:
            col_p1, col_p2, col_p3 = st.columns(3)
            
            top_1 = profitable.iloc[0]
            col_p1.metric(
                f"{top_1['product']}",
                f"₹ {top_1['revenue']:,.0f}"
            )
            
            if len(profitable) > 1:
                top_2 = profitable.iloc[1]
                col_p2.metric(
                    f"{top_2['product']}",
                    f"₹ {top_2['revenue']:,.0f}"
                )
            
            if len(profitable) > 2:
                top_3 = profitable.iloc[2]
                col_p3.metric(
                    f" {top_3['product']}",
                    f"₹ {top_3['revenue']:,.0f}"
                )
            
            # Full list
            with st.expander("All Profitable Products", expanded=False):
                display_profitable = profitable.copy()
                display_profitable.columns = ["Product", "Revenue (₹)"]
                display_profitable["Revenue (₹)"] = display_profitable["Revenue (₹)"].apply(lambda x: f"₹ {x:,.2f}")
                st.dataframe(display_profitable, use_container_width=True, hide_index=True, key="profitable_products_table")
        else:
            st.info("Could not identify profitable products")
    except Exception as e:
        st.warning(f"Error in profitability analysis: {str(e)}")
    
    st.divider()
    
    # ========== SLOW-MOVING PRODUCTS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Slow-Moving Products</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Products with below-average sales velocity</div>", unsafe_allow_html=True)
    
    try:
        slow_movers = get_slow_moving_products(sales_df)
        
        if slow_movers is not None and not slow_movers.empty:
            st.markdown(f"<div style='background: rgba(255,251,235,0.7); border-left: 3px solid #d97706; border-radius: 12px; padding: 12px; color: #0f172a; font-weight: 600; margin-bottom: 16px;'>{len(slow_movers)} product(s) are moving slower than average</div>", unsafe_allow_html=True)
            
            for idx, (_, row) in enumerate(slow_movers.iterrows(), 1):
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #d97706; border-radius: 12px; padding: 16px; margin-bottom: 12px;'>
                    <div style='font-weight: 600; color: #0f172a;'>#{idx}. {row['product']}</div>
                    <div style='color: #475569; font-size: 14px; margin-top: 8px;'>Total Quantity Sold: {int(row['quantity'])} units</div>
                    <div style='color: #0e7490; font-size: 14px; margin-top: 8px;'>Recommendation: Consider promotional discount or bundling to increase sales velocity</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background: rgba(240,253,244,0.7); border-left: 3px solid #16a34a; border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 12px;'>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <div>
                    <div style='font-weight: 600; color: #16a34a;'>No significant slow-moving products</div>
                    <div style='color: #475569; font-size: 14px;'>All products are performing well</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Error identifying slow movers: {str(e)}")
    
    st.divider()
    
    # ========== AI INSIGHTS ==========
    st.subheader(" AI-Generated Insights")
    st.caption("Smart recommendations based on current data")
    
    try:
        insights = []
        
        if sales_df is not None and not sales_df.empty:
            # Insight 1: Best performing product
            if "product" in sales_df.columns:
                top_product = sales_df.groupby("product")["revenue"].sum().idxmax()
                insights.append(f" **Focus on {top_product}**: Your top performer - maintain stock and visibility.")
        
        if inventory_df is not None and not inventory_df.empty:
            # Insight 2: Reorder urgency
            low_stock_items = len(alerts_df[alerts_df["Alert Type"] == "Low Stock"]) if not alerts_df.empty else 0
            if low_stock_items > 0:
                insights.append(f" **Urgent Reorder**: {low_stock_items} items are below reorder point.")
            
            # Insight 3: Overstock
            overstock_items = len(alerts_df[alerts_df["Alert Type"] == "Overstock"]) if not alerts_df.empty else 0
            if overstock_items > 0:
                insights.append(f" **Overstock Alert**: {overstock_items} items exceed optimal levels - consider discounts.")
        
        if sales_df is not None and not sales_df.empty:
            # Insight 4: Demand pattern
            if "category" in sales_df.columns:
                top_category = sales_df.groupby("category")["revenue"].sum().idxmax()
                insights.append(f" **Category Leader**: {top_category} is your strongest category.")
        
        if not insights:
            insights.append(" All systems running smoothly. Continue monitoring for changes.")
        
        for insight in insights:
            st.markdown(f"- {insight}")
    
    except Exception as e:
        st.warning(f" Error generating insights: {str(e)}")