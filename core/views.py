from django.shortcuts import render

# Create your views here.
def debug_404(request):
    return render(request, "404.html", status=404)

def debug_500(request):
    return render(request, "500.html", status=500)