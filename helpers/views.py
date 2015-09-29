from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from braces.views import FormMessagesMixin
from envelope.views import ContactView


class ContactFormView(FormMessagesMixin, ContactView):
    form_valid_message = _("Thank you for your inquiry. We will try to contact you as soon as possible.")
    form_invalid_message = _("There is an error in the contact form.")

    success_url = '/'


def pdf_response(pdf, force_download=False, *args, **kwargs):
    attachment = 'attachment; ' if force_download else ''

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = attachment + 'filename="%s"' % pdf.filename()

    pdf.write_to(response)
    return response
