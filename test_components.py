"""
Test script to verify all components of the Silver Analysis application
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import pandas as pd
        print("✓ pandas installed")
        import streamlit as st
        print("✓ streamlit installed")
        import geopandas as gpd
        print("✓ geopandas installed")
        import matplotlib.pyplot as plt
        print("✓ matplotlib installed")
        import plotly.express as px
        print("✓ plotly installed")
        import numpy as np
        print("✓ numpy installed")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\nTesting data files...")
    files_to_check = [
        "historical_silver_price.csv",
        "state_wise_silver_purchased_kg.csv",
        "../State/State.shp",
        "../State/State.dbf",
        "../State/State.shx",
        "../State/State.prj"
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_data_loading():
    """Test if data files can be loaded properly"""
    print("\nTesting data loading...")
    
    try:
        import pandas as pd
        import geopandas as gpd
        
        # Test historical data
        df_historical = pd.read_csv("historical_silver_price.csv")
        print(f"✓ Historical data loaded: {len(df_historical)} rows")
        
        # Test silver purchase data
        df_silver = pd.read_csv("state_wise_silver_purchased_kg.csv")
        print(f"✓ Silver purchase data loaded: {len(df_silver)} rows")
        
        # Test shapefile
        india_map = gpd.read_file("../State/State.shp")
        print(f"✓ Shapefile loaded: {len(india_map)} features")
        
        return True
    except Exception as e:
        print(f"✗ Data loading error: {e}")
        return False

def test_data_structure():
    """Test if data has expected structure"""
    print("\nTesting data structure...")
    try:
        import pandas as pd
        
        # Check historical data structure
        df_historical = pd.read_csv("historical_silver_price.csv")
        expected_cols = ['Year', 'Month', 'Silver_Price_INR_per_kg']
        if all(col in df_historical.columns for col in expected_cols):
            print(f"✓ Historical data has correct columns")
        else:
            print(f"✗ Historical data missing columns")
            return False
        
        # Check silver purchase data structure
        df_silver = pd.read_csv("state_wise_silver_purchased_kg.csv")
        expected_cols = ['State', 'Silver_Purchased_kg']
        if all(col in df_silver.columns for col in expected_cols):
            print(f"✓ Silver purchase data has correct columns")
        else:
            print(f"✗ Silver purchase data missing columns")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Structure test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SILVER ANALYSIS APPLICATION - COMPONENT TEST")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Data Loading", test_data_loading()))
    results.append(("Data Structure", test_data_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed! Application is ready to run.")
        print("\nTo start the application, run:")
        print("  streamlit run 2547230_cia2.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
