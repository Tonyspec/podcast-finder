from googleapiclient.discovery import build
import pandas as pd

# Set up the API
api_key = 'AIzaSyDmD_9GM41wuFwtcR3vBwgHLK4SxSGdWxU'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_videos(channel_name, max_results=10):
    # First, search for the channel
    channel_search = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id',
        maxResults=1
    ).execute()

    if channel_search['items']:
        channel_id = channel_search['items'][0]['id']['channelId']
        # Now get videos from that channel
        videos = youtube.search().list(
            channelId=channel_id,
            part='id,snippet',
            maxResults=max_results,
            order="viewCount"  # This orders by popularity (views)
        ).execute()

        video_data = []
        for item in videos['items']:
            if item['id']['kind'] == "youtube#video":
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                # Fetch detailed stats for each video
                video_stats = youtube.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()
                
                stats = video_stats['items'][0]['statistics']
                video_data.append({
                    'title': video_title,
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0))
                })

        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(video_data)
        df = df.sort_values('views', ascending=False)  # Sort by views for popularity
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if channel not found

# Example usage
popular_videos = get_channel_videos('Matt Walsh', max_results=5)
print(popular_videos)