import streamlit as st
from streamlit_folium import folium_static
import folium
from PIL import Image
import streamlit.components.v1 as components
import subprocess

# Sample university data with coordinates
universities = [
    {"name": "Harvard University", "location": "Cambridge, MA", "state": "MA", "country": "USA", "ranking": 1, "coordinates": (42.373611, -71.109733)},
    {"name": "Stanford University", "location": "Stanford, CA", "state": "CA", "country": "USA", "ranking": 2, "coordinates": (37.4275, -122.1697)},
    {"name": "Massachusetts Institute of Technology (MIT)", "location": "Cambridge, MA", "state": "MA", "country": "USA", "ranking": 3, "coordinates": (42.3601, -71.0942)},
    {"name": "University of California, Berkeley", "location": "Berkeley, CA", "state": "CA", "country": "USA", "ranking": 4, "coordinates": (37.8719, -122.2585)},
    {"name": "University of Washington", "location": "Seattle, WA", "state": "WA", "country": "USA", "ranking": 5, "coordinates": (47.6553, -122.3035)},
    {"name": "University of Toronto", "location": "Toronto, ON", "state": "ON", "country": "Canada", "ranking": 6, "coordinates": (43.6629, -79.3957)},
    {"name": "University of Oxford", "location": "Oxford", "state": "", "country": "UK", "ranking": 7, "coordinates": (51.754816, -1.254367)},
    {"name": "Indian Institute of Technology (IIT) Bombay", "location": "Mumbai", "state": "MH", "country": "India", "ranking": 8, "coordinates": (19.1334, 72.9133)},
    {"name": "Indian Institute of Technology (IIT) Delhi", "location": "New Delhi", "state": "DL", "country": "India", "ranking": 9, "coordinates": (28.5465, 77.2732)},
    {"name": "Technical University of Munich", "location": "Munich", "state": "", "country": "Germany", "ranking": 10, "coordinates": (48.1351, 11.5820)},
]

# Function to display university information with details button
def display_university_info(name, location, ranking, image_path, details_button_id):
    # Resize the image
    resized_img_col2 = resize_image(image_path, height=300)

    # Display the university information
    st.image(resized_img_col2, caption=name, use_column_width=True)
    st.markdown(f"**{name}**")
    st.write(f"Location: {location}")
    st.write(f"Ranking: {ranking}")

    # Add a button to show details
    details_button = st.button("Univ Details", key=details_button_id)

    # Check if the button is clicked
    if details_button:
        # Open the university details page in a new browser window
        subprocess.run(["streamlit", "run", "univ_details.py"])
    
    # Add a horizontal line for separation
    st.markdown("---")


# Sample images for universities
image_folder = "images/"
univ_images = [f"{image_folder}univ{idx + 1}.jpg" for idx in range(len(universities))]


# Function to resize the image
def resize_image(image_path, height):
    original_image = Image.open(image_path)
    original_width, original_height = original_image.size
    width = int((height / original_height) * original_width)
    resized_image = original_image.resize((width, height))
    return resized_image

# Function to display map
def display_us_map(filtered_universities):
    # You can customize this map according to your needs
    map_center = [37.7749, -122.4194]  # Coordinates for San Francisco, CA
    m = folium.Map(location=map_center, zoom_start=4)

    # Add markers for each university with actual coordinates
    for university in filtered_universities:
        if "coordinates" in university:
            folium.Marker(location=university["coordinates"], popup=university["name"]).add_to(m)

    return m

# Streamlit app
def main():
    # Display the image instead of the title
    image_path = "images/univoyaj.png"
    st.image(image_path, use_column_width=False)

    # Add a dropdown for selecting the state in the left sidebar
    selected_state = st.sidebar.selectbox("Select State", ["All"] + sorted(set([uni["state"] for uni in universities])))

    # Add a dropdown for selecting the country in the left sidebar
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(set([uni["country"] for uni in universities])))

    # Add a button to execute graphs.py
    if st.sidebar.button("Show Analytics"):
        subprocess.run(["streamlit", "run", "graphs.py"])

    # Your existing code here...

    # Filter universities based on selected state and country
    filtered_universities = universities
    if selected_state != "All":
        filtered_universities = [uni for uni in filtered_universities if uni["state"] == selected_state]
    if selected_country != "All":
        filtered_universities = [uni for uni in filtered_universities if uni["country"] == selected_country]

    # Layout: 3 columns - First 2 for universities, the third for the map
    col1, col2, col3 = st.columns([3, 3, 3])

    # Display the top 5 universities in the first two columns
    for idx in range(0, len(filtered_universities), 2):
        with col1:
            img_num_col1 = filtered_universities[idx]["ranking"] - 1  # Adjust the index
            details_button_id_col1 = f"details_button_{idx}"
            display_university_info(
                filtered_universities[idx]["name"],
                filtered_universities[idx]["location"],
                filtered_universities[idx]["ranking"],
                univ_images[img_num_col1],
                details_button_id_col1
            )

        # Check if there's another university for the second column
        if idx + 1 < len(filtered_universities):
            with col2:
                img_num_col2 = filtered_universities[idx + 1]["ranking"] - 1  # Adjust the index
                details_button_id_col2 = f"details_button_{idx + 1}"
                display_university_info(
                    filtered_universities[idx + 1]["name"],
                    filtered_universities[idx + 1]["location"],
                    filtered_universities[idx + 1]["ranking"],
                    univ_images[img_num_col2],
                    details_button_id_col2
                )

    # Display the map in the third column with increased width
    with col3:
        st.header("University Locations Map")
        folium_map = display_us_map(filtered_universities)
        folium_static(folium_map, width=1000, height=800)  # Adjust the width and height as needed

if __name__ == "__main__":
    main()