from playwright.sync_api import sync_playwright

def generate_auth_via_browser():
    print("🚀 [浏览器模式] 开始生成最稳的凭证...")
    
    with sync_playwright() as p:
        # 1. 启动浏览器 (headless=True 代表不显示界面，在后台跑，速度也很快)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 2. 像用户一样去登录
        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button[type='submit']")

        # 3. 确保真的进去了 (这一步很关键，等 Cookie 完全写入)
        # 等待页面出现 "logout" 按钮，或者 URL 变成 secure
        page.wait_for_selector("a[href='/logout']")
        
        # 4. 保存状态
        # 这时候保存下来的，是经过浏览器验证的、绝对合法的 Cookie
        context.storage_state(path="auth.json")
        print("💾 浏览器版 auth.json 已保存！(这个肯定能用)")

        browser.close()

if __name__ == "__main__":
    generate_auth_via_browser()