import streamlit as st
import pandas as pd

# Load university details from CSV
df = pd.read_csv('univ_details.csv')

# # Create Streamlit app
# st.title("University Details")
# Display the image instead of the title
image_path = "images/univoyaj.png"
st.image(image_path, use_column_width=False)

# Navigation buttons
prev_button, next_button = st.columns(2)

# Store the current index in the session state
if 'index' not in st.session_state:
    st.session_state.index = 0

# Display university information
st.write(f"## {df['University Name'][st.session_state.index]}")
image_path = f"images/univ{st.session_state.index + 1}.jpg"
st.image(image_path, caption=f"Image for {df['University Name'][st.session_state.index]}")

# Display other details
st.write(f"**Region:** {df['Region'][st.session_state.index]}")
st.write(f"**Country:** {df['Country'][st.session_state.index]}")
st.write(f"**Found Year:** {df['Found Year'][st.session_state.index]}")
st.write(f"**Address:** {df['Address'][st.session_state.index]}")
st.write(f"**Website:** {df['Website'][st.session_state.index]}")
st.write(f"**Introduction:** {df['Introduction'][st.session_state.index]}")

# Update index on button click
if prev_button.button("Previous") and st.session_state.index > 0:
    st.session_state.index -= 1

if next_button.button("Next") and st.session_state.index < len(df) - 1:
    st.session_state.index += 1
