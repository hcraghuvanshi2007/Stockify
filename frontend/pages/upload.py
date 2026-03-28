import streamlit as st
from pathlib import Path
import sys
import logging
from frontend.layout import inject_css

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _ensure_project_root_in_path():
    # ensure package imports work whether running from frontend/ or project root
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        logger.info(f"Added project root to sys.path: {project_root}")


_ensure_project_root_in_path()

# Track import status
_import_error = None

try:
    from ingestion import process_inventory_file, process_sales_file
    logger.info("✓ Successfully imported ingestion pipeline functions")
except Exception as e:
    # fallback: set to None if import fails
    _import_error = e
    logger.error(f"✗ Failed to import ingestion pipeline: {str(e)}", exc_info=True)
    process_inventory_file = None
    process_sales_file = None


def show_upload():
    """Display file upload page for inventory and sales data."""
    inject_css()
    
    # Page header
    st.markdown("""
    <div class='page-header'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <div>
                <div class='page-header-title' style='margin: 0;'>Upload Data</div>
            </div>
        </div>
        <div class='page-header-subtitle'>Upload CSV or Excel files for inventory and sales analysis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-left: 3px solid #3b82f6; border-radius: 12px; padding: 12px 16px; margin-bottom: 24px; color: #0f172a; font-size: 14px;'>
        Processed files will be saved in the <span style='font-weight: 600;'>data/processed</span> folder
    </div>
    """, unsafe_allow_html=True)

    # Inventory section
    st.markdown("""
    <div style='margin-bottom: 16px;'>
        <div style='font-weight: 600; color: #0f172a; margin-bottom: 12px;'>Inventory File</div>
        <div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Upload your inventory CSV or Excel file</div>
    </div>
    """, unsafe_allow_html=True)
    
    inv_file = st.file_uploader("Drop inventory CSV/Excel file here", type=["csv", "xlsx"], key="inventory_uploader")
    if inv_file is not None:
        if process_inventory_file is None:
            st.error(
                "❌ Ingestion pipeline not available (import error).\n\n"
                f"**Details:** {str(_import_error) if _import_error else 'Unknown error'}\n\n"
                "Run `python debug_imports.py` at project root to diagnose."
            )
            logger.error(f"Inventory upload failed - import error: {_import_error}")
        else:
            try:
                logger.info(f"Processing inventory file: {inv_file.name}")
                cleaned = process_inventory_file(inv_file)
                logger.info(f"Successfully processed inventory file: {len(cleaned)} rows")
                st.markdown("""
                <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <span style='color: #16a34a; font-weight: 600;'>Inventory file processed successfully</span>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(cleaned.head(10), use_container_width=True)
            except Exception as e:
                logger.error(f"Error processing inventory file: {str(e)}", exc_info=True)
                st.error(
                    f"❌ Error processing inventory file:\n\n"
                    f"**Type:** {type(e).__name__}\n\n"
                    f"**Message:** {str(e)}\n\n"
                    "Check the server logs for more details."
                )

    st.markdown("##### Expected Columns")
    st.table({
        "Product ID": ["P001", "P002"],
        "Product Name": ["Coffee Beans", "Green Tea"],
        "Category": ["Beverages", "Beverages"],
        "Quantity On Hand": [120, 80],
        "Reorder Point": [30, 20],
        "Unit Cost": [3.50, 2.00],
        "Selling Price": [5.99, 3.99],
        "Last Purchase Date": ["2026-01-10", "2026-01-12"]
    })

    st.divider()

    # Sales section
    st.markdown("""
    <div style='margin-bottom: 16px;'>
        <div style='font-weight: 600; color: #0f172a; margin-bottom: 12px;'>Sales File</div>
        <div style='color: #475569; font-size: 14px; margin-bottom: 12px;'>Upload your sales CSV or Excel file</div>
    </div>
    """, unsafe_allow_html=True)
    
    sales_file = st.file_uploader("Drop sales CSV/Excel file here", type=["csv", "xlsx"], key="sales_uploader")
    if sales_file is not None:
        if process_sales_file is None:
            st.error(
                "❌ Ingestion pipeline not available (import error).\n\n"
                f"**Details:** {str(_import_error) if _import_error else 'Unknown error'}\n\n"
                "Run `python debug_imports.py` at project root to diagnose."
            )
            logger.error(f"Sales upload failed - import error: {_import_error}")
        else:
            try:
                logger.info(f"Processing sales file: {sales_file.name}")
                cleaned = process_sales_file(sales_file)
                logger.info(f"Successfully processed sales file: {len(cleaned)} rows")
                st.markdown("""
                <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                    <span style='color: #16a34a; font-weight: 600;'>Sales file processed successfully</span>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(cleaned.head(10), use_container_width=True)
            except Exception as e:
                logger.error(f"Error processing sales file: {str(e)}", exc_info=True)
                st.error(
                    f"❌ Error processing sales file:\n\n"
                    f"**Type:** {type(e).__name__}\n\n"
                    f"**Message:** {str(e)}\n\n"
                    "Check the server logs for more details."
                )

    st.divider()

    st.markdown("##### Expected Columns")
    st.table({
        "product": ["Coffee Beans", "Green Tea"],
        "date": ["2026-01-15", "2026-01-15"],
        "quantity": [45, 30],
        "revenue": [675.0, 240.0],
        "category": ["Beverages", "Beverages"]
    })