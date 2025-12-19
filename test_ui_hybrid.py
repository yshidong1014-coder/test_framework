# test_ui_hybrid.py
import pytest
from playwright.sync_api import Page, expect
from api_objects.booking_api import BookingApi

@pytest.fixture(scope="function")
def login_page(page: Page, playwright):
    # 1. 【API 动作】利用我们封装好的 API 这一层去拿 Token
    # 注意：这里我们临时创建一个 API 上下文，只为了拿 Token
    api_request = playwright.request.new_context(base_url="https://restful-booker.herokuapp.com")
    api_service = BookingApi(api_request)
    
    # 登录拿到 token
    res = api_service.login("admin", "password123")
    token = res.json()["token"]
    
    # 2. 【核心黑魔法】把 Token 注入到浏览器 (UI) 里
    # 注意：这个网站是用 Cookie 存 Token 的，key 是 "token"
    # context.add_cookies 需要传入 domain，这里是 localhost 或者网站域名
    context = page.context
    context.add_cookies([{
        "name": "token",
        "value": token,
        "domain": "restful-booker.herokuapp.com",
        "path": "/"
    }])
    
    # 3. 返回这个已经"自带登录态"的页面
    return page
def test_admin_panel_access(login_page: Page):
    # 1. 直接访问后台管理页 (因为 Cookie 里已有 Token，理论上应该直接进)
    # 注意：这个靶场其实没有真正的后台页，我们用它的首页模拟
    login_page.goto("https://restful-booker.herokuapp.com/#/admin")

    # --- 这里开始是 Level 1 (Locator) 的练习 ---
    
    # 练习 A: 使用 get_by_role 定位 (推荐)
    # 假设页面上有一个 "Rooms" 的链接
    # 验证它是可见的
    expect(login_page.get_by_role("link", name="Rooms")).to_be_visible()

    # 练习 B: 使用 get_by_text 定位
    # 验证页面上有 "Log out" 按钮 (证明登录成功)
    expect(login_page.get_by_text("Log out")).to_be_visible()
    
    # 练习 C: 交互操作
    # 点击 Rooms
    login_page.get_by_role("link", name="Rooms").click()
    
    print("混合模式 UI 测试通过！")