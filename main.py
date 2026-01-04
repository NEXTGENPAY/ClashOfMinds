import os
import flet as ft
import google.generativeai as genai

# إعداد الذكاء الاصطناعي من السكريت
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # رابط الأرباح الخاص بك الذي استخرجته من كودك
    AD_URL = "https://pl28402732.effectivegatecpm.com/5074631cf56b2d724ded69adfb7d145f"
    
    def open_ad(e=None):
        page.launch_url(AD_URL)

    # يفتح الإعلان فور دخول المستخدم للموقع
    page.on_connect = open_ad

    chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])
    
    def send_message(e):
        if user_input.value:
            # يفتح إعلان جديد في صفحة مستقلة عند كل إرسال لزيادة ربحك
            page.launch_url(AD_URL)
            try:
                response = chat.send_message(user_input.value)
                messages.controls.append(ft.Text(f"👤 أنت: {user_input.value}", color="blue200", weight="bold"))
                messages.controls.append(ft.Text(f"🤖 الذكاء: {response.text}", color="white"))
            except Exception as ex:
                messages.controls.append(ft.Text(f"⚠️ خطأ في الاتصال", color="red"))
            
            user_input.value = ""
            page.update()

    messages = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    user_input = ft.TextField(
        hint_text="اكتب موضوع المناظرة...",
        expand=True,
        border_radius=15,
        on_submit=send_message
    )
    
    page.add(
        ft.AppBar(
            title=ft.Text("Clash of Minds"),
            bgcolor="blue",
            center_title=True,
            leading=ft.Image(src="icon.png", width=30, height=30)
        ),
        messages,
        ft.Row([user_input, ft.IconButton(ft.Icons.SEND_ROUNDED, on_click=send_message, icon_color="blue400")])
    )

# التشغيل كنسخة ويب عالمية
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
                
