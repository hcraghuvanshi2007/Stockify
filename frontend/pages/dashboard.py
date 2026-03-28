import streamlit as st
import traceback
import pandas as pd
import os
import plotly.express as px
from frontend.layout import inject_css

def show_dashboard(metrics=None):
    """Display dashboard with KPI metrics and visualization.
    
    Args:
        metrics (dict): Optional dictionary with keys: total_revenue, total_quantity, 
                       avg_order_value, unique_products
    """
    try:
        inject_css()
    except Exception as e:
        st.error(f"CSS injection failed: {str(e)}")
        st.write(traceback.format_exc())
    
    # If metrics not provided, calculate from data
    if metrics is None:
        metrics = _load_dashboard_data()

    try:
        # Page header
        st.markdown("""
        <div class='page-header'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <div>
                    <div class='page-header-title' style='margin: 0;'>Overview</div>
                </div>
            </div>
            <div class='page-header-subtitle'>Key inventory and sales metrics at a glance</div>
        </div>
        """, unsafe_allow_html=True)

        # Demo Mode banner
        st.markdown("""
        <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #3b82f6; border-radius: 12px; padding: 12px 16px; margin-bottom: 24px; color: #0f172a; font-size: 14px;'>
            <span style='font-weight: 600;'>Demo Mode Active</span> — Full access to explore features
        </div>
        """, unsafe_allow_html=True)

        # Key metrics with colored left borders
        col1, col2, col3, col4 = st.columns(4)

        # Format metrics for display
        revenue_str = f"${metrics['total_revenue']:,.2f}" if metrics['total_revenue'] > 0 else "—"
        units_str = f"{metrics['total_quantity']:,}" if metrics['total_quantity'] > 0 else "—"
        products_str = f"{metrics['unique_products']}" if metrics['unique_products'] > 0 else "—"
        avg_trans_str = f"${metrics['avg_order_value']:,.2f}" if metrics['avg_order_value'] > 0 else "—"

        with col1:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #3b82f6; border-radius: 12px; padding: 16px; box-shadow: 0 4px 24px rgba(59,130,246,0.08); animation: fadeInUp 0.4s ease;'>
                <div style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Total Revenue</div>
                <div style='color: #1d4ed8; font-weight: 700; font-size: 24px;'>{revenue_str}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #06b6d4; border-radius: 12px; padding: 16px; box-shadow: 0 4px 24px rgba(59,130,246,0.08); animation: fadeInUp 0.4s ease 0.1s both;'>
                <div style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Units Sold</div>
                <div style='color: #0e7490; font-weight: 700; font-size: 24px;'>{units_str}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #6366f1; border-radius: 12px; padding: 16px; box-shadow: 0 4px 24px rgba(59,130,246,0.08); animation: fadeInUp 0.4s ease 0.2s both;'>
                <div style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Products</div>
                <div style='color: #4f46e5; font-weight: 700; font-size: 24px;'>{products_str}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #0ea5e9; border-radius: 12px; padding: 16px; box-shadow: 0 4px 24px rgba(59,130,246,0.08); animation: fadeInUp 0.4s ease 0.3s both;'>
                <div style='color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;'>Avg Transaction</div>
                <div style='color: #0369a1; font-weight: 700; font-size: 24px;'>{avg_trans_str}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Charts section
        st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Revenue & Performance</div>", unsafe_allow_html=True)
        
        colA, colB = st.columns(2)

        with colA:
            try:
                trend_data = _load_trend_data()
                if trend_data is not None and not trend_data.empty:
                    # Import trend chart function
                    from visualization.trend_charts import plot_sales_trend
                    plot_sales_trend(trend_data)
                else:
                    st.info("📊 Upload sales data to view revenue trends")
            except Exception as e:
                st.warning(f"⚠️ Could not load trend chart: {str(e)}")

        with colB:
            try:
                # Show distribution by category or summary stats
                category_data = _load_category_distribution()
                if category_data is not None and not category_data.empty:
                    import plotly.express as px
                    fig = px.pie(
                        category_data,
                        values="total_revenue",
                        names="category",
                        title="Sales by Category",
                        hole=0.3,
                        color_discrete_sequence=px.colors.sequential.Blues_r
                    )
                    st.plotly_chart(fig, use_container_width=True, key="category_dist")
                else:
                    st.info("📊 Upload data to view category distribution")
            except Exception as e:
                st.warning(f"⚠️ Could not load category distribution: {str(e)}")

        st.divider()

        # Top products section
        st.markdown("<div style='color: #0f172a; font-weight: 600; font-size: 18px; margin: 24px 0 16px 0;'>Top Performing Products</div>", unsafe_allow_html=True)
        
        try:
            product_data = _load_product_demand_data()
            if product_data is not None and not product_data.empty:
                # Import demand chart function
                from visualization.demand_charts import plot_top_products
                plot_top_products(product_data)
            else:
                st.info("📊 Upload sales data to view top performing products")
        except Exception as e:
            st.warning(f"⚠️ Could not load product performance chart: {str(e)}")
        
    except Exception as e:
        st.error("❌ Error rendering dashboard")
        st.error(f"Details: {str(e)}")
        st.write(traceback.format_exc())


