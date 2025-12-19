# api_objects/booking_api.py
from api_objects.base_api import BaseApi

class BookingApi(BaseApi):
    
    # 鉴权：登录方法
    def login(self, username, password):
        payload = {"username": username, "password": password}
        response = self.post("/auth", data=payload)
        return response

    # 业务：修改预定
    # 你看，这里把 url 拼接的脏活累活都干了
    def update_booking(self, booking_id, data, token):
        headers = {"Cookie": f"token={token}"}
        # 调用父类的 put
        return self.put(f"/booking/{booking_id}", data=data, headers=headers)

    # 业务：查询预定 (预留)
    def get_booking(self, booking_id):
        return self.get(f"/booking/{booking_id}")
    
    # 业务：删除预定
    def delete_booking(self, booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return self.delete(f"/booking/{booking_id}", headers=headers)