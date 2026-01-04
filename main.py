import os
import flet as ft
import google.generativeai as genai

# AI
genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

AD_URL = "https://pl28402732.effectivegatecpm.com/5074631cf56b2d724ded69adfb7d145f"

def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    def show_ad(e=None):
        page.launch_url(AD_URL)

    def send_msg(e):
        if not input_box.value:
            return
        page.launch_url(AD_URL)
        try:
            r = chat.send_message(input_box.value)
            chat_view.controls.append(ft.Text(f"أنت: {input_box.value}", color="cyan"))
            chat_view.controls.append(ft.Text(f"الذكاء: {r.text}", color="white"))
        except:
            chat_view.controls.append(ft.Text("خطأ اتصال", color="red"))
        input_box.value = ""
        page.update()

    chat_view = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    input_box = ft.TextField(
        hint_text="اكتب موضوع الصدام",
        on_submit=send_msg,
        expand=True
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Clash of Minds"),
            leading=ft.Image(src="icon.png.png", width=30, height=30),
            actions=[ft.IconButton(ft.icons.MONETIZATION_ON, on_click=show_ad)]
        ),
        chat_view,
        ft.Row([input_box, ft.IconButton(ft.icons.SEND, on_click=send_msg)])
    )

ft.app(target=main)
