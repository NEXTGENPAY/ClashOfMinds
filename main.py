import flet as ft
import google.generativeai as genai
import os
import time

# --- إعداد الذكاء الاصطناعي ---
GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# --- رابط الإعلان ---
AD_URL = "https://pl28402732.effectivegatecpm.com/5074631cf56b2d724ded69adfb7d145f"

def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    # --- الإعلان الأول عند فتح التطبيق ---
    def launch_initial_ad():
        time.sleep(1.5)
        page.launch_url(AD_URL)

    # --- وظيفة إرسال الرسائل ---
    def send_message(e):
        if not user_input.value:
            return
        page.launch_url(AD_URL)  # إعلان عند كل رسالة
        try:
            r = chat.send_message(user_input.value)
            messages.controls.append(ft.Text(f"👤 أنت: {user_input.value}", color="cyan"))
            messages.controls.append(ft.Text(f"🤖 الذكاء: {r.text}", color="white"))
        except:
            messages.controls.append(ft.Text("⚠️ خطأ في الاتصال", color="red"))
        user_input.value = ""
        page.update()

    # --- الواجهة ---
    messages = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    user_input = ft.TextField(
        hint_text="اكتب موضوع الصدام...",
        on_submit=send_message,
        expand=True
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Clash of Minds"),
            leading=ft.Image(src="icon.png.png", width=30, height=30),
            actions=[ft.IconButton(ft.icons.MONETIZATION_ON, on_click=lambda e: page.launch_url(AD_URL))]
        ),
        messages,
        ft.Row([user_input, ft.IconButton(ft.icons.SEND, on_click=send_message)])
    )

    # تشغيل الإعلان الأول
    page.run_task(launch_initial_ad)

# --- تشغيل التطبيق على المتصفح ---
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
