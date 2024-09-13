from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Crew, Tag
from .serializers import CrewSerializer, TagSeirializer

# Create your views here.

class CrewJoin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        crew_id = request.data.get('crew_id')
        crew = get_object_or_404(Crew, id=crew_id)

        if crew.participants.count() < crew.max_participants:

            if request.user not in crew.participants.all():

                if crew.participants.count() == crew.max_participants-1:
                    crew.status = '진행중'
                    crew.save()
                
                crew.participants.add(request.user)
                return Response({"message":"크루 참가 완료되었습니다."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"이미 참가 중인 크루입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messsage":"참가 인원이 마감되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
