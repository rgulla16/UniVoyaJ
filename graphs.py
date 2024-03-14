import streamlit as st
import pandas as pd
import altair as alt

# Read data from CSV file
file_path = 'univ_rank_clean.csv'  # Replace with your actual path
univ_df = pd.read_csv(file_path)

# Convert 'National Rank' and 'World Rank' columns to integers
univ_df['National Rank'] = pd.to_numeric(univ_df['National Rank'], errors='coerce')
univ_df['World Rank'] = pd.to_numeric(univ_df['World Rank'], errors='coerce')

# Set default rank values
default_rank_range = 100

# Sidebar controls
st.sidebar.title("Filter Data")

# Dropdown for selecting country
selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(univ_df['Country'].unique()))

# Dropdown for selecting World Rank range
world_rank_ranges = [0, 100, 250, 500, 1000]
selected_world_rank_range = st.sidebar.selectbox("Select World Rank Range", world_rank_ranges, index=world_rank_ranges.index(default_rank_range))

# Dropdown for selecting National Rank range
national_rank_ranges = [0, 100, 250, 500, 1000]
selected_national_rank_range = st.sidebar.selectbox("Select National Rank Range", national_rank_ranges, index=national_rank_ranges.index(default_rank_range))

# Filter data based on selected options
filtered_df_country = univ_df.copy()
filtered_df_world_rank = univ_df.copy()
filtered_df_national_rank = univ_df.copy()

# Apply country filter
if selected_country != "All":
    filtered_df_country = filtered_df_country[filtered_df_country['Country'] == selected_country]

# Apply World Rank filter
filtered_df_world_rank = filtered_df_world_rank[filtered_df_world_rank['World Rank'] <= selected_world_rank_range]

# Apply National Rank filter
filtered_df_national_rank = filtered_df_national_rank[filtered_df_national_rank['National Rank'] <= selected_national_rank_range]

# Bar graph with countries on x-axis and the number of universities on the y-axis
country_univ_count = (
    alt.Chart(filtered_df_country.groupby('Country').size().reset_index(name='Num of Universities'))
    .mark_bar()
    .encode(
        x=alt.X('Country:N', title='Country'),
        y=alt.Y('Num of Universities:Q', title='Number of Universities'),
        tooltip=['Country', 'Num of Universities']
    )
    .properties(
        title='Number of Universities per Country'
    )
)

# Bar graph with countries on x-axis and the number of universities on the y-axis for World Rank
world_rank_bar = (
    alt.Chart(filtered_df_world_rank.groupby('Country').size().reset_index(name='Num of Universities'))
    .mark_bar()
    .encode(
        x=alt.X('Country:N', title='Country'),
        y=alt.Y('Num of Universities:Q', title='Number of Universities'),
        tooltip=['Country', 'Num of Universities']
    )
    .properties(
        title=f'Number of Universities per Country (World Rank <= {selected_world_rank_range})'
    )
)

# Bar graph with countries on x-axis and the number of universities on the y-axis for National Rank
national_rank_bar = (
    alt.Chart(filtered_df_national_rank.groupby('Country').size().reset_index(name='Num of Universities'))
    .mark_bar()
    .encode(
        x=alt.X('Country:N', title='Country'),
        y=alt.Y('Num of Universities:Q', title='Number of Universities'),
        tooltip=['Country', 'Num of Universities']
    )
    .properties(
        title=f'Number of Universities per Country (National Rank <= {selected_national_rank_range})'
    )
)

# Display visualizations
image_path = "images/univoyaj.png"
st.image(image_path, use_column_width=False)

st.subheader("Number of Universities per Country")
st.altair_chart(country_univ_count, use_container_width=True)

st.subheader("Number of Universities per Country (World Rank Range)")
st.altair_chart(world_rank_bar, use_container_width=True)

st.subheader("Number of Universities per Country (National Rank Range)")
st.altair_chart(national_rank_bar, use_container_width=True)
