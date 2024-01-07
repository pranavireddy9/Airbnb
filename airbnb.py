import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu

file_path = "C:/Users/durga prasad/Desktop/airbnbData.xlsx"

# Read Excel file into a DataFrame
df = pd.read_excel(file_path)
# Streamlit app
st.set_page_config(layout="wide")

selected = option_menu(None,
                       options = ["About","Analysis","Insights"],
                       icons = ["house","toggles","bar-chart"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-4px" ,"--hover-color": "#800080"},
                               "nav-link-selected": {"background-color": "#800080"},
                               "nav": {"background-color": "#E6E6FA"}})


# ABOUT PAGE
if selected == "About":
    col1, col2, = st.columns(2)
    col1.image("https://tse4.mm.bing.net/th?id=OIP.nr8NdjWR9W9WGpncu4lOhQHaFj&pid=Api&P=0&h=180", width=500)
    with col2:
        st.subheader(
            "This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")


if selected=="Analysis":

    countries=df['country'].unique().tolist()
    selected_countries = st.multiselect('Select Countries', countries)

    # Filter the DataFrame based on the selected countries
    filtered_df = df[df['country'].isin(selected_countries)]

    # Create a multiselect for choosing states in the selected countries
    selected_states = st.multiselect('Select States', filtered_df['state'].unique())

    # Filter the DataFrame based on the selected states
    filtered_st_df = filtered_df[filtered_df['state'].isin(selected_states)]

    selected_neighborhoods = st.multiselect('Select Neighborhoods', filtered_st_df['host_neighbourhood'].unique())

    filtered_df = filtered_st_df[filtered_st_df['host_neighbourhood'].isin(selected_neighborhoods)]



    # Check if both country_name and selected_city are selected
    if selected_countries and selected_states and selected_neighborhoods:
        room_type_df = filtered_df.groupby(['room_type', 'state', 'host_neighbourhood'])['price'].mean().reset_index()
        room_type_df1 = filtered_df.groupby(['room_type', 'state', 'host_neighbourhood'])['price'].agg(['mean', 'sum', 'min', 'max']).reset_index()

        col3, col4, = st.columns(2)
        with col3:
            st.write('Selected Country:', selected_countries)
            st.write('Selected City:', selected_states)
            st.write('Prices by Room Type:')
            st.write(room_type_df1)
            
        with col4:
            fig = px.scatter(room_type_df, x='room_type', y='price', color='host_neighbourhood',
                            labels={'price': 'Average Price'},
                            title='Average Price by Room Type and Neighbourhood')
            
            st.plotly_chart(fig)
        #availability

        availability_columns = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
        average_availability_df = filtered_df.groupby(['room_type', 'state', 'host_neighbourhood'])[availability_columns].mean().reset_index()
        with col3:
            availability_columns = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
            average_availability_df = filtered_df.groupby(['room_type', 'state', 'host_neighbourhood'])[availability_columns].mean().reset_index()

            st.write('Average Availability by Room Type and Neighbourhood:')
            st.write(average_availability_df)

        with col4:
            melted_df = pd.melt(average_availability_df, id_vars=['room_type', 'state', 'host_neighbourhood'], var_name='availability_period', value_name='average_availability')

            # Create the bar chart using Plotly Express
            fig_availability = px.bar(melted_df, x='room_type', y='average_availability', color='availability_period',
                                    facet_col='host_neighbourhood', facet_col_wrap=2,
                                    labels={'average_availability': 'Average Availability'},
                                    title='Average Availability by Room Type and Neighbourhood')

            st.plotly_chart(fig_availability)

            neighborhood_df = filtered_df[filtered_df['host_neighbourhood'].isin(selected_neighborhoods)]
            host_listings_count = neighborhood_df.groupby('host_name')['host_total_listings_count'].sum().reset_index()
            host_listings_count = host_listings_count.sort_values(by='host_total_listings_count', ascending=False)
            top_10_hosts = host_listings_count.head(10)
            fig = px.bar(top_10_hosts, x='host_name', y='host_total_listings_count',
                        labels={'host_total_listings_count': 'Total Listings Count'},
                        title=f'Top 10 Hosts in {selected_neighborhoods} based on Total Listings Count')
            st.plotly_chart(fig)


            # Group by host_name and calculate the average price for each host
            host_min_price = neighborhood_df.groupby('host_name')['price'].min().reset_index()
            host_min_price = host_min_price.sort_values(by='price', ascending=True)
            top_10_hosts = host_min_price.head(10)
            fig = px.bar(top_10_hosts, x='host_name', y='price',
                        labels={'price': 'Minimum Price'},
                        title=f'Top 10 Hosts in {selected_neighborhoods[0]} based on minimum Price')

            # Show the Plotly chart
            st.plotly_chart(fig)
        with col3:
            st.write("Top 10 Neighborhoods based on Minimum Price for Room Type")
            selected_room_types = df['room_type'].unique().tolist()
            roomType=st.selectbox('select room type',selected_room_types)
            room_type_df = filtered_st_df[filtered_st_df['room_type']==roomType]
            neighborhood_min_price = room_type_df.groupby(['host_neighbourhood', 'room_type'])['price'].min().reset_index()
            neighborhood_min_price = neighborhood_min_price.sort_values(by='price', ascending=True)
            top_10_neighborhoods = neighborhood_min_price.groupby('room_type').head(10)
            fig = px.bar(top_10_neighborhoods, x='host_neighbourhood', y='price', color='room_type',
                        labels={'price': 'Minimum Price'},
                        title='Top 10 Neighborhoods based on Minimum Price for Each Room Type')
            st.plotly_chart(fig)
    else:
        st.warning('Please select both a country and a city.')


    


