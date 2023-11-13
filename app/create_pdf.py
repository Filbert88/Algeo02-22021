from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from PIL import Image as PILImage
import orjson, os, tempfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def save_temp_image(image, suffix):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temp_image_path = tmp.name
        image.save(temp_image_path)
    return temp_image_path

class HorizontalLine(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width

    def draw(self):
        self.canv.line(0, 0, self.width, 0)

def create_report():
    with open("app/data/result.json", "rb") as f:
        result_data = orjson.loads(f.read())

    if result_data:
        total_images = len(result_data)
        pdf_filename = "PixPlore_report.pdf"
        doc = SimpleDocTemplate(os.path.join('app/static',pdf_filename), pagesize=letter, author="PixPlore.")

        pdf_content = []

        font_name = "SpaceMono-Regular"  
        font_path = "app/static/fonts/SpaceMono-Regular.ttf" 
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        font_name = "SpaceMono-Bold"
        font_path = "app/static/fonts/SpaceMono-Bold.ttf"
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.fontName = "SpaceMono-Bold"
        heading_style = ParagraphStyle(name="HeadingStyle", fontSize=14, fontName="SpaceMono-Regular",alignment=TA_CENTER)
        body_style = ParagraphStyle(name="BodyStyle", fontSize=12, fontName="SpaceMono-Regular")
        center_style = ParagraphStyle(name="CenterStyle", fontSize=12, fontName="SpaceMono-Regular", alignment=TA_CENTER)

        title = Paragraph("SIMILARITY REPORT by PixPlore.", title_style)
        pdf_content.append(title)
        pdf_content.append(Spacer(1, 5))
        s_type = result_data[0]["type"]
        search_type = Paragraph(f"SEARCH TYPE: {s_type}", heading_style)
        pdf_content.append(search_type)
        pdf_content.append(Spacer(1, 20))
        pdf_content.append(HorizontalLine(doc.width))
        pdf_content.append(Spacer(1, 20))

        input_img_name = os.listdir('app/data/img/user')[0]
        input_img_url = os.path.join('app/data/img/user', input_img_name)
        input_img = PILImage.open(input_img_url)
        input_img = input_img.resize((150, 150))
        input_suffix = os.path.splitext(input_img_url)[1].lower()
        temp_input_image_path = save_temp_image(input_img, input_suffix)


        pdf_content.append(Paragraph("INPUT IMAGE", heading_style))
        pdf_content.append(Spacer(1, 40))
        pdf_content.append(Image(temp_input_image_path, width=150, height=150))
        pdf_content.append(Spacer(1, 40))
        pdf_content.append(HorizontalLine(doc.width))
        pdf_content.append(Spacer(1, 20))

        temp_paths = []  
        pdf_content.append(Paragraph("RESULT",heading_style))
        pdf_content.append(Spacer(1, 50))

        for i, item in enumerate(result_data):
            similarity = round(float(item["similarity"]), 5)
            if similarity % 1 > 0:
                similarity = "{:.3f}%".format(similarity * 100)
            else:
                similarity = "{:.0f}%".format(similarity * 100)
            image_url = item["file_path"]

            result_img = PILImage.open(image_url)
            result_img = result_img.resize((150, 150))
            file_extension = os.path.splitext(image_url)[1].lower()
            temp_image_path = save_temp_image(result_img, file_extension)
            temp_paths.append(temp_image_path)

            pdf_content += [
                Paragraph(f"Result {i + 1}/{total_images}", body_style),
                Image(temp_image_path, width=150, height=150),
                Spacer(1, 10),
                Paragraph(f"Similarity: {similarity}", center_style),
                Spacer(1, 12),
                HorizontalLine(doc.width), 
                Spacer(1, 12),
            ]

        doc.build(pdf_content)

        os.remove(temp_input_image_path)
        for path in temp_paths:
            os.remove(path)

        print(f"PDF report '{pdf_filename}' generated successfully.")
    else:
        print("No data available in result.json.")
