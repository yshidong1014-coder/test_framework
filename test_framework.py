# test_framework.py
import allure
import pytest
from playwright.sync_api import Playwright
from api_objects.booking_api import BookingApi  # 引入我们封装好的类

# --- Fixture 升级：返回业务对象 ---
@pytest.fixture(scope="session")
def booking_service(playwright: Playwright):
    # 1. 创建上下文
    context = playwright.request.new_context(base_url="https://restful-booker.herokuapp.com")
    
    # 2. 实例化业务对象
    service = BookingApi(context)
    
    # 3. 在 fixture 里完成登录，拿到 token
    # (为了演示方便，我把 token 存作 service 的一个属性，或者你也可以单独传)
    res = service.login("admin", "password123")
    service.token = res.json()["token"]
    print(f"Token已就绪: {service.token}")
    
    yield service
    context.dispose()

# --- 测试用例 ---
@allure.feature("架构模式更改测试")
@allure.title("测试用例: 名字={firstname}, 价格={totalprice}")
def test_update_booking_framework(booking_service):
    # 准备数据
    data = {
        "firstname": "Framework",
        "lastname": "Master",
        "totalprice": 999,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
        "additionalneeds": "Dinner"
    }

    # ⚡️ 核心变化在这里！⚡️
    # 以前：api.put("/booking/1", headers=..., data=...)
    # 现在：像调用普通函数一样，完全看不到 HTTP 细节
    res = booking_service.update_booking(booking_id=1, data=data, token=booking_service.token)

    # 验证
    assert res.ok
    assert res.json()["firstname"] == "Framework"


@allure.feature("架构模式获取测试")
def test_get_booking_framework(booking_service):
    res = booking_service.get_booking(booking_id=1)
    assert res.ok


@allure.feature("架构模式删除测试")
def test_delete_booking_framework(booking_service):
    res = booking_service.delete_booking(booking_id=1, token=booking_service.token)
    assert res.ok
