import gradio as gr

from nameh_khan.page_reader.plain_text_page import PlainTextPageReader


theme = gr.themes.Ocean(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="gray",
    text_size="md",
    spacing_size="sm",
    font=[
        'san-serif',
        'Tahoma',
        gr.themes.GoogleFont('ui-sans-serif'), 
        gr.themes.GoogleFont('IBM Plex Sans'), 
        gr.themes.GoogleFont('system-ui'),
        gr.themes.GoogleFont('sans-serif')
    ],
).set(
    body_background_fill='*code_background_fill',
    body_text_size='*input_text_size',
    background_fill_primary='*primary_50',
    prose_header_text_weight='800',
    shadow_drop='none',
    button_border_width='*panel_border_width',
    button_border_width_dark='*panel_border_width',
    button_transform_hover='scale(1.05)',
    button_primary_background_fill='#007BFF',  # Set primary background color
    button_primary_text_color='white',  # Set text color for buttons
    button_primary_background_fill_hover='teal',  # Hover color
)


copy_js = """
function(text) {
    navigator.clipboard.writeText(text);
}
"""


title = "Nameh Khan"
desc_1 = "Turn picture into text with our image to text converter."
desc_2 = "Simply upload your photos in our OCR and extract text from image with a single click."
logo = """<svg width="65" height="60" viewBox="0 0 65 60" fill="none" xmlns="http://www.w3.org/2000/svg">
<path opacity="0.984" fill-rule="evenodd" clip-rule="evenodd" d="M64.2518 9.56264C64.2518 9.68764 64.2518 9.81264 64.2518 9.93764C60.8312 21.3655 56.9771 32.6572 52.6893 43.8126C51.3651 47.1295 49.6567 50.2129 47.5643 53.0627C42.9778 58.522 37.2069 60.4595 30.2518 58.8752C21.9384 55.26 13.6884 51.51 5.5018 47.6251C1.57804 44.5678 -0.0261354 40.547 0.6893 35.5626C0.774855 34.6961 0.962355 33.8628 1.2518 33.0626C10.5435 36.8335 19.8352 40.6043 29.1268 44.3751C29.1399 46.2501 29.3691 48.1043 29.8143 49.9377C31.5218 54.1613 34.5011 55.3904 38.7518 53.6252C41.3542 52.4597 43.3751 50.6472 44.8143 48.1877C46.3802 45.5139 47.7136 42.7223 48.8143 39.8126C52.2887 30.5353 55.4762 21.1603 58.3768 11.6876C47.9173 9.64155 37.4589 7.62071 27.0018 5.62514C23.7978 14.4451 20.5687 23.2576 17.3143 32.0626C16.3187 33.2769 15.1312 33.506 13.7518 32.7501C12.812 31.9645 12.4995 30.9854 12.8143 29.8126C16.2651 20.2101 19.7651 10.6268 23.3143 1.06264C24.2007 0.128719 25.2632 -0.142114 26.5018 0.250144C38.4216 2.60909 50.3382 4.98409 62.2518 7.37514C63.3426 7.73591 64.0092 8.46507 64.2518 9.56264Z" fill="white"/>
</svg>"""

download_icon = """<svg width="25" height="24" viewBox="0 0 25 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M6.086 6.414L8.914 3.586C9.289 3.211 9.798 3 10.328 3H17.5C18.605 3 19.5 3.895 19.5 5V19C19.5 20.105 18.605 21 17.5 21H7.5C6.395 21 5.5 20.105 5.5 19V7.828C5.5 7.298 5.711 6.789 6.086 6.414Z" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M5.5 8H9.5C10.052 8 10.5 7.552 10.5 7V3" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M16.5 11H8.5" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M16.5 14H8.5" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M16.5 17H12.17" stroke="white" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def function(image):
    output_path = 'text.txt'
    # page_reader = PlainTextPageReader()
    # text = page_reader.transform(image)
    text = 'hi'
    with open(output_path, 'w') as f: 
        f.write(text)
    return text, output_path

with gr.Blocks(theme=theme, css="footer { display: none !important; }") as demo:
    gr.Markdown(f"""
    <div style='text-align: center; font-size: 18px;'>
    <div style='display: flex; align-items: center; gap: 10px; justify-content: center'>{logo}
    <h1 style='font-size: 43px'>{title}</h1>
    </div><p style='margin-bottom: 0'>{desc_1}</p>
    <p style='margin-top: 0'>{desc_2}</p></div>"""
    )

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type='filepath', width=700, height=600, sources=['upload'])
            with gr.Row():
                submit_button = gr.Button("Submit", variant='primary')
                clear_button = gr.Button("Clear", variant='huggingface')

        with gr.Column(scale=0, min_width=100):
            pass

        with gr.Column():
            output_text = gr.Textbox(label='Text', rtl=True, lines=27, max_lines=30)
            with gr.Row():
                copy_button = gr.DownloadButton(label='Copy to Clipboard', size='lg', visible=False, icon='interface-essential.svg')
                download_button = gr.DownloadButton(label='Download .txt', size='lg', visible=False, icon='files-17.svg')
    
    submit_button.click(fn=function, inputs=image_input, outputs=[output_text, download_button])
    submit_button.click(
        fn=lambda text: [gr.update(visible=True), gr.update(visible=True)],  
        inputs=output_text,
        outputs=[copy_button, download_button]
    )
    clear_button.click(lambda: (None, ""), inputs=None, outputs=[image_input, output_text])
    clear_button.click(
        fn=lambda text: [gr.update(visible=False), gr.update(visible=False)],  
        inputs=output_text,
        outputs=[copy_button, download_button]
    )
    copy_button.click(fn=None, inputs=output_text, outputs=None, js=copy_js)

demo.launch()
