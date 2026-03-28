import streamlit as st
import pandas as pd
import os
from pathlib import Path
from frontend.layout import inject_css
# Setup path for imports
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(project_root))

from analytics.demand_analysis import aggregate_top_products, aggregate_product_demand
from visualization.demand_charts import plot_top_products


def load_sales_inventory():
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


def calculate_profit_margins(sales_df, inventory_df):
    """Calculate profit margin per product."""
    if sales_df is None or inventory_df is None:
        return None
    
    try:
        # Get product revenue from sales
        product_revenue = sales_df.groupby("product").agg({
            "revenue": "sum",
            "quantity": "sum"
        }).reset_index()
        
        # Merge with inventory (Unit Cost, Selling Price)
        if "Product Name" in inventory_df.columns:
            inventory_df_merge = inventory_df[["Product Name", "Unit Cost", "Selling Price"]].copy()
            inventory_df_merge.columns = ["product", "Unit Cost", "Selling Price"]
        else:
            inventory_df_merge = inventory_df.copy()
        
        merged = product_revenue.merge(
            inventory_df_merge,
            on="product",
            how="left"
        )
        
        # Calculate profit margin
        if "Selling Price" in merged.columns and "Unit Cost" in merged.columns:
            merged["Profit Margin %"] = (
                ((merged["Selling Price"] - merged["Unit Cost"]) / merged["Selling Price"] * 100)
                .fillna(0)
            )
            return merged[["product", "revenue", "quantity", "Profit Margin %"]].sort_values("Profit Margin %", ascending=False)
        
        return None
    except Exception as e:
        st.warning(f" Could not calculate profit margins: {str(e)}")
        return None


