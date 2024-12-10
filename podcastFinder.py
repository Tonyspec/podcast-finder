from flask import Flask, render_template, request
from googleapiclient.discovery import build
import pandas as pd

app = Flask(__name__)

# Your API key
api_key = 'AIzaSyDmD_9GM41wuFwtcR3vBwgHLK4SxSGdWxU'

# YouTube API setup
youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_videos(channel_name, max_results=10):
    # Channel search logic as before
    channel_search = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id',
        maxResults=1
    ).execute()

    if channel_search['items']:
        channel_id = channel_search['items'][0]['id']['channelId']
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

        df = pd.DataFrame(video_data)
        return df.to_dict('records')
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        channel_name = request.form['channel_name']
        top_videos = get_channel_videos(channel_name)
        return render_template('index.html', videos=top_videos)
    return render_template('index.html', videos=None)

if __name__ == '__main__':
    app.run(debug=True)