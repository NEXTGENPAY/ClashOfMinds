import flet as ft
import google.generativeai as genai
import asyncio
import os

# --- 1. إعدادات الأمان والذكاء الاصطناعي ---
# يجلب المفتاح من Secrets باسم GEMINI_KEY
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_clash_response(char1, char2, topic):
    prompt = f"""
    أنت مخرج برنامج "صدام الأفكار". صمم مناظرة حادة وساخرة بين:
    الشخصية 1: {char1} والشخصية 2: {char2} حول الموضوع: {topic}
    القواعد: 3 جولات، لغة قوية، أسلوب مميز لكل شخصية.
    """
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        return "⚠️ فشل في الاتصال بالذكاء الاصطناعي. تأكد من إعدادات المفتاح والإنترنت."

def main(page: ft.Page):
    # إعدادات الصفحة الاحترافية
    page.title = "Clash of Minds - صدام الأفكار"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    
    # تحميل الخطوط
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf",
        "Cairo": "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bwght%5D.ttf"
    }

    # --- عناصر واجهة الدخول (Splash Screen) ---
    splash_content = ft.Column(
        [
            ft.Icon(ft.icons.PSYCHOLOGY, size=100, color=ft.colors.CYAN_A400),
            ft.Text("صدام الأفكار", size=48, weight="bold", color=ft.colors.CYAN_A400, font_family="Cairo"),
            ft.Text("Clash of Minds", size=30, weight="bold", color=ft.colors.WHITE70, font_family="RobotoSlab"),
            ft.Text("حيث تتصادم العقول وتشتعل المناظرات!", size=16, color=ft.colors.WHITE54, font_family="Cairo", text_align="center"),
            ft.Divider(height=40, color=ft.colors.TRANSPARENT),
            ft.ElevatedButton(
                content=ft.Text("ابدأ الصدام الآن", size=20, font_family="Cairo"),
                on_click=lambda _: view_manager.go_to_main_screen(),
                bgcolor=ft.colors.CYAN_A400,
                color=ft.colors.BLACK,
                height=60,
                width=250,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    splash_screen = ft.Container(content=splash_content, expand=True, alignment=ft.alignment.center)

    # --- عناصر الشاشة الرئيسية (Main Screen) ---
    char1_input = ft.TextField(label="الشخصية الأولى / First Character", border_radius=12, filled=True, font_family="Cairo")
    char2_input = ft.TextField(label="الشخصية الثانية / Second Character", border_radius=12, filled=True, font_family="Cairo")
    topic_input = ft.TextField(label="الموضوع / Topic", multiline=True, min_lines=2, border_radius=12, filled=True, font_family="Cairo")
    
    result_display = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
    progress_bar = ft.ProgressBar(visible=False, color="cyan")

    async def run_clash(e):
        if not char1_input.value or not char2_input.value or not topic_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("أدخل البيانات كاملة!", font_family="Cairo"))
            page.snack_bar.open = True
            page.update()
            return

        # 1. الربح الإجباري: فتح رابط الإعلان
        page.launch_url("https://www.google.com") # سنغير هذا برابط إعلانك لاحقاً
        
        # 2. بدء التحميل
        progress_bar.visible = True
        result_display.controls.clear()
        result_display.controls.append(ft.Text("جاري استدعاء العقول... يرجى الانتظار", font_family="Cairo", italic=True))
        page.update()

        # 3. جلب النتيجة
        response = await get_clash_response(char1_input.value, char2_input.value, topic_input.value)
        
        progress_bar.visible = False
        result_display.controls.clear()
        result_display.controls.append(
            ft.Container(
                content=ft.Text(response, size=16, font_family="Cairo", color=ft.colors.WHITE),
                padding=20,
                bgcolor=ft.colors.BLUE_GREY_800,
                border_radius=15
            )
        )
        page.update()

    clash_btn = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.icons.FLAME), ft.Text("أشعل الصدام!", size=18, font_family="Cairo")], alignment="center"),
        on_click=run_clash,
        bgcolor=ft.colors.ORANGE_700,
        color=ft.colors.WHITE,
        height=55,
        width=float("inf")
    )

    main_layout = ft.Column(
        [
            ft.Text("تجهيز حلبة الصدام", size=24, weight="bold", font_family="Cairo"),
            char1_input,
            char2_input,
            topic_input,
            clash_btn,
            progress_bar,
            ft.Divider(height=20),
            ft.Text("مجريات الصدام:", size=20, weight="bold", font_family="Cairo"),
            result_display
        ],
        expand=True,
        spacing=15
    )

    # --- مدير العرض (View Manager) ---
    class ViewManager:
        def __init__(self, page):
            self.page = page
            self.page.views.clear()
            self.page.add(splash_screen)

        def go_to_main_screen(self):
            self.page.views.append(
                ft.View(
                    "/main",
                    [main_layout],
                    bgcolor=ft.colors.BLUE_GREY_900,
                    padding=25
                )
            )
            self.page.go("/main")

    view_manager = ViewManager(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
