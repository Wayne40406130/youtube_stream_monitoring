from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import YouTubeURLSerializer
from chat_downloader.sites import YouTubeChatDownloader


class CheckLiveStatusView(APIView):
    def post(self, request):
        serializer = YouTubeURLSerializer(data=request.data)
        if serializer.is_valid():
            video_id = serializer.validated_data['youtube_url']
        else:
            return Response(serializer.errors, status=400)
        try:
            video_data = YouTubeChatDownloader().get_video_data(video_id)
            if video_data.get('status') == 'live':
                return Response({'live_status': True})
            else:
                return Response({'live_status': False})
        except Exception as e:
            return Response({'live_status': False})
