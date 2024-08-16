import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px


# Streamlit part

st.set_page_config(layout = "wide")
st.title("Airbnb Data Analysis")
st.write('')

def dataframe():
    df_airbnb = pd.read_csv("/home/abdul/Airbnb---DS_Airbnb-Analysis/airbnb_cleaned_data.csv")
    return df_airbnb

airbnb_df = dataframe()

with st.sidebar:
    options = option_menu("Main Menu", ["Home", "Overview", "About"])

if options == "Home":

    image_1 = Image.open("/home/abdul/Airbnb---DS_Airbnb-Analysis/airbnb-marketing.jpg")
    st.image(image_1)

    st.header("Analytical Summary")

    # About section with Streamlit text functions

    st.subheader("Overview")
    st.write(
        "This analysis focuses on Airbnb listings and their associated metrics to provide a detailed understanding of the rental market. We explore various aspects of Airbnb data to uncover trends and insights that can inform strategic decisions."
    )

    st.subheader("Key Points")
    st.write(
        "- **Data Sources**: The data is sourced from Airbnb's public listings and booking data.\n"
        "- **Visualization**: We use charts, maps, and graphs to visualize rental prices, booking trends, and other relevant metrics.\n"
        "- **Techniques**: The analysis involves exploratory data analysis (EDA), price trend analysis, and comparison across different regions and property types."
    )

    st.subheader("Objectives")
    st.write(
        "- Analyze the distribution of Airbnb listings by location and property type.\n"
        "- Examine pricing trends and seasonal variations.\n"
        "- Identify popular neighborhoods and factors influencing rental prices."
    )

