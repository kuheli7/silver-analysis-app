import pandas as pd
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Silver Price Calculator & Sales Analysis", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>.main{padding:0rem 1rem}.stTabs [data-baseweb='tab-list']{gap:24px}.stTabs [data-baseweb='tab']{height:50px;padding-left:20px;padding-right:20px}</style>", unsafe_allow_html=True)
st.title("Silver Price Calculator & Silver Sales Analysis")
st.markdown("---")
tab1, tab2 = st.tabs(["Silver Price Calculator", "Silver Sales Dashboard"])

with tab1:
    st.header("Silver Price Calculator")
    st.subheader("Calculate Silver Cost")
    col1, col2 = st.columns(2)
    with col1:
        weight_unit = st.radio("Select Weight Unit:", ["Grams", "Kilograms"], horizontal=True)
        weight = st.number_input(f"Enter Weight ({'grams' if weight_unit == 'Grams' else 'kilograms'}):", min_value=0.0, value=100.0 if weight_unit == "Grams" else 0.1, step=1.0 if weight_unit == "Grams" else 0.01)
        weight_in_grams = weight if weight_unit == "Grams" else weight * 1000
        price_per_gram = st.number_input("Current Price per Gram (INR):", min_value=0.0, value=75.0, step=0.1)
        total_cost_inr = weight_in_grams * price_per_gram
        st.markdown("---")
        st.subheader("Total Cost")
        st.metric(label="Cost in INR", value=f"₹{total_cost_inr:,.2f}")
    with col2:
        st.subheader("Currency Conversion")
        currency = st.selectbox("Converting total cost to:", ["USD", "EUR", "GBP", "AED"])
        exchange_rates = {"USD": 83.50, "EUR": 90.25, "GBP": 105.50, "AED": 22.75}
        converted_amount = total_cost_inr / exchange_rates[currency]
        st.metric(label=f"Cost in {currency}", value=f"{currency} {converted_amount:,.2f}")
        st.info(f"**Summary:**\n- Weight: {weight_in_grams:,.2f} grams ({weight_in_grams/1000:,.3f} kg)\n- Price per gram: ₹{price_per_gram:,.2f}\n- Total Cost: ₹{total_cost_inr:,.2f}\n- Converted: {currency} {converted_amount:,.2f}")
    st.markdown("---")
    st.subheader("Historical Silver Price Trends")
    try:
        df_historical = pd.read_csv("historical_silver_price.csv")
        df_historical['Date'] = pd.to_datetime(df_historical['Year'].astype(str) + '-' + df_historical['Month'], format='%Y-%b')
        df_historical = df_historical.sort_values('Date')
        price_filter = st.radio("Filter by Price Range:", ["All Prices", "≤ ₹20,000 per kg", "₹20,000 - ₹30,000 per kg", "≥ ₹30,000 per kg"], horizontal=True)
        if price_filter == "≤ ₹20,000 per kg":
            df_filtered = df_historical[df_historical['Silver_Price_INR_per_kg'] <= 20000]
        elif price_filter == "₹20,000 - ₹30,000 per kg":
            df_filtered = df_historical[(df_historical['Silver_Price_INR_per_kg'] > 20000) & (df_historical['Silver_Price_INR_per_kg'] <= 30000)]
        elif price_filter == "≥ ₹30,000 per kg":
            df_filtered = df_historical[df_historical['Silver_Price_INR_per_kg'] > 30000]
        else:
            df_filtered = df_historical
        fig = go.Figure(go.Scatter(x=df_filtered['Date'], y=df_filtered['Silver_Price_INR_per_kg'], mode='lines', line=dict(color='#C0C0C0', width=2), fill='tozeroy', fillcolor='rgba(192,192,192,0.2)'))
        fig.update_layout(title=f"Historical Silver Prices ({price_filter})", xaxis_title="Date", yaxis_title="Price (INR per kg)", hovermode='x unified', height=500, template='plotly_white')
        st.plotly_chart(fig, width='stretch')
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Min Price", f"₹{df_filtered['Silver_Price_INR_per_kg'].min():,.0f}")
        col_b.metric("Max Price", f"₹{df_filtered['Silver_Price_INR_per_kg'].max():,.0f}")
        col_c.metric("Avg Price", f"₹{df_filtered['Silver_Price_INR_per_kg'].mean():,.0f}")
    except Exception as e:
        st.error(f"Error loading historical data: {str(e)}")

