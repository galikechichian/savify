from pytube import YouTube
import streamlit as st

video = YouTube("http://youtu.be/mUs97qXjw1M")
print(video.title)


def scrape_video():
    """
    Scrapes YouTube for the URL of the spotify song
    """
    print(0)

def dl_video(dest):
    """
    Downloads mp3 file to destination directory
    """
    print(0)

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")