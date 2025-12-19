import uuid
import time
import base64
import urllib.parse
from api_objects.base_api import BaseApi

class BookingApi(BaseApi):

    # ... (前面的 _encrypt_password 和 login 方法保持不变) ...
    def _encrypt_password(self, password):
        uid = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))
        raw_str = f"{uid}{password}{timestamp}"
        b64_bytes = base64.b64encode(raw_str.encode("utf-8"))
        b64_str = b64_bytes.decode("utf-8")
        final_str = urllib.parse.quote(b64_str)
        return final_str
    
    def login(self, username, password):
        payload = {"username": username, "password": password}
        return self.post("/auth", data=payload)

    def create_booking(self, data):
        return self.post("/booking", data=data)

    # ⚡️ 修改点 1：token 改为默认 None
    def update_booking(self, booking_id, data, token=None):
        headers = None
        # 只有当显式传入 token 时，才去覆盖 header
        if token:
            headers = {"Cookie": f"token={token}"}
        return self.put(f"/booking/{booking_id}", data=data, headers=headers)

    def get_booking(self, booking_id):
        return self.get(f"/booking/{booking_id}")
    
    # ⚡️ 修改点 2：token 改为默认 None
    def delete_booking(self, booking_id, token=None):
        headers = None
        if token:
            headers = {"Cookie": f"token={token}"}
        return self.delete(f"/booking/{booking_id}", headers=headers)