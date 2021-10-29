from xhtml2pdf import pisa
import jinja2
import os
from django.conf import settings
from certification_api.settings import firebase_storage


def from_html(context):

    template_path = os.path.join(settings.BASE_DIR, r'certification/templates/certification')
    output_path = os.path.join(settings.BASE_DIR, r'certification/file_buffer')
    template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    template_env = jinja2.Environment(loader=template_loader)

    certificate_template = 'certificate_template.html'
    certificate_template = template_env.get_template(certificate_template)
    output_file = os.path.join(output_path, f'{context["certificate_id"]}.pdf')

    source_html = certificate_template.render(data=context)
    certificate = open(output_file, 'wb')
    pisa.CreatePDF(src=source_html, dest=certificate)
    certificate.close()
    return f'{context["certificate_id"]}.pdf'

def from_database(file_name):
    buffer_loc = os.path.join(settings.BASE_DIR, 'certification', 'file_buffer', file_name)
    firebase_storage.child(file_name).download(buffer_loc)
    return file_name
