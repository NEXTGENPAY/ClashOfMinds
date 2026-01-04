import os
import flet as ft
import google.generativeai as genai

# جلب المفتاح السري من إعدادات GitHub التي جهزتها
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK  # وضع ليلي فخم
    page.padding = 20
    
    # --- مكان رابط الإعلانات (جاهز للتغيير لاحقاً) ---
    AD_URL = "https://www.google.com" 
    
    def open_ad(e=None):
        page.launch_url(AD_URL)

    # تشغيل الإعلان عند فتح التطبيق
    page.on_connect = open_ad
    # ----------------------------------------------

    chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])
    
    def send_message(e):
        if user_input.value:
            # فتح إعلان عند كل إرسال لزيادة الربح
            page.launch_url(AD_URL)
            
            try:
                response = chat.send_message(user_input.value)
                messages.controls.append(ft.Text(f"👤 أنت: {user_input.value}", color="blue200", weight="bold"))
                messages.controls.append(ft.Text(f"🤖 الذكاء: {response.text}", color="white"))
            except Exception as ex:
                messages.controls.append(ft.Text(f"⚠️ خطأ: {str(ex)}", color="red"))
            
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
            title=ft.Text("Clash of Minds", color="white"),
            bgcolor="blue",
            center_title=True,
            leading=ft.Image(src="icon.png", width=30, height=30) # أيقونتك التي رفعتها
        ),
        messages,
        ft.Row([user_input, ft.IconButton(ft.Icons.SEND_ROUNDED, on_click=send_message, icon_color="blue400")], alignment="center")
    )

# تشغيل كمتصفح ويب (أهم سطر للربح)
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
                
