import pytest
from playwright.sync_api import Browser

# 这里的 browser 是 pytest-playwright 提供的全局对象
def test_login_bypass(browser: Browser):
    # 1. 【核心】创建 Context 时注入凭证
    # 就像你带着身份证去开了一个新窗口
    context = browser.new_context(storage_state="auth.json")
    
    # 2. 打开页面
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/secure")

    # 3. 验证：不需要登录，直接就在里面了！
    # 如果没注入凭证，访问这个 /secure 网址会直接跳回登录页
    import time
    time.sleep(2) # 强行暂停给你看一眼
    
    assert "secure" in page.url
    print("🎉 免登录测试通过！")
    
    context.close()