def _load_dashboard_data():
    """Load and calculate dashboard metrics from processed CSV files."""
    try:
        sales_path = "data/processed/clean_sales.csv"
        
        # Check if sales data exists
        if not os.path.exists(sales_path):
            return {
                "total_revenue": 0,
                "total_quantity": 0,
                "avg_order_value": 0,
                "unique_products": 0
            }
        
        # Load sales data
        sales_df = pd.read_csv(sales_path)
        
        if sales_df.empty:
            return {
                "total_revenue": 0,
                "total_quantity": 0,
                "avg_order_value": 0,
                "unique_products": 0
            }
        
        # Validate required columns
        if "revenue" not in sales_df.columns or "quantity" not in sales_df.columns:
            return {
                "total_revenue": 0,
                "total_quantity": 0,
                "avg_order_value": 0,
                "unique_products": 0
            }
        
        # Convert to numeric and calculate metrics
        revenue = pd.to_numeric(sales_df["revenue"], errors="coerce").fillna(0)
        quantity = pd.to_numeric(sales_df["quantity"], errors="coerce").fillna(0)
        
        total_revenue = revenue.sum()
        total_quantity = int(quantity.sum())
        num_transactions = len(sales_df)
        avg_order_value = total_revenue / num_transactions if num_transactions > 0 else 0
        
        # Get unique products
        unique_products = 0
        if "product" in sales_df.columns:
            unique_products = sales_df["product"].nunique()
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_quantity": total_quantity,
            "avg_order_value": round(avg_order_value, 2),
            "unique_products": unique_products
        }
    except Exception as e:
        st.warning(f"⚠️ Error loading dashboard data: {str(e)}")
        return {
            "total_revenue": 0,
            "total_quantity": 0,
            "avg_order_value": 0,
            "unique_products": 0
        }


def _load_trend_data():
    """Load daily trend data for the sales trend chart."""
    try:
        sales_path = "data/processed/clean_sales.csv"
        
        if not os.path.exists(sales_path):
            return None
        
        sales_df = pd.read_csv(sales_path)
        
        if sales_df.empty:
            return None
        
        # Validate required columns
        if "date" not in sales_df.columns or "quantity" not in sales_df.columns:
            return None
        
        # Use analytics function to aggregate daily trends
        from analytics.trend_analysis import aggregate_daily_trends
        try:
            trend_data = aggregate_daily_trends(sales_df)
            return trend_data
        except Exception:
            # Fallback: manually aggregate if analytics function fails
            trend_data = sales_df.groupby("date", as_index=False).agg({
                "quantity": "sum",
                "revenue": "sum"
            })
            return trend_data
    except Exception as e:
        st.warning(f"⚠️ Error loading trend data: {str(e)}")
        return None


def _load_product_demand_data():
    """Load product-level demand data for the top products chart."""
    try:
        sales_path = "data/processed/clean_sales.csv"
        
        if not os.path.exists(sales_path):
            return None
        
        sales_df = pd.read_csv(sales_path)
        
        if sales_df.empty:
            return None
        
        # Validate required columns
        if "product" not in sales_df.columns or "revenue" not in sales_df.columns:
            return None
        
        # Use analytics function to aggregate product demand
        from analytics.demand_analysis import aggregate_product_demand
        try:
            product_data = aggregate_product_demand(sales_df)
            # Rename columns to match visualization function expectations
            # Convert camelCase to snake_case
            if "totalRevenue" in product_data.columns:
                product_data = product_data.rename(columns={"totalRevenue": "revenue"})
            if "totalQuantity" in product_data.columns:
                product_data = product_data.rename(columns={"totalQuantity": "quantity"})
            if "salesCount" in product_data.columns:
                product_data = product_data.rename(columns={"salesCount": "sales_count"})
            if "avgQuantityPerSale" in product_data.columns:
                product_data = product_data.rename(columns={"avgQuantityPerSale": "avg_quantity_per_sale"})
            
            return product_data
        except Exception:
            # Fallback: manually aggregate if analytics function fails
            product_data = sales_df.groupby("product", as_index=False).agg({
                "revenue": "sum",
                "quantity": "sum"
            })
            return product_data
    except Exception as e:
        st.warning(f"⚠️ Error loading product data: {str(e)}")
        return None


def _load_category_distribution():
    """Load category-wise revenue distribution."""
    try:
        sales_path = "data/processed/clean_sales.csv"
        
        if not os.path.exists(sales_path):
            return None
        
        sales_df = pd.read_csv(sales_path)
        
        if sales_df.empty:
            return None
        
        # Check if category column exists
        if "category" not in sales_df.columns:
            # Fallback: use product grouping
            return _load_product_demand_data()
        
        # Aggregate by category
        category_data = sales_df.groupby("category", as_index=False).agg({
            "revenue": "sum"
        }).rename(columns={"revenue": "total_revenue"})
        
        return category_data
    except Exception as e:
        st.warning(f"⚠️ Error loading category distribution: {str(e)}")
        return None