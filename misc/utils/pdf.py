import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template


def export_pdf_from_html(request, name, html, options, data):
    html_template = get_template(html)
    rendered_html = html_template.render(data, request)
    pdf_file = pdfkit.from_string(rendered_html, False, configuration=settings.PDF_CONFIG, options=options)
    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'attachment;filename="' + name + '.pdf"'
    return http_response
