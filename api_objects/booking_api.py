# api_objects/booking_api.py
import uuid
import time
import base64
import urllib.parse
from api_objects.base_api import BaseApi

class BookingApi(BaseApi):

    # --- 新增：自定义加密算法 ---
    def _encrypt_password(self, password):
        # 1. 生成一个随机的 UUID
        uid = str(uuid.uuid4())
        
        # 2. 获取当前毫秒级时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 3. 拼接字符串
        raw_str = f"{uid}{password}{timestamp}"
        
        # 4. Base64 编码
        b64_bytes = base64.b64encode(raw_str.encode("utf-8"))
        b64_str = b64_bytes.decode("utf-8")
        
        # 5. URL 编码
        final_str = urllib.parse.quote(b64_str)
        
        print(f"加密调试: 原始={password} -> 结果={final_str}")
        return final_str
    
    # 鉴权：登录方法
    def login(self, username, password):
        # 如果需要启用加密，取消下面这行的注释即可
        # password = self._encrypt_password(password)
        
        payload = {"username": username, "password": password}
        response = self.post("/auth", data=payload)
        return response

    # ➕➕➕【本次新增的核心方法】➕➕➕
    # 业务：创建预定
    def create_booking(self, data):
        # 这里的 /booking 是接口文档规定的创建路径
        return self.post("/booking", data=data)

    # 业务：修改预定
    def update_booking(self, booking_id, data, token):
        headers = {"Cookie": f"token={token}"}
        return self.put(f"/booking/{booking_id}", data=data, headers=headers)

    # 业务：查询预定
    def get_booking(self, booking_id):
        return self.get(f"/booking/{booking_id}")
    
    # 业务：删除预定
    def delete_booking(self, booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return self.delete(f"/booking/{booking_id}", headers=headers)