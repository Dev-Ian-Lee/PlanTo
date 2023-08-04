from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JobSerializer
from todo.serializers import TaskSerializer
from datetime import datetime
import requests
import configparser
import os

class JobList(APIView):
    # 채용공고 목록 출력
    def get(self, request, format = None):
        base_url = "https://oapi.saramin.co.kr/job-search?access-key="
        
        config = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
        config.read(config_file_path)
        
        api_key = config.get("API_KEYS", "SARAMIN_API_KEY")
        base_url += api_key
        
        # 사용자가 지역, 직무, 검색어를 검색 조건으로 사용 가능
        query_parameters = [
            "location",
            "position",
            "keywords"
        ]
        
        query_params = {}
        
        # 사용자가 보낸 요청에 검색 조건이 있을 경우, 해당 조건을 사람인 API로 보낼 요청의 query_params로 사용
        for parameter in query_parameters:
            parameter_value = request.query_params.get(parameter, "")
            
            if parameter_value:
                query_params[parameter] = parameter_value
        
        # 검색 결과 수 10개로 지정
        query_params["count"] = 10
        
        response = requests.get(base_url, params = query_params)
        
        # 응답 코드가 HTTP 200인 경우, JSON 형태로 데이터를 반환하고, 다른 값일 경우 해당 응답 코드와 에러 메시지 반환
        if response.status_code == 200:
            data = response.json()
        
            return Response(data)
        
        else:
            return Response({"error": "채용공고를 불러오는 데 실패했습니다."}, status = response.status_code)
        
    # 사용자가 채용공고 일정에 추가
    def post(self, request, format = None):
        try:
            data = request.data
            
            # Unix timestamp 형태로 전달되는 데이터를 datetime으로 변환
            due_date = data.get("due_date")
            if due_date:
                due_date = datetime.utcfromtimestamp(int(due_date)).date()
                data["due_date"] = due_date
            
            # 데이터 Deserialize
            job_serializer = JobSerializer(data = data)
            task_serializer = TaskSerializer(data = data)
            
            # 데이터가 유효한 경우, 채용공고를 사용자 모델에 추가 및 일정 모델로 변환
            if job_serializer.is_valid() and task_serializer.is_valid():
                job_serializer.save(owner = request.user)
                task_serializer.save(owner = request.user)
                
                return Response({"message": "채용공고가 추가되었습니다."}, status = status.HTTP_201_CREATED)
            
            return Response(job_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status = status.HTTP_400_BAD_REQUEST)
