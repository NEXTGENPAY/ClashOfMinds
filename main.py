import flet as ft
import google.generativeai as genai
import asyncio

# --- 1. إعدادات API (ضع مفتاحك هنا) ---
# احصل على مفتاحك من Google AI Studio: https://aistudio.google.com/
# تأكد من استبدال 'YOUR_GEMINI_API_KEY' بمفتاحك الحقيقي
GEMINI_API_KEY = "AIzaSyDst-UxzgT5jifMwSIkX-b85x256HRhddc"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. وظيفة الذكاء الاصطناعي (قلب التطبيق) ---
async def get_clash_response(char1, char2, topic):
    prompt = f"""
    أنت محاور بارع ومخرج لبرنامج "صدام الأفكار" العالمي.
    صمم مناظرة فكرية قوية، حادة، وساخرة بين:
    الشخصية 1: {char1}
    الشخصية 2: {char2}
    حول الموضوع: {topic}
    
    القواعد الصارمة:
    1. اجعل كل شخصية تستخدم منطقها الخاص، خلفيتها التاريخية/المعرفية، وأسلوبها المميز في الحوار والسخرية من الآخر.
    2. استخدم لغة عربية فصحى قوية وواضحة (أو لهجة تتناسب مع الشخصية تماماً إن لزم الأمر).
    3. قسم المناظرة إلى 3 جولات فقط (الجولة الأولى، الجولة الثانية، الجولة الثالثة).
    4. ابدأ فوراً بالحوار بدون مقدمات مملة.
    5. اجعل الحوار متوازناً وقوياً من الطرفين.
    """
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ: {e}\nالرجاء التأكد من مفتاح الـ API والاتصال بالإنترنت."

# --- 3. تصميم الواجهة الاحترافية (Flet UI) ---
def main(page: ft.Page):
    page.title = "صدام الأفكار - Clash of Minds"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = ft.colors.BLUE_GREY_900 # خلفية داكنة وجذابة
    page.window_width = 400 # عرض مناسب للموبايل
    page.window_height = 800 # طول مناسب للموبايل

    # --- الخطوط (لتحسين شكل النصوص العربية والإنجليزية) ---
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf",
        "Cairo": "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bwght%5D.ttf"
    }

    # --- عناصر الواجهة ---
    
    # 1. شاشة الدخول الفخمة (Splach Screen)
    app_title_ar = ft.Text(
        "صدام الأفكار",
        size=48,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.CYAN_A400,
        font_family="Cairo"
    )
    app_title_en = ft.Text(
        "Clash of Minds",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE70,
        font_family="RobotoSlab"
    )
    
    intro_text = ft.Text(
        "حيث تتصادم العقول وتشتعل المناظرات!",
        size=18,
        color=ft.colors.WHITE54,
        text_align=ft.TextAlign.CENTER,
        font_family="Cairo"
    )
    
    start_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.ARROW_FORWARD, color=ft.colors.BLACK),
                ft.Text("ابدأ الصدام", color=ft.colors.BLACK, size=18, font_family="Cairo"),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_click=lambda e: view_manager.go_to_main_screen(),
        bgcolor=ft.colors.CYAN_A400,
        color=ft.colors.BLACK,
        height=50,
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    splash_screen = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Brain-clipart-transparent-background-5.png", width=150, height=150), # أيقونة جذابة
                app_title_ar,
                app_title_en,
                ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                intro_text,
                ft.Divider(height=50, color=ft.colors.TRANSPARENT),
                start_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    # 2. الشاشة الرئيسية (Main Screen)
    char1_input = ft.TextField(
        label="الشخصية الأولى (مثل: المتنبي)",
        hint_text="Enter First Character",
        border_radius=10,
        filled=True,
        bgcolor=ft.colors.BLUE_GREY_800,
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE70, font_family="Cairo"),
        text_style=ft.TextStyle(font_family="Cairo")
    )
    char2_input = ft.TextField(
        label="الشخصية الثانية (مثل: إيلون ماسك)",
        hint_text="Enter Second Character",
        border_radius=10,
        filled=True,
        bgcolor=ft.colors.BLUE_GREY_800,
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE70, font_family="Cairo"),
        text_style=ft.TextStyle(font_family="Cairo")
    )
    topic_input = ft.TextField(
        label="موضوع الصدام (مثلاً: مستقبل البشرية في الفضاء)",
        hint_text="Enter Debate Topic",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border_radius=10,
        filled=True,
        bgcolor=ft.colors.BLUE_GREY_800,
        color=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.WHITE70, font_family="Cairo"),
        text_style=ft.TextStyle(font_family="Cairo")
    )

    clash_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.FLAME_KITCHEN, color=ft.colors.BLACK),
                ft.Text("اشعل الصدام!", color=ft.colors.BLACK, size=18, font_family="Cairo")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.colors.ORANGE_A700,
        color=ft.colors.BLACK,
        height=50,
        width=250,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    
    clash_result_container = ft.Container(
        content=ft.Column([], scroll=ft.ScrollMode.ADAPTIVE),
        expand=True,
        padding=ft.padding.all(10),
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=10,
        alignment=ft.alignment.top_left
    )
    
    progress_ring = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)

    async def on_clash_click(e):
        char1 = char1_input.value
        char2 = char2_input.value
        topic = topic_input.value

        if not char1 or not char2 or not topic:
            page.snack_bar = ft.SnackBar(
                ft.Text("الرجاء إدخال جميع المعلومات لإطلاق الصدام!", font_family="Cairo"),
                bgcolor=ft.colors.RED_700
            )
            page.snack_bar.open = True
            page.update()
            return
        
        clash_result_container.content.controls.clear()
        clash_result_container.content.controls.append(ft.Row([ft.Text("جاري توليد المناظرة...", font_family="Cairo", color=ft.colors.WHITE54), progress_ring], alignment=ft.MainAxisAlignment.CENTER))
        progress_ring.visible = True
        page.update()

        result_text = await get_clash_response(char1, char2, topic)
        
        progress_ring.visible = False
        clash_result_container.content.controls.clear()
        clash_result_container.content.controls.append(
            ft.Text(
                result_text,
                selectable=True,
                color=ft.colors.WHITE,
                font_family="Cairo",
                size=16
            )
        )
        page.update()
        
    clash_button.on_click = on_clash_click
    
    main_screen_layout = ft.Column(
        [
            ft.Text("أدخل تفاصيل الصدام:", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family="Cairo"),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            char1_input,
            char2_input,
            topic_input,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            clash_button,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.Text("نتائج الصدام:", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family="Cairo"),
            clash_result_container,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    
    # --- 4. مدير عرض الصفحات (للانتقال بين شاشة الدخول والشاشة الرئيسية) ---
    class ViewManager:
        def __init__(self, page: ft.Page):
            self.page = page
            self.page.views.clear()
            self.page.add(splash_screen) # نبدأ بشاشة الدخول

        def go_to_main_screen(self):
            self.page.views.append(
                ft.View(
                    "/main",
                    [
                        main_screen_layout
                    ],
                    bgcolor=self.page.bgcolor,
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    padding=20
                )
            )
            self.page.go("/main") # الانتقال إلى المسار الرئيسي

    view_manager = ViewManager(page)
    page.update()

# --- 5. تشغيل التطبيق ---
if __name__ == "__main__":
    ft.app(target=main) # هنا يمكنك تحديد assets_dir="assets" لو لديك صور محلية
