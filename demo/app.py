import gradio as gr

from nameh_khan.page_reader.plain_text_page import PlainTextPageReader


theme = gr.themes.Ocean(
    primary_hue="teal",
    secondary_hue="violet",
    neutral_hue="gray",
    text_size="lg",
    spacing_size="lg",
    font=[gr.themes.GoogleFont('IBM Plex Sans'), 
    gr.themes.GoogleFont('ui-sans-serif'), 
    gr.themes.GoogleFont('system-ui'),
     gr.themes.GoogleFont('sans-serif')],
).set(
    body_background_fill='*code_background_fill',
    body_text_size='*input_text_size',
    background_fill_primary='*primary_50',
    prose_header_text_weight='800',
    shadow_drop='none',
    button_border_width='*panel_border_width',
    button_border_width_dark='*panel_border_width',
    button_transform_hover='scale(1.05)'
)

title = "Nameh Khan"
desc = "Turn picture into text with our image to text converter. Simply upload your photos in our OCR and extract text from image with a single click."


def function(image):
    output_path = 'text.txt'
    # page_reader = PlainTextPageReader()
    # text = page_reader.transform(image)
    text = '''20
صالحی دیدار با نماینده ولی فقیه در استان و امام جمعه کرمانشاه،
برگزاری یازده کرسی تلاوت و ویژه‌ برنامه‌هایی در بقاع متبرکه
استان با رعایت پروتکل‌های بهداشتی، برگزاری نشست تخصصی
وقف با حضور استاندار کرمانشاه، برگزاری همایش یاوران وقف به
صورت کشوری و از طریق ویدئوکنفرانس، اجرای طرح دستهای
مهربانی، اجرای طرح مهرتندرستی با حضور پزشکان و کادر درمان
در مناطق حاشیه‌نشین، برپایی ایستگاه‌های همه واقف باشیم، تجلیل
از مدافعان سلامت و غبارروبی و عطرافشانی بقاع متبرکه را از جمله
برنامه‌های تدارک دیده شده در دهه وقف در استان کرمانشاه برشمرد.
17 وقف جدید در استان کرمانشاه ثبت شده
وی در ادامه با اشاره به ضرورت برنامه‌ریزی رسانه‌ها برای نهادینه
کردن فرهنگ وقف در جامعه، گفت: در استان کرمانشاه رسانه‌ها ورود
خوبی به این حوزه داشته‌اند که امیدواریم بتواند در افزایش آگاهی‌
مردم در مورد اهمیت پرداختن به وقف اثرگذار بوده و زمینه‌ساز
افزایش تعداد موقوفات استان شود.
صالحی اشاره ای هم به ثبت 17 وقف جدید در استان کرمانشاه از ابتدای
امسال تاکنون داشت و گفت: عمده این موقوفات در حوزه های
قرآنی، کمک به نیازمندان، ایتام و ... بوده‌ است.
وی در پایان راه‌اندازی 10 نیروگاه خورشیدی در بقاع متبرکه'''

    with open(output_path, 'w') as f: 
        f.write(text)
    return text, output_path

demo = gr.Interface(
    fn=function,  
    inputs=gr.Image(type='filepath', width=800, height=600, sources=['upload']),
    outputs=[gr.Textbox(label='Text', rtl=True), gr.DownloadButton(label='Download .txt', size='sm')],
    theme=theme,
    title=title, 
    description=desc,
    flagging_mode="never",
    css="footer{display:none !important}"
)
    
demo.launch()