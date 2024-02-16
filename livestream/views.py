from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import YouTubeURLSerializer
from chat_downloader.sites import YouTubeChatDownloader
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CheckLiveStatusView(APIView):
    @swagger_auto_schema(  # todo need fix wrong example responses, see #4
        operation_summary='透過輸入直播網址、video_id監控是否正在直播',
        operation_description='透過輸入直播網址、video_id監控是否正在直播',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'youtube_url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Youtube URL or video_id'
                )
            },
            responses={
                "200": openapi.Response(
                    description="example response",
                    examples={
                        "application/json": {
                            "live_status": "true"
                        }
                    }
                )
            },
        )
    )
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
