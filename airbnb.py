import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu

file_path = "C:/Users/durga prasad/Downloads/output_file (1).xlsx"

# Read Excel file into a DataFrame
df = pd.read_excel(file_path)
# Streamlit app
st.set_page_config(layout="wide")

selected = option_menu(None,
                       options = ["About","Analysis"],
                       icons = ["house""bar-chart"],
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


if selected == "Analysis":
    Property_type = df['property_type'].unique().tolist()
    selected_properties = st.multiselect('Select property type', Property_type)

    # Filter the DataFrame based on the selected Property_type
    filtered_prop_df = df[df['property_type'].isin(selected_properties)]

    # Create a multiselect for choosing room_type in the selected Property_type
    selected_room_type = st.multiselect('Select room type', filtered_prop_df['room_type'].unique())

    # Filter the DataFrame based on the selected room_type
    filtered_room_df = filtered_prop_df[filtered_prop_df['room_type'].isin(selected_room_type)]

    selected_neighborhoods = st.multiselect('Select Neighborhoods', filtered_room_df['host_neighbourhood'].unique())

    # Filter the DataFrame based on the selected neighborhoods
    filtered_df = filtered_room_df[filtered_room_df['host_neighbourhood'].isin(selected_neighborhoods)]

    # Check if both properties, room_type, and neighborhoods are selected
    if selected_properties and selected_room_type and selected_neighborhoods:
        availability_columns = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
        availability_df = filtered_df[availability_columns].mean().reset_index()
        availability_df.columns = ['Availability', 'Average Availability']

        col3, col4 = st.columns(2)
        with col3:
            st.write('Selected property:', selected_properties)
            st.write('Selected room type:', selected_room_type)
            st.write('Selected neighborhoods:', selected_neighborhoods)
            st.write('Availability of rooms:')
            st.write(availability_df)

        with col4:
            fig = px.bar(
                availability_df,
                x='Availability',  # X-axis: Availability column names
                y='Average Availability',  # Y-axis: Average Availability values
                labels={'Average Availability': 'Average Availability'},
                title=f'Avaliable days based on {selected_properties} room type, {selected_room_type} property type, and {selected_neighborhoods} neighborhood'
            )

            st.plotly_chart(fig)

            #top 10 hosts based on reviews
        with col3:
            best_hosts_df = filtered_df[['host_name','rating']].groupby('host_name')['rating'].median().nlargest(10).reset_index()
            top_10_hosts = best_hosts_df.head(10)
            st.write('Top 10 hosts based on rating')
            st.write(top_10_hosts)

        with col4:
            
            # Create the bar chart using Plotly Express
            fig = px.bar(top_10_hosts, x='host_name', y='rating', color='rating',
                        labels={'rating': 'Median Rating'},
                        title='Top 10 Hosts Based on Rating')
            fig.update_layout(xaxis_title='Host Name', yaxis_title='Median Rating')
            st.plotly_chart(fig)

        with col3:
            filtered_df = filtered_df.sort_values(by='price', ascending=True)

            # Get the top 10 hosts
            top_10_low_price_hosts = filtered_df.head(10)

            # Create a bar chart using Plotly Express
            fig = px.bar(
                top_10_low_price_hosts,
                x='host_name',
                y='price',
                labels={'price': 'Price'},
                title=f'Top 10 Hosts based on price on selected {selected_properties} room type, {selected_room_type} property type, and {selected_neighborhoods} neighborhood')

            # Display the bar chart in Streamlit
            st.plotly_chart(fig)
        with col4:
            st.write("Top 10 Neighborhoods based on Minimum Price for Room Type")
            top_10_neighborhoods = filtered_room_df.groupby('host_neighbourhood')['price'].min().nlargest(10).reset_index()
            
            # Create a bar chart with Plotly Express
            fig = px.bar(top_10_neighborhoods, x='host_neighbourhood', y='price', color='price',
                        labels={'price': 'Minimum Price'},
                        title=f'Top 10 Neighborhoods with Minimum Price for {selected_room_type} Room Type')
            fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Minimum Price')
            st.plotly_chart(fig)
    else:
        st.warning('Please select both a country and a city.')


    


