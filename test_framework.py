import allure
import pytest
from playwright.sync_api import Playwright
from api_objects.booking_api import BookingApi

# --- Fixture 1: 基础服务 (Session级) ---
@pytest.fixture(scope="session")
def booking_service(playwright: Playwright):
    context = playwright.request.new_context(base_url="https://restful-booker.herokuapp.com")
    service = BookingApi(context)
    
    # 登录并保存 Token (建议直接更新到 headers，这样后续调用都不用传 token 了)
    res = service.login("admin", "password123")
    token = res.json()["token"]
    
    # 【优化】直接将 token 注入到 context 的默认请求头中
    # 这样后续所有请求都会自动带上 Cookie: token=...
    # 注意：restful-booker 需要 Cookie: token=xxx 或 Authorization: Basic ...
    # 这里假设你的 ApiObject 封装里没有处理 headers，我们在这一层处理
    new_headers = {"Cookie": f"token={token}"}
    service.context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com",
        extra_http_headers=new_headers
    )
    # 重新实例化以便使用带 header 的 context
    final_service = BookingApi(service.context)
    
    yield final_service
    service.context.dispose()

# --- Fixture 2: 准备独立测试数据 (Function级) ---
# 每次执行测试前，先创建一个新的订单，测试后自动清除
@pytest.fixture(scope="function")
def active_booking_id(booking_service):
    # 1. 创建数据
    data = {
        "firstname": "Test", "lastname": "User", "totalprice": 100,
        "depositpaid": True, "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
        "additionalneeds": "Breakfast"
    }
    # 假设你的 API 对象有 create_booking 方法
    # 如果没有，用 playwright 原生发一个请求也可以
    res = booking_service.create_booking(data) 
    booking_id = res.json()["bookingid"]
    print(f"创建临时测试数据 ID: {booking_id}")
    
    yield booking_id
    
    # 2. 清理数据 (Teardown)
    print(f"清理测试数据 ID: {booking_id}")
    booking_service.delete_booking(booking_id)


# --- 测试用例 ---

# 修复 Allure 标题：去掉无法识别的变量，或者写死
@allure.feature("架构模式更改测试")
@allure.title("测试修改订单功能") 
def test_update_booking_framework(booking_service, active_booking_id):
    # 准备数据
    data = {
        "firstname": "Framework",
        "lastname": "Master",
        "totalprice": 999,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
        "additionalneeds": "Dinner"
    }

    # 使用 Fixture 提供的动态 ID，不再硬编码 1
    # 也不再手动传 token，因为我们在 fixture 里配置好 header 了 (视你的封装而定)
    res = booking_service.update_booking(booking_id=active_booking_id, data=data)

    assert res.ok
    assert res.json()["firstname"] == "Framework"


@allure.feature("架构模式获取测试")
def test_get_booking_framework(booking_service, active_booking_id):
    res = booking_service.get_booking(booking_id=active_booking_id)
    assert res.ok
    # 最好断言一下 ID 或内容是否匹配
    assert res.json()["firstname"] == "Test" # 对应 active_booking_id 创建时的初始数据


@allure.feature("架构模式删除测试")
def test_delete_booking_framework(booking_service, active_booking_id):
    # 这里我们手动删除，验证删除功能
    res = booking_service.delete_booking(booking_id=active_booking_id)
    assert res.status == 201
    
    # 验证确实删除了
    get_res = booking_service.get_booking(booking_id=active_booking_id)
    assert get_res.status == 404