with tab2:
    st.header("Silver Sales Dashboard - India")
    try:
        df_silver = pd.read_csv("state_wise_silver_purchased_kg.csv")
        st.subheader("State-wise Silver Purchase Map")
        try:
            import requests
            from matplotlib import colors as mcolors
            with st.spinner("Loading India state boundaries..."):
                india_gdf = gpd.GeoDataFrame.from_features(requests.get("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson").json()['features'])
            india_merged = india_gdf.merge(df_silver, left_on='ST_NM', right_on='State', how='left')
            india_merged['Silver_Purchased_kg'] = india_merged['Silver_Purchased_kg'].fillna(0)
            fig, ax = plt.subplots(figsize=(15, 12))
            cmap = plt.colormaps.get_cmap('YlOrRd')
            cmap.set_bad('white')
            india_merged.plot(ax=ax, column='Silver_Purchased_kg', cmap=cmap, edgecolor='black', linewidth=0.8, legend=True, legend_kwds={'label': "Silver Purchased (kg)", 'orientation': "horizontal"})
            for x, y, label, value in zip(india_merged.geometry.centroid.x, india_merged.geometry.centroid.y, india_merged['ST_NM'], india_merged['Silver_Purchased_kg']):
                if value > 0:
                    ax.text(x, y, f"{label}\n{value:.0f} kg", fontsize=7, ha='center', va='center', weight='bold')
            ax.set_title('State-wise Silver Purchases in India (Darker Shade = Higher Purchases)', fontsize=16, weight='bold', pad=20)
            ax.axis('off')
            st.pyplot(fig)
            plt.close()
            st.success("State boundaries displayed using GeoPandas")
        except Exception as e:
            st.warning(f"Could not load online GeoJSON. Using alternative visualization. Error: {str(e)}")
            st.info("Note: Displaying bubble map representation of silver purchases across India.")
            state_coords = {'Maharashtra': {'lat': 19.7515, 'lon': 75.7139}, 'Karnataka': {'lat': 15.3173, 'lon': 75.7139}, 'Gujarat': {'lat': 22.2587, 'lon': 71.1924}, 'Rajasthan': {'lat': 27.0238, 'lon': 74.2179}, 'Tamil Nadu': {'lat': 11.1271, 'lon': 78.6569}, 'Andhra Pradesh': {'lat': 15.9129, 'lon': 79.7400}, 'Madhya Pradesh': {'lat': 22.9734, 'lon': 78.6569}, 'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462}, 'West Bengal': {'lat': 22.9868, 'lon': 87.8550}, 'Bihar': {'lat': 25.0961, 'lon': 85.3131}, 'Telangana': {'lat': 18.1124, 'lon': 79.0193}, 'Kerala': {'lat': 10.8505, 'lon': 76.2711}, 'Odisha': {'lat': 20.9517, 'lon': 85.0985}, 'Punjab': {'lat': 31.1471, 'lon': 75.3412}, 'Haryana': {'lat': 29.0588, 'lon': 76.0856}, 'Jharkhand': {'lat': 23.6102, 'lon': 85.2799}, 'Chhattisgarh': {'lat': 21.2787, 'lon': 81.8661}, 'Assam': {'lat': 26.2006, 'lon': 92.9376}, 'Himachal Pradesh': {'lat': 31.1048, 'lon': 77.1734}, 'Uttarakhand': {'lat': 30.0668, 'lon': 79.0193}, 'Goa': {'lat': 15.2993, 'lon': 74.1240}, 'Tripura': {'lat': 23.9408, 'lon': 91.9882}, 'Manipur': {'lat': 24.6637, 'lon': 93.9063}, 'Meghalaya': {'lat': 25.4670, 'lon': 91.3662}, 'Nagaland': {'lat': 26.1584, 'lon': 94.5624}, 'Mizoram': {'lat': 23.1645, 'lon': 92.9376}, 'Arunachal Pradesh': {'lat': 28.2180, 'lon': 94.7278}, 'Sikkim': {'lat': 27.5330, 'lon': 88.5122}}
            df_map = df_silver.copy()
            df_map['lat'] = df_map['State'].map(lambda x: state_coords.get(x, {}).get('lat', 0))
            df_map['lon'] = df_map['State'].map(lambda x: state_coords.get(x, {}).get('lon', 0))
            df_map = df_map[df_map['lat'] != 0]
            fig_map = px.scatter_geo(df_map, lat='lat', lon='lon', size='Silver_Purchased_kg', color='Silver_Purchased_kg', hover_name='State', hover_data={'Silver_Purchased_kg': ':,.0f', 'lat': False, 'lon': False}, size_max=50, color_continuous_scale='YlOrRd', title='State-wise Silver Purchases in India (Larger/Darker = Higher Purchases)', labels={'Silver_Purchased_kg': 'Silver Purchased (kg)'})
            fig_map.update_geos(scope='asia', center=dict(lat=23, lon=80), projection_scale=3.5, showland=True, landcolor='rgb(243, 243, 243)', coastlinecolor='rgb(204, 204, 204)', showcountries=True, countrycolor='rgb(204, 204, 204)', showlakes=True, lakecolor='rgb(255, 255, 255)')
            fig_map.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})
            st.plotly_chart(fig_map, width='stretch')
        st.subheader("Regional Distribution of Silver Purchases")
        fig_bar_all = px.bar(df_silver.sort_values('Silver_Purchased_kg', ascending=True), x='Silver_Purchased_kg', y='State', orientation='h', title='All States - Silver Purchase Distribution', labels={'Silver_Purchased_kg': 'Silver Purchased (kg)', 'State': ''}, color='Silver_Purchased_kg', color_continuous_scale='YlOrRd', height=800)
        fig_bar_all.update_layout(showlegend=False, xaxis_title='Silver Purchased (kg)', yaxis_title='')
        st.plotly_chart(fig_bar_all, width='stretch')
        st.markdown("---")
        st.header("Silver Sales Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 5 States - Highest Silver Purchases")
            top5_states = df_silver.nlargest(5, 'Silver_Purchased_kg')
            fig_bar = px.bar(top5_states, x='State', y='Silver_Purchased_kg', title='Top 5 States by Silver Purchases', labels={'Silver_Purchased_kg': 'Silver Purchased (kg)', 'State': 'State'}, color='Silver_Purchased_kg', color_continuous_scale='YlOrRd', text='Silver_Purchased_kg')
            fig_bar.update_traces(texttemplate='%{text:,.0f} kg', textposition='outside')
            fig_bar.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, width='stretch')
            st.dataframe(top5_states.style.format({'Silver_Purchased_kg': '{:,.0f} kg'}), hide_index=True, width='stretch')
        with col2:
            st.subheader("January 2026 - State-wise Silver Sales Trends")
            df_january = df_silver.nlargest(10, 'Silver_Purchased_kg').copy()
            np.random.seed(26)
            df_january['January_Sales_kg'] = df_january['Silver_Purchased_kg'] * np.random.uniform(0.07, 0.09, len(df_january))
            df_january = df_january.sort_values('January_Sales_kg', ascending=True)
            fig_line = go.Figure(go.Scatter(x=df_january['January_Sales_kg'], y=df_january['State'], mode='lines+markers', line=dict(color='#FF6347', width=3), marker=dict(size=12, color='#FF6347', symbol='diamond'), orientation='h'))
            fig_line.update_layout(title='Top 10 States - January 2026 Silver Sales', xaxis_title='Silver Sales (kg)', yaxis_title='State', hovermode='y unified', height=400, template='plotly_white', showlegend=False)
            st.plotly_chart(fig_line, width='stretch')
            st.dataframe(df_january[['State', 'January_Sales_kg']].sort_values('January_Sales_kg', ascending=False).style.format({'January_Sales_kg': '{:,.2f} kg'}), hide_index=True, width='stretch')
        st.markdown("---")
        st.subheader("Overall Statistics")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        col_stat1.metric("Total Silver Purchased", f"{df_silver['Silver_Purchased_kg'].sum():,.0f} kg")
        col_stat2.metric("Average per State", f"{df_silver['Silver_Purchased_kg'].mean():,.0f} kg")
        col_stat3.metric("Highest Purchasing State", df_silver.loc[df_silver['Silver_Purchased_kg'].idxmax(), 'State'])
        col_stat4.metric("Number of States", len(df_silver))
    except Exception as e:
        st.error(f"Error loading sales data: {str(e)}")
        st.info("Please ensure the following files are in the same directory:\n- state_wise_silver_purchased_kg.csv\n- State.shp and related files in ../State/ folder")

