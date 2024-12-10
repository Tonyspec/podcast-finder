from flask import Flask, render_template, request, render_template, redirect, url_for
from googleapiclient.discovery import build
from config import API_KEY

app = Flask(__name__)

api_key = API_KEY

# YouTube API setup
youtube = build('youtube', 'v3', developerKey=api_key)


def get_channel_videos(channel_name, max_results=10):
    channel_search = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id',
        maxResults=1
    ).execute()

    if channel_search['items']:
        channel_id = channel_search['items'][0]['id']['channelId']
        
        # Get channel description
        channel_info = youtube.channels().list(
            part="snippet",
            id=channel_id
        ).execute()
        
        channel_description = channel_info['items'][0]['snippet']['description'] if channel_info['items'] else "Description not available"

        videos = youtube.search().list(
            channelId=channel_id,
            part='id,snippet',
            maxResults=max_results,
            order="viewCount"
        ).execute()

        video_data = []
        for item in videos['items']:
            if item['id']['kind'] == "youtube#video":
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                # Fetch full video details for the full description
                video_details = youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                ).execute()
                
                if video_details['items']:
                    video_desc = video_details['items'][0]['snippet']['description']
                    stats = video_details['items'][0]['statistics']
                    video_data.append({
                        'title': video_title,
                        'description': video_desc,
                        'views': int(stats.get('viewCount', 0)),
                        'lik