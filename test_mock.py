import pytest
from playwright.sync_api import Page, expect

def test_mock_booking_data(page: Page):
    # 1. 定义 Mock Data (保持不变)
    mock_data = {
        "firstname": "Tester",
        "lastname": "Hero",
        "totalprice": 99999,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-02-01"},
        "additionalneeds": "VIP Service"
    }

    # 2. 开启拦截 (保持不变)
    def handle_route(route):
        print(f"⚠️ 拦截到了请求: {route.request.url}")
        route.fulfill(
            status=200,
            content_type="application/json",
            json=mock_data
        )

    page.route("**/booking/1", handle_route)

    # 3. 访问空页面开启浏览器环境
    page.goto("about:blank")

    # 4. 【核心修改】让浏览器自己去 fetch！
    # page.evaluate 会在浏览器控制台里执行这段 JS 代码
    # 这样发出的请求才会被 page.route 拦截到
    data = page.evaluate("""async () => {
        const response = await fetch("https://restful-booker.herokuapp.com/booking/1");
        return response.json();
    }""")

    # 5. 验证
    print(f"实际拿到的数据: {data}")
    assert data["firstname"] == "Tester"
    assert data["totalprice"] == 99999
    print("🎉 Mock 成功！浏览器完全被我们骗了！")