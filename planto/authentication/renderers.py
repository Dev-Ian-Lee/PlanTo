import json

from rest_framework.renderers import JSONRenderer

class UserJsonRenderer(JSONRenderer):
    charset = "utf-8"
    
    def render(self, data, media_type = None, renderer_context = None):
        # data 내의 token은 Byte 타입으로 존재
        token = data.get("token", None)
        
        # Byte는 직렬화(Serialize)하지 못하기 때문에 rendering 전에 decode
        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")
            
        # data를 "user"로 감싼 뒤, json 타입으로 render
        return json.dumps(
            {"user": data}
        )