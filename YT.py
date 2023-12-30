import streamlit as st
from googleapiclient.discovery import build

# Function to display channel videos and name
def display_channel_videos_and_name(api_key, channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_request = youtube.channels().list(part='snippet,contentDetails', id=channel_id)
        channel_response = channel_request.execute()

        channel_name = channel_response['items'][0]['snippet']['title']
        st.write(f"Channel Name: {channel_name}")

        playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        playlist_request = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50)
        playlist_response = playlist_request.execute()

        videos = playlist_response['items']
        st.write(f"Number of Videos: {len(videos)}")
        for video in videos:
            title = video['snippet']['title']
            st.write(title)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main function for Streamlit app
def main():
    background_gif = "https://i.gifer.com/g3Ys.gif"

    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url({background_gif});
                background-size: cover;
            }}
            .main, .sidebar .sidebar-content {{
                background-color: rgba(255, 255, 255, 0.8);
            }}
            .main * {{
                color: black;
            }}
            .sidebar .sidebar-content * {{
                color: white;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    st.sidebar.markdown("## Settings")
    api_key = st.sidebar.text_input("YouTube API Key", "")
    channel_id = st.sidebar.text_input("Channel ID", "")

    st.title("YT Video Uploader🎥")
    st.markdown("### Explore and Discover Videos from YouTube Channels")

    if st.sidebar.button("Show Videos"):
        if api_key and channel_id:
            with st.spinner('Fetching videos and channel info...'):
                display_channel_videos_and_name(api_key, channel_id)
        else:
            st.sidebar.error("Please enter both API Key and Channel ID")

if __name__ == "__main__":
    main()