if options == "Overview":
    tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(["Price Analysis","Avalability Analysis","Location Based Analysis", "Geosaptial Visualization", "Top Charts Analysis"])
    with tab_1:
        st.title("**Average review scores**")
        col1, col2 = st.columns(2)

        with col1:
            # Select a country
            country = st.selectbox("Select the Country", airbnb_df["country"].unique())

            # Filter DataFrame for the selected country
            df_country = airbnb_df[airbnb_df["country"] == country]
            df_country.reset_index(drop=True, inplace=True)

            # Select a room type
            room_type = st.selectbox("Select the Room Type", df_country["room_type"].unique())

            # Filter DataFrame for the selected room type
            df_filtered = df_country[df_country["room_type"] == room_type]
            df_filtered.reset_index(drop=True, inplace=True)

            # Group by property type and calculate the average review score
            df_avg_review = df_filtered.groupby("property_type")["review_scores"].mean().reset_index()

            # Create a bar chart using Plotly Express
            fig_review = px.bar(df_avg_review, x='property_type', y="review_scores",
                                title="Average review scores for Property types",
                                color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig_review)

        with col2:
            # Spacer to adjust layout
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            # Select a property type
            property_type = st.selectbox("Select the Property Type", df_filtered["property_type"].unique())

            # Filter DataFrame for the selected property type
            df_filtered_property = df_filtered[df_filtered["property_type"] == property_type].reset_index(drop=True)

            # Group the filtered data by host response time and calculate the sum of price and bedrooms
            df_pie_chart_data = df_filtered_property.groupby("host_response_time")[["price", "bedrooms"]].sum().reset_index()

            # Create a pie chart using Plotly Express
            fig_pie_chart = px.pie(df_pie_chart_data,
                                values="price",
                                names="host_response_time",
                                hover_data=["bedrooms"],
                                color_discrete_sequence=px.colors.sequential.Viridis_r,
                                title="PRICE DIFFERENCE BASED ON HOST RESPONSE TIME",
                                width=600,
                                height=500)

            # Display the Plotly chart in Streamlit
            st.plotly_chart(fig_pie_chart)

        col1, col2 = st.columns(2)

        with col1:
            # Dropdown for selecting host response time
            selected_host_response_time = st.selectbox("Select the Host Response Time", df_filtered_property["host_response_time"].unique())

            # Filter the DataFrame based on the selected host response time
            df_filtered_host_response = df_filtered_property[df_filtered_property["host_response_time"] == selected_host_response_time].reset_index(drop=True)

            # Group the data by bed type and calculate the sum of minimum_nights, maximum_nights, and price
            df_bed_type_grouped = df_filtered_host_response.groupby("bed_type")[["minimum_nights", "maximum_nights", "price"]].sum().reset_index()

            # Create a grouped bar chart
            fig_bed_type_bar = px.bar(
                df_bed_type_grouped,
                x="bed_type",
                y=["minimum_nights", "maximum_nights"],
                title="Minimum nights and maximum nights",
                hover_data=["price"],
                barmode="group",
                color_discrete_sequence=px.colors.sequential.Rainbow,
                width=600,
                height=500
            )

            # Display the bar chart
            st.plotly_chart(fig_bed_type_bar)

        with col2:
            # Spacer to adjust layout
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            # Group the data by bed type and calculate the sum of bedrooms, beds, accommodates, and price
            df_bed_type_summary = df_filtered_host_response.groupby("bed_type")[["bedrooms", "beds", "accommodates", "price"]].sum().reset_index()

            # Create a grouped bar chart
            fig_bed_type_bar_2 = px.bar(
                df_bed_type_summary,
                x="bed_type",
                y=["bedrooms", "beds", "accommodates"],
                title="Bedrooms and beds accommodates",
                hover_data=["price"],
                barmode="group",
                color_discrete_sequence=px.colors.sequential.Rainbow_r,
                width=600,
                height=500
            )

            # Display the bar chart
            st.plotly_chart(fig_bed_type_bar_2)

    with tab_2:
        st.title("**Availability Analysis**")
        col1, col2 = st.columns(2)

        with col1:
            # Dropdown for selecting a country
            selected_country_a = st.selectbox("Select the Country", airbnb_df["country"].unique(), key= "sel_cntry_a")

            # Filter DataFrame for the selected country
            df_country_filtered_a = airbnb_df[airbnb_df["country"] == selected_country_a].reset_index(drop=True)

            # Dropdown for selecting a property type
            selected_property_type_a = st.selectbox("Select the Property Type", df_country_filtered_a["property_type"].unique())

            # Filter DataFrame for the selected property type
            df_property_filtered_a = df_country_filtered_a[df_country_filtered_a["property_type"] == selected_property_type_a].reset_index(drop=True)

            # Create a sunburst chart for availability in the next 30 days
            fig_sunburst_30 = px.sunburst(
                df_property_filtered_a,
                path=["room_type", "bed_type", "is_location_exact"],
                values="availability_30",
                title="Availability in the Next 30 Days by Room and Bed Type",
                color_discrete_sequence=px.colors.sequential.Peach_r,
                width=600,
                height=500
            )
            st.plotly_chart(fig_sunburst_30)

        with col2:
            # Spacer to adjust layout
            for _ in range(10):
                st.write("")

            # Create a sunburst chart for availability in the next 60 days
            fig_sunburst_60 = px.sunburst(
                df_property_filtered_a,
                path=["room_type", "bed_type", "is_location_exact"],
                values="availability_60",
                title="Availability in the Next 60 Days by Room and Bed Type",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                width=600,
                height=500
            )
            st.plotly_chart(fig_sunburst_60)

        col1, col2 = st.columns(2)

        with col1:
            # Create a sunburst chart for availability in the next 90 days
            fig_sunburst_90 = px.sunburst(
                df_property_filtered_a,
                path=["room_type", "bed_type", "is_location_exact"],
                values="availability_90",
                title="Availability in the Next 90 Days by Room and Bed Type",
                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                width=600,
                height=500
            )
            st.plotly_chart(fig_sunburst_90)

        with col2:
            # Create a sunburst chart for availability in the next 365 days
            fig_sunburst_365 = px.sunburst(
                df_property_filtered_a,
                path=["room_type", "bed_type", "is_location_exact"],
                values="availability_365",
                title="Availability in the Next 365 Days by Room and Bed Type",
                color_discrete_sequence=px.colors.sequential.Greens_r,
                width=600,
                height=500
            )
            st.plotly_chart(fig_sunburst_365)

        # Dropdown for selecting room type
        selected_room_type_a = st.selectbox("Select the Room Type", df_property_filtered_a["room_type"].unique(), key= "room_type")

        # Filter DataFrame for the selected room type
        df_room_filtered_a = df_property_filtered_a[df_property_filtered_a["room_type"] == selected_room_type_a]

        # Group data by host response time and calculate the sum of availabilities and price
        df_availability_by_response = df_room_filtered_a.groupby("host_response_time")[["availability_30", "availability_60", "availability_90", "availability_365", "price"]].sum().reset_index()

        # Create a grouped bar chart for availability based on host response time
        fig_availability_bar = px.bar(
            df_availability_by_response,
            x="host_response_time",
            y=["availability_30", "availability_60", "availability_90", "availability_365"],
            title="Total Availability Based on Host Response Time",
            hover_data=["price"],
            barmode="group",
            color_discrete_sequence=px.colors.sequential.Rainbow_r,
            width=1000
        )
        st.plotly_chart(fig_availability_bar)

    with tab_3:
        st.title("**Location Analysis**")
        st.write("")

        # Dropdown for selecting a country
        selected_country_l = st.selectbox("Select the Country", airbnb_df["country"].unique(), key= "sel_cntry_l")

        # Filter DataFrame for the selected country
        df_country_filtered_l = airbnb_df[airbnb_df["country"] == selected_country_l].reset_index(drop=True)

        # Dropdown for selecting a property type
        selected_property_type_l = st.selectbox("Select the Property Type", df_country_filtered_l["property_type"].unique(), key= "prop_type")

        # Filter DataFrame for the selected property type
        df_property_filtered_l = df_country_filtered_l[df_country_filtered_l["property_type"] == selected_property_type_l].reset_index(drop=True)

        st.write("")

        # Calculate the difference between max and min prices
        differ_max_min = df_property_filtered_l['price'].max() - df_property_filtered_l['price'].min()

        def filter_by_price_range(selected_range):
            if selected_range == str(df_property_filtered_l['price'].min()) + ' to ' + str(differ_max_min * 0.30 + df_property_filtered_l['price'].min()) + ' (30% of the Value)':
                filtered_df = df_property_filtered_l[df_property_filtered_l["price"] <= differ_max_min * 0.30 + df_property_filtered_l['price'].min()]
            elif selected_range == str(differ_max_min * 0.30 + df_property_filtered_l['price'].min()) + ' to ' + str(differ_max_min * 0.60 + df_property_filtered_l['price'].min()) + ' (30% to 60% of the Value)':
                filtered_df = df_property_filtered_l[df_property_filtered_l["price"].between(differ_max_min * 0.30 + df_property_filtered_l['price'].min(), differ_max_min * 0.60 + df_property_filtered_l['price'].min())]
            elif selected_range == str(differ_max_min * 0.60 + df_property_filtered_l['price'].min()) + ' to ' + str(df_property_filtered_l['price'].max()) + ' (60% to 100% of the Value)':
                filtered_df = df_property_filtered_l[df_property_filtered_l["price"] >= differ_max_min * 0.60 + df_property_filtered_l['price'].min()]
            return filtered_df.reset_index(drop=True)
        

        # Radio button for selecting price range
        selected_price_range = st.radio(
            "Select the Price Range",
            [
                str(df_property_filtered_l['price'].min()) + ' to ' + str(differ_max_min * 0.30 + df_property_filtered_l['price'].min()) + ' (30% of the Value)',
                str(differ_max_min * 0.30 + df_property_filtered_l['price'].min()) + ' to ' + str(differ_max_min * 0.60 + df_property_filtered_l['price'].min()) + ' (30% to 60% of the Value)',
                str(differ_max_min * 0.60 + df_property_filtered_l['price'].min()) + ' to ' + str(df_property_filtered_l['price'].max()) + ' (60% to 100% of the Value)'
            ]
        )

        # Filter DataFrame based on the selected price range
        df_filtered = filter_by_price_range(selected_price_range)

        # Display the filtered DataFrame
        st.dataframe(df_filtered)

        # Correlation matrix of filtered data
        df_filtered_corr = df_filtered.drop(columns=[
            "listing_url", "name", "property_type", "room_type", "bed_type", "cancellation_policy",
            "images", "host_url", "host_name", "host_location", "host_response_time", "host_thumbnail_url",
            "host_response_rate", "host_is_superhost", "host_has_profile_pic", "host_picture_url", "host_neighbourhood",
            "host_identity_verified", "host_verifications", "street", "suburb", "government_area", "market",
            "country", "country_code", "location_type", "is_location_exact", "amenities"
        ]).corr()

        # Display the correlation matrix
        st.dataframe(df_filtered_corr)

        # Group data by accommodates and calculate sums
        df_grouped_by_accommodates = df_filtered.groupby("accommodates")[["cleaning_fee", "bedrooms", "beds", "extra_people"]].sum().reset_index()

        # Bar chart for accommodates
        fig_accommodates = px.bar(
            df_grouped_by_accommodates,
            x="accommodates",
            y=["cleaning_fee", "bedrooms", "beds"],
            title="Summary of Cleaning Fee, Bedrooms, and Beds by Accommodates",
            hover_data="extra_people",
            barmode="group",
            color_discrete_sequence=px.colors.sequential.Rainbow_r,
            width=1000
        )
        st.plotly_chart(fig_accommodates)

        # Dropdown for selecting room type
        selected_room_type_l = st.selectbox("Select the Room Type", df_filtered["room_type"].unique(), key= "room_typ_l")

        # Filter DataFrame for the selected room type
        df_room_filtered_l = df_filtered[df_filtered["room_type"] == selected_room_type_l]

        # Bar chart for market by street, host location, and host neighborhood
        fig_market = px.bar(
            df_room_filtered_l,
            x=["street", "host_location", "host_neighbourhood"],
            y="market",
            title="Market Distribution by Street, Host Location, and Host Neighbourhood",
            hover_data=["name", "host_name", "market"],
            barmode="group",
            orientation="h",
            color_discrete_sequence=px.colors.sequential.Rainbow_r,
            width=1000
        )
        st.plotly_chart(fig_market)

        # Bar chart for government area by superhost status, neighborhood, and cancellation policy
        fig_government_area = px.bar(
            df_room_filtered_l,
            x="government_area",
            y=["host_is_superhost", "host_neighbourhood", "cancellation_policy"],
            title="Government Area Analysis by Host Superhost Status, Neighborhood, and Cancellation Policy",
            hover_data=["guests_included", "location_type"],
            barmode="group",
            color_discrete_sequence=px.colors.sequential.Rainbow_r,
            width=1000
        )
        st.plotly_chart(fig_government_area)

    with tab_4:
        st.title("**Geospatial Visualization**")
        st.write("")

        # Scatter mapbox visualization
        fig_geospatial = px.scatter_mapbox(
            airbnb_df,
            lat='latitude',
            lon='longitude',
            color='price',
            size='accommodates',
            color_continuous_scale="rainbow",
            hover_name='name',
            range_color=(0, 49000),
            mapbox_style="carto-positron",
            zoom=1
        )
        fig_geospatial.update_layout(
            width=1150,
            height=800,
            title='Geospatial Distribution of Listings'
        )
        st.plotly_chart(fig_geospatial)

    with tab_5:
        st.title("**Detailed Price Analysis**")
        st.write("")

        # Select country and property type
        selected_country = st.selectbox("Select the Country", airbnb_df["country"].unique(), key= 'slc_cntry_D')
        filtered_by_country = airbnb_df[airbnb_df["country"] == selected_country]

        selected_property_type = st.selectbox("Select the Property Type", filtered_by_country["property_type"].unique(), key="prop_type_D")
        filtered_by_property_type = filtered_by_country[filtered_by_country["property_type"] == selected_property_type]
        filtered_by_property_type.reset_index(drop=True, inplace=True)

        # Sort by price
        sorted_by_price = filtered_by_property_type.sort_values(by="price")
        sorted_by_price.reset_index(drop=True, inplace=True)

        # Price aggregation by host_neighbourhood
        price_by_neighbourhood = pd.DataFrame(
            sorted_by_price.groupby("host_neighbourhood")["price"].agg(["sum", "mean"])
        )
        price_by_neighbourhood.reset_index(inplace=True)
        price_by_neighbourhood.columns = ["host_neighbourhood", "Total Price", "Average Price"]

        # Columns for visualization
        col1, col2 = st.columns(2)

        with col1:
            fig_neighbourhood_total_price = px.bar(
                price_by_neighbourhood,
                x="Total Price",
                y="host_neighbourhood",
                orientation='h',
                title="Total Price by Host Neighbourhood",
                width=600,
                height=800
            )
            st.plotly_chart(fig_neighbourhood_total_price)

        with col2:
            fig_neighbourhood_avg_price = px.bar(
                price_by_neighbourhood,
                x="Average Price",
                y="host_neighbourhood",
                orientation='h',
                title="Average Price by Host Neighbourhood",
                width=600,
                height=800
            )
            st.plotly_chart(fig_neighbourhood_avg_price)

        # Price aggregation by host_location
        price_by_location = pd.DataFrame(
            sorted_by_price.groupby("host_location")["price"].agg(["sum", "mean"])
        )
        price_by_location.reset_index(inplace=True)
        price_by_location.columns = ["host_location", "Total Price", "Average Price"]

        col1, col2 = st.columns(2)

        with col1:
            fig_location_total_price = px.bar(
                price_by_location,
                x="Total Price",
                y="host_location",
                orientation='h',
                title="Total Price by Host Location",
                color_discrete_sequence=px.colors.sequential.Bluered_r,
                width=600,
                height=800
            )
            st.plotly_chart(fig_location_total_price)

        with col2:
            fig_location_avg_price = px.bar(
                price_by_location,
                x="Average Price",
                y="host_location",
                orientation='h',
                title="Average Price by Host Location",
                color_discrete_sequence=px.colors.sequential.Bluered_r,
                width=600,
                height=800
            )
            st.plotly_chart(fig_location_avg_price)

        # Filter by room type and top 100 by price
        selected_room_type = st.selectbox("Select the Room Type", sorted_by_price["room_type"].unique(), key= 'room_type_D')
        filtered_by_room_type = sorted_by_price[sorted_by_price["room_type"] == selected_room_type]
        filtered_by_room_type.reset_index(drop=True, inplace=True)

        top_100_by_price = filtered_by_room_type.head(100)

        fig_top_100_price_details = px.bar(
            top_100_by_price,
            x="name",
            y="price",
            color="price",
            color_continuous_scale="rainbow",
            range_color=(0, top_100_by_price["price"].max()),
            title="Price Details with Minimum Nights, Maximum Nights, and Accommodates",
            width=1200,
            height=800,
            hover_data=["minimum_nights", "maximum_nights", "accommodates"]
        )
        st.plotly_chart(fig_top_100_price_details)

        fig_top_100_bedroom_details = px.bar(
            top_100_by_price,
            x="name",
            y="price",
            color="price",
            color_continuous_scale="greens",
            range_color=(0, top_100_by_price["price"].max()),
            title="Price Details with Bedrooms, Beds, Accommodates, and Bed Type",
            width=1200,
            height=800,
            hover_data=["accommodates", "bedrooms", "beds", "bed_type"]
        )
        st.plotly_chart(fig_top_100_bedroom_details)




