from rest_framework.views import APIView
from rest_framework.response import Response
from chat_downloader.sites import YouTubeChatDownloader
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def extract_video_id(youtube_url):
    video_id = youtube_url
    if "watch?v=" in youtube_url:
        video_id = youtube_url.split("watch?v=")[1]  # 直接從瀏覽器複製網址
    elif "youtu.be/" in youtube_url:  # 按"Share"時會產生youtu.be/
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
    elif "/live/" in youtube_url:  # 直播按"Share"時會產生youtube.com/live/<video id>
        video_id = youtube_url.split("/live/")[1].split("?")[0]
    return video_id


class CheckLiveStatusView(APIView):
    @swagger_auto_schema(  # todo need fix wrong example responses, see #4
        operation_summary="透過輸入直播網址、video_id監控是否正在直播",
        operation_description="透過輸入直播網址、video_id監控是否正在直播",
        manual_parameters=[
            openapi.Parameter(
                name="youtube_url",
                in_=openapi.IN_QUERY,
                description="youtube URL or video_id",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request):
        youtube_url = request.query_params.get("youtube_url", "")
        if not youtube_url:
            return Response({"detail": "YouTube 網址不能為空。"}, status=400)

        video_id = extract_video_id(youtube_url)
        try:
            video_data = YouTubeChatDownloader().get_video_data(video_id)
            if not video_data.get("original_video_id"):
                return Response({"detail": "YouTube 直播不存在。"}, status=400)
            video_id = video_data.get("original_video_id")
            response_data = {
                "title": video_data.get("title"),
                "channel_name": video_data.get("author"),
                "channel_id": video_data.get("author_id"),
                "video_id": video_id,
                "URL": f"https://www.youtube.com/watch?v={video_id}",
                "live_status": video_data.get("status") == "live",
            }
            return Response(response_data)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
