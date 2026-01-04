import os
import flet as ft
import google.generativeai as genai

# إعداد Gemini
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    AD_URL = "https://pl28402732.effectivegatecpm.com/5074631cf56b2d724ded69adfb7d145f"

    chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

    messages = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    def send_message(e):
        if not user_input.value:
            return

        messages.controls.append(
            ft.Text(f"👤 أنت: {user_input.value}", color="blue200", weight="bold")
        )

        try:
            response = chat.send_message(user_input.value)
            messages.controls.append(
                ft.Text(f"🤖 الذكاء: {response.text}", color="white")
            )
        except:
            messages.controls.append(
                ft.Text("⚠️ خطأ في الاتصال بالذكاء الاصطناعي", color="red")
            )

        user_input.value = ""
        page.launch_url(AD_URL)
        page.update()

    user_input = ft.TextField(
        hint_text="اكتب موضوع المناظرة...",
        expand=True,
        border_radius=15,
        on_submit=send_message
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Clash of Minds"),
            center_title=True,
            bgcolor="blue",
            leading=ft.Image(
                src="icon.png.png",
                width=30,
                height=30
            )
        ),
        messages,
        ft.Row(
            [
                user_input,
                ft.IconButton(
                    ft.Icons.SEND_ROUNDED,
                    on_click=send_message,
                    icon_color="blue400"
                )
            ]
        )
    )

ft.app(target=main)
