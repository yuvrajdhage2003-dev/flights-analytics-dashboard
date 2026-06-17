import streamlit as st
import pandas as pd
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox(
    'Menu',
    ['Select One', 'Check Flights', 'Analytics']
)

if user_option == 'Check Flights':

    st.title('Check Flights')

    city = db.fetch_city_names()

    if not city:
        st.error("No cities found. Please check your database connection.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox('Source', sorted(city))

    with col2:
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):

        results = db.fetch_all_flights(source, destination)

        if results:

            df = pd.DataFrame(
                results,
                columns=[
                    'Airline',
                    'Route',
                    'Departure Time',
                    'Duration',
                    'Price'
                ]
            )

            st.dataframe(df, use_container_width=True)

        else:
            st.warning('No flights found.')

elif user_option == 'Analytics':

    st.title('Flight Analytics Dashboard')

    # Pie Chart

    airline, frequency = db.fetch_airline_frequency()

    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo='label+percent',
            textinfo='value'
        )
    )

    st.subheader('Airline Frequency')
    st.plotly_chart(fig, use_container_width=True)

    # Busy Airports

    city, frequency1 = db.busy_airport()

    airport_df = pd.DataFrame({
        'City': city,
        'Flights': frequency1
    })

    fig = px.bar(
        airport_df,
        x='City',
        y='Flights',
        title='Busiest Airports'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Daily Frequency

    date, frequency2 = db.daily_frequency()

    daily_df = pd.DataFrame({
        'Date': date,
        'Flights': frequency2
    })

    fig = px.line(
        daily_df,
        x='Date',
        y='Flights',
        title='Daily Flight Frequency',
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.title('Flight Analytics Project')
    st.write(
        'This application allows users to search flights and visualize flight data analytics.'
    )
