"""
Product-level demand analysis aggregation.

This module handles STEP 1 of the analytics pipeline:
aggregating raw sales data to product-level metrics.
"""

import pandas as pd


def aggregate_product_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate raw sales data to product-level demand metrics.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string, non-empty)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string; may be missing or empty)

    OUTPUT:
    Returns a DataFrame with exactly these columns:
    - product (string)
    - category (string; defaults to "Uncategorized" if missing/empty)
    - totalQuantity (number) → sum of quantity per product
    - totalRevenue (number) → sum of revenue per product
    - salesCount (integer) → count of records per product
    - avgQuantityPerSale (float) → totalQuantity / salesCount

    CATEGORY HANDLING:
    - Per product, uses the first non-empty category value.
    - If all category values for a product are missing/empty, defaults to "Uncategorized".

    ASSUMPTIONS:
    - Input DataFrame is already clean (schema validation handled by ingestion layer).
    - All rows are valid; no further validation performed.
    - Output is JSON-serializable (no NaN or Infinity).

    ARGS:
        df: Clean sales data DataFrame.

    RETURNS:
        Aggregated product-level DataFrame matching the output contract exactly.
    """
    # Group by product and aggregate metrics
    grouped = df.groupby("product", as_index=False).agg(
        totalQuantity=("quantity", "sum"),
        totalRevenue=("revenue", "sum"),
        salesCount=("quantity", "count"),
        category=("category", lambda x: _get_first_valid_category(x)),
    )

    # Calculate average quantity per sale
    grouped["avgQuantityPerSale"] = grouped["totalQuantity"] / grouped["salesCount"]

    # Reorder columns to match output contract
    result = grouped[["product", "category", "totalQuantity", "totalRevenue", "salesCount", "avgQuantityPerSale"]]

    # Ensure JSON-serializability by converting inf/NaN to safe values
    result = result.fillna(0).replace([float("inf"), float("-inf")], 0)

    return result


def aggregate_category_demand(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate raw sales data to category-level demand metrics.

    INPUT:
    Expects a clean Pandas DataFrame with columns:
    - product (string, non-empty)
    - date (string, format YYYY-MM-DD)
    - quantity (int > 0)
    - revenue (float)
    - category (string; may be missing or empty)

    OUTPUT:
