# api_objects/booking_api.py
from api_objects.base_api import BaseApi

class BookingApi(BaseApi):
    # --- 新增：自定义加密算法 ---
    def _encrypt_password(self, password):
        # 1. 生成一个随机的 UUID (每次都不一样)
        uid = str(uuid.uuid4())
        
        # 2. 获取当前毫秒级时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 3. 拼接字符串: UUID + 密码 + 时间戳
        # 结果类似: "3698beb5...AutoUser_0011765792217008"
        raw_str = f"{uid}{password}{timestamp}"
        
        # 4. Base64 编码
        # 注意: base64.b64encode 接收 bytes，所以要 encode
        b64_bytes = base64.b64encode(raw_str.encode("utf-8"))
        b64_str = b64_bytes.decode("utf-8")
        
        # 5. URL 编码 (处理特殊字符，比如 = 变成 %3D)
        final_str = urllib.parse.quote(b64_str)
        
        print(f"加密调试: 原始={password} -> 结果={final_str}")
        return final_str
    
    # 鉴权：登录方法
    def login(self, username, password):
        # ⚡️ 新增：使用自定义加密算法
        # encrypted_password = self._encrypt_password(password)
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