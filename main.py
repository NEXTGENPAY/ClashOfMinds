import os
import flet as ft
import google.generativeai as genai
import asyncio

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)

AD_URL = "https://pl28402732.effectivegatecpm.com/5074631cf56b2d724ded69adfb7d145f"

async def main(page: ft.Page):
    page.title = "Clash of Minds"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])

    messages = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    async def open_ad_later():
        await asyncio.sleep(1)
        page.launch_url(AD_URL)

    async def send_message(e):
        if not user_input.value:
            return

        page.launch_url(AD_URL)

        messages.controls.append(
            ft.Text(f"👤 أنت: {user_input.value}", weight="bold")
        )
        page.update()

        try:
            response = await asyncio.to_thread(
                chat.send_message, user_input.value
            )
            messages.controls.append(
                ft.Text(f"🤖 الذكاء: {response.text}")
            )
        except:
            messages.controls.append(
                ft.Text("⚠️ خطأ في الاتصال", color="red")
            )

        user_input.value = ""
        page.update()

    user_input = ft.TextField(
        hint_text="اكتب موضوع المناظرة...",
        expand=True,
        on_submit=send_message
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Clash of Minds"),
            bgcolor=ft.colors.BLUE_700,
            center_title=True
        ),
        messages,
        ft.Row([
            user_input,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                on_click=send_message
            )
        ])
    )

    page.run_task(open_ad_later)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
