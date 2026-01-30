# 💎 Silver Price Calculator & Silver Sales Analysis

A comprehensive Streamlit application for analyzing silver prices and state-wise silver purchases in India.

## Features

### 1. Silver Price Calculator
- Calculate total silver cost based on weight (grams/kilograms) and current price
- Currency conversion (INR to USD, EUR, GBP, AED)
- Interactive historical silver price chart with filters:
  - ≤ ₹20,000 per kg
  - ₹20,000 - ₹30,000 per kg
  - ≥ ₹30,000 per kg
- Statistical insights (Min, Max, Average prices)

### 2. Silver Sales Dashboard
- Interactive India state-wise map with color-coded silver purchases
- Top 5 states with highest silver purchases (bar chart)
- Karnataka monthly purchase trends (line chart)
- Overall statistics and insights

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

Navigate to the Cia 1 directory and run:
```bash
streamlit run 2547230_cia2.py
```

## Required Files

Ensure the following files are in the correct locations:
- `historical_silver_price.csv` (in Cia 1 folder)
- `state_wise_silver_purchased_kg.csv` (in Cia 1 folder)
- `State.shp` and related files (in ../State/ folder)

## Deployment

To deploy this application, you can use:
- **Streamlit Cloud**: Push to GitHub and deploy via share.streamlit.io
- **Heroku**: Use a Procfile and requirements.txt
- **AWS/Azure**: Deploy as a containerized application

## Usage

1. **Silver Price Calculator Tab**:
   - Enter weight in grams or kilograms
   - Input current price per gram
   - View calculated total cost
   - Select currency for conversion
   - Explore historical price trends with filters

2. **Silver Sales Dashboard Tab**:
   - View state-wise map (darker shades = higher purchases)
   - Analyze top 5 purchasing states
   - Examine Karnataka's monthly trends
   - Review overall statistics

## Technologies Used
- **Streamlit**: Web application framework
- **GeoPandas**: Geographic data manipulation and visualization
- **Plotly**: Interactive charts
- **Pandas**: Data analysis
- **Matplotlib**: Map visualization

## Author
Student ID: 2547230
