from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .saramin.api_access import get_saramin_response
from .serializers import JobSerializer 
from .models import Job
from todo.serializers import TaskSerializer
from datetime import datetime

class JobList(ListCreateAPIView):
    serializer_class = JobSerializer
    
    # 채용공고 목록 출력
    def get(self, request, format = None):
        response = get_saramin_response(request.query_params)
        
        # 응답 코드가 HTTP 200인 경우, JSON 형태로 데이터를 반환하고, 다른 값일 경우 해당 응답 코드와 에러 메시지 반환
        if response.status_code == 200:
            data = response.json()

            return Response(data)

        else:
            return Response({"error": "채용공고를 불러오는 데 실패했습니다."}, status = response.status_code)

    # 채용공고 일정으로 추가
    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            due_date = data.get("due_date")
            if due_date:
                due_date = datetime.utcfromtimestamp(int(due_date)).date()
                data["due_date"] = due_date

            job_serializer = self.get_serializer(data = data)
            task_serializer = TaskSerializer(data = data)

            if job_serializer.is_valid() and task_serializer.is_valid():
                job_serializer.save(owner = request.user)
                task_serializer.save(owner = request.user)

                return Response({"message": "채용공고가 추가되었습니다."}, status = status.HTTP_201_CREATED)

            return Response(job_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_400_BAD_REQUEST)