if options == "About":

    st.header("ABOUT THIS PROJECT")

    st.subheader(":orange[1. Data Collection:]")
    st.write('''***Acquire data from Airbnb's public API or other available sources.
        Gather detailed information on listings, hosts, reviews, pricing, and geographical data.***''')
    
    st.subheader(":orange[2. Data Cleaning and Preprocessing:]")
    st.write('''***Clean and preprocess the data to address missing values and outliers, ensuring high data quality.
        Standardize formats, handle duplicates, and convert data types as necessary.***''')
    
    st.subheader(":orange[3. Exploratory Data Analysis (EDA):]")
    st.write('''***Perform exploratory data analysis to uncover distribution patterns and insights within the data.
        Examine relationships between variables and identify key trends.***''')
    
    st.subheader(":orange[4. Visualization:]")
    st.write('''***Develop visualizations to effectively showcase key metrics and trends.
        Utilize charts, graphs, and maps to present information clearly.
        Consider using visualization libraries such as Matplotlib, Seaborn, or Plotly.***''')
    
    st.subheader(":orange[5. Geospatial Analysis:]")
    st.write('''***Leverage geospatial analysis to explore the geographic distribution of listings.
        Identify popular neighborhoods, analyze area characteristics, and visualize pricing differences across locations.***''')

