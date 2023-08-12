import requests
import configparser
import os

def get_saramin_response(parameter_injection):
    base_url = "https://oapi.saramin.co.kr/job-search?access-key="
    
    config = configparser.ConfigParser()
    
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    config_file_path = os.path.join(root_directory, "config.ini")
    config.read(config_file_path)
    
    api_key = config.get("API_KEYS", "SARAMIN_API_KEY")
    base_url += api_key
    
    # 사용자가 지역, 업종, 키워드를 검색 조건으로 사용 가능
    query_parameters = [
        "location",
        "industry",
        "keywords"
    ]
    
    query_params = {}
    
    # 사용자가 보낸 요청에 검색 조건이 있을 경우, 해당 조건을 사람인 API로 보낼 요청의 query_params로 사용
    for parameter in query_parameters:
        if parameter_injection:
            parameter_value = parameter_injection.get(parameter, "")
            
            # 수정
            if parameter == "location":
                query_params[parameter] = parameter_value
        
            # 수정
            elif parameter == "industry":
                query_params[parameter] = parameter_value
                
            else:
                query_params[parameter] = parameter_value
    
    # 검색 결과 수 10개로 지정
    query_params["count"] = 10
    
    response = requests.get(base_url, params = query_params)
    return response