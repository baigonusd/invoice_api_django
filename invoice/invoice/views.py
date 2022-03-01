from django.shortcuts import redirect


def redirect_invoice(request):
    return redirect('main_page_url', permanent=True)
