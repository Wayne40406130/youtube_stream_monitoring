from rest_framework import serializers

class YouTubeURLSerializer(serializers.Serializer):
    youtube_url = serializers.CharField(max_length=1000)

    def validate_youtube_url(self, value):
        video_id = self.extract_video_id(value)
        return video_id

    def extract_video_id(self, youtube_url):
        video_id = youtube_url
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("watch?v=")[1] # 直接從瀏覽器複製網址
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0] # 按"Share"時會產生youtu.be/
        elif "/live/" in youtube_url:
            video_id = youtube_url.split("/live/")[1].split("?")[0] # 直播按"Share"時會產生youtube.com/live/<video id>
        return video_id