def show_products():
    """Display product performance analytics."""
    inject_css()
    
    # Page header
    st.markdown("""
    <div class='page-header'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            <div>
                <div class='page-header-title' style='margin: 0;'>Product Performance</div>
            </div>
        </div>
        <div class='page-header-subtitle'>Comprehensive analysis of product sales, inventory, and profitability</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    sales_df, inventory_df = load_sales_inventory()
    
    if sales_df is None or inventory_df is None:
        st.error("Cannot load data. Please upload CSV files first.")
        st.info("Go to Upload page to upload inventory and sales data.")
        return
    
    # ========== TOP METRICS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Key Metrics</div>", unsafe_allow_html=True)
    
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        total_products = sales_df["product"].nunique()
        total_revenue = sales_df["revenue"].sum()
        total_quantity = sales_df["quantity"].sum()
        avg_revenue_per_product = total_revenue / total_products if total_products > 0 else 0
        
        col1.metric("Total Products", f"{total_products:,}")
        col2.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
        col3.metric("Total Quantity", f"{int(total_quantity):,} units")
        col4.metric("Avg Revenue/Product", f"₹ {avg_revenue_per_product:,.0f}")
    except Exception as e:
        st.warning(f"Error computing metrics: {str(e)}")
    
    st.divider()
    
    # ========== TOP PRODUCTS BY REVENUE ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Top Products by Revenue</div>", unsafe_allow_html=True)
    
    try:
        if not sales_df.empty:
            top_revenue = aggregate_top_products(sales_df, top_n=8)
            
            if top_revenue is not None and not top_revenue.empty:
                # Show chart
                plot_top_products(top_revenue, chart_key="top_products_chart")
                
                # Show table
                with st.expander("View Details", expanded=False):
                    display_df = top_revenue[["product", "revenue", "quantity"]].copy()
                    display_df.columns = ["Product", "Revenue (₹)", "Quantity"]
                    display_df["Revenue (₹)"] = display_df["Revenue (₹)"].apply(lambda x: f"₹ {x:,.2f}")
                    st.dataframe(display_df, use_container_width=True, hide_index=True, key="top_products_table")
            else:
                st.info("No product revenue data available")
        else:
            st.info("No sales data available")
    except Exception as e:
        st.warning(f"Could not generate revenue chart: {str(e)}")
    
    st.divider()
    
    # ========== PRODUCT DEMAND ANALYSIS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Product Demand Analysis</div>", unsafe_allow_html=True)
    
    try:
        if not sales_df.empty:
            product_demand = aggregate_product_demand(sales_df)
            
            if product_demand is not None and not product_demand.empty:
                # Sort by revenue
                product_demand = product_demand.sort_values("totalRevenue", ascending=False)
                
                col_high, col_medium, col_low = st.columns(3)
                
                total_products_count = len(product_demand)
                high_demand = len(product_demand[product_demand["totalRevenue"] > product_demand["totalRevenue"].quantile(0.66)])
                medium_demand = len(product_demand[(product_demand["totalRevenue"] <= product_demand["totalRevenue"].quantile(0.66)) & 
                                                    (product_demand["totalRevenue"] > product_demand["totalRevenue"].quantile(0.33))])
                low_demand = total_products_count - high_demand - medium_demand
                
                col_high.metric("High Demand", high_demand)
                col_medium.metric("Medium Demand", medium_demand)
                col_low.metric("Low Demand", low_demand)
                
                # Detailed table
                with st.expander("Detailed Product Analysis", expanded=True):
                    display_columns = ["product", "category", "totalQuantity", "totalRevenue", "avgQuantityPerSale"]
                    display_df = product_demand[display_columns].copy()
                    display_df.columns = ["Product", "Category", "Total Qty", "Revenue (₹)", "Avg Qty/Sale"]
                    display_df["Revenue (₹)"] = display_df["Revenue (₹)"].apply(lambda x: f"₹ {x:,.2f}")
                    display_df["Avg Qty/Sale"] = display_df["Avg Qty/Sale"].apply(lambda x: f"{x:.2f}")
                    st.dataframe(display_df, use_container_width=True, hide_index=True, key="demand_analysis_table")
            else:
                st.info("No product demand data available")
        else:
            st.info("No sales data available")
    except Exception as e:
        st.warning(f"Could not generate demand analysis: {str(e)}")
    
    st.divider()
    
    # ========== INVENTORY STATUS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Current Inventory Status</div>", unsafe_allow_html=True)
    
    try:
        if inventory_df is not None and not inventory_df.empty:
            required_cols = ["Product Name", "Quantity On Hand", "Reorder Point"]
            
            if all(col in inventory_df.columns for col in required_cols):
                # Calculate inventory metrics
                inventory_df_display = inventory_df[required_cols].copy()
                inventory_df_display["Stock Status"] = inventory_df_display.apply(
                    lambda row: "Low" if row["Quantity On Hand"] <= row["Reorder Point"] 
                    else ("Medium" if row["Quantity On Hand"] <= row["Reorder Point"] * 2 else "Healthy"),
                    axis=1
                )
                
                # Summary
                col_in_stock, col_low_stock, col_over_stock = st.columns(3)
                
                in_stock = len(inventory_df_display[inventory_df_display["Stock Status"] == "Healthy"])
                low_stock = len(inventory_df_display[inventory_df_display["Stock Status"] == "Low"])
                medium_stock = len(inventory_df_display[inventory_df_display["Stock Status"] == "Medium"])
                
                col_in_stock.metric("Healthy Stock", in_stock)
                col_low_stock.metric("Low Stock", low_stock)
                col_over_stock.metric("Medium Stock", medium_stock)
                
                # Detailed inventory
                with st.expander("Inventory Details", expanded=True):
                    st.dataframe(inventory_df_display, use_container_width=True, hide_index=True, key="inventory_status_table")
            else:
                st.warning(f"Inventory missing required columns: {required_cols}")
        else:
            st.info("No inventory data available")
    except Exception as e:
        st.warning(f"Could not display inventory: {str(e)}")
    
    st.divider()
    
    # ========== PROFIT MARGINS ==========
    st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Product Profitability</div>", unsafe_allow_html=True)
    
    try:
        profit_margins = calculate_profit_margins(sales_df, inventory_df)
        
        if profit_margins is not None and not profit_margins.empty:
            # Top by margin
            top_margin = profit_margins.nlargest(5, "Profit Margin %")
            bottom_margin = profit_margins.nsmallest(5, "Profit Margin %")
            
            col_top, col_bottom = st.columns(2)
            
            with col_top:
                st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 16px; margin-bottom: 16px;'>Highest Profit Margin</div>", unsafe_allow_html=True)
                for idx, row in top_margin.iterrows():
                    st.write(f"**{row['product']}**: {row['Profit Margin %']:.1f}% | ₹ {row['revenue']:,.0f}")
            
            with col_bottom:
                st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 16px; margin-bottom: 16px;'>Lowest Profit Margin</div>", unsafe_allow_html=True)
                for idx, row in bottom_margin.iterrows():
                    st.write(f"**{row['product']}**: {row['Profit Margin %']:.1f}% | ₹ {row['revenue']:,.0f}")
            
            # Full table
            with st.expander(" All Profit Margins", expanded=False):
                display_pm = profit_margins.copy()
                display_pm["Revenue (₹)"] = display_pm["revenue"].apply(lambda x: f"₹ {x:,.2f}")
                display_pm["Profit Margin %"] = display_pm["Profit Margin %"].apply(lambda x: f"{x:.1f}%")
                display_pm = display_pm[["product", "Revenue (₹)", "quantity", "Profit Margin %"]].copy()
                display_pm.columns = ["Product", "Revenue", "Quantity", "Profit Margin"]
                st.dataframe(display_pm, use_container_width=True, hide_index=True, key="profit_margins_table")
        else:
            st.info("Could not calculate profit margins")
    except Exception as e:
        st.warning(f" Could not display profit margins: {str(e)}")