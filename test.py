from jinja2 import Environment, FileSystemLoader
import os
import base64
from datetime import date, datetime
from pdfkit import PDFKit

name = "dummy123"
age = "23"
symptoms = "chestpain fever bodypain"


def image2base64():
    # changing image to base64 string
    with open('logo.jpg', 'rb') as f:
        return base64.b64encode(f.read()).decode()


def rendering_prescription(name,age,symptoms,prediction):
    print("creating cover page")
    file_loader = FileSystemLoader(searchpath="D:/Projects/Telebot/telegram")
    env = Environment(loader=file_loader)
    # variables to be passed to html file
    values = {
        'name': name,
        'img_string': image2base64(),
        'age': age,
        'symp': symptoms,
        'prediction': prediction,
        'date': date.today().strftime('%d/%m/%Y'),
        'time': datetime.now().strftime("%H:%M:%S")
    }
    # rendering into cover.html template
    cover_page = env.get_template("template.html").render(values)
    file = os.path.join("D:/Projects/Telebot/telegram/output/content.html")
    text_file = open(file, "w")
    text_file.write(cover_page)
    text_file.close()
    print('cover page created')


def html2pdf():
    today = date.today().strftime('%Y/%m/%d')
    cur_time = datetime.now().time().replace(microsecond=0)
    options = {
        # configuration options for pdf
        'page-size': 'A4',
        'margin-top': '0.35in',
        'margin-right': '0.3in',
        'margin-bottom': '0.35in',
        'margin-left': '0.3in',
        'footer-line': '',
        'footer-left': cur_time,
        'footer-font-size': '10',
        # 'header-line': '',
        # 'header-right': 'Swastha Seva',
        'header-font-size': '10',
        'header-spacing': '4',
        'footer-right': '[page] of [topage]',
        'footer-center': today,
        'footer-spacing': '2'
    }
    content = "D:/Projects/Telebot/telegram/output/content.html"
    # naming dictionary for diff input types
    # tuple to store the sequence of given files
    x = []
    x.append(content)
    x = tuple(x)
    # adding table data,cover page,toc to be converted to into pdf
    r = PDFKit(x,
               "D:/Projects/Telebot/telegram/output/prescription.pdf", options=options)
    print("creating all merged pdf")
    return r.to_pdf("D:/Projects/Telebot/telegram/output/prescription.pdf")


# rendering_prescription()
# html2pdf()
