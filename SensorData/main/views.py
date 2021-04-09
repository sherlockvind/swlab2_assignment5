from django.shortcuts import render, get_object_or_404, redirect
from .sensor_data_handler import SensorDataHandler as sdh
from .forms import FileForm

def home(request):
    context = {"form": None, "data": None}
    form = None

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            data_handler = sdh(uploaded_file, time_field="Time", reading_field="Reading", sensor_field="Sensor", status_field="Status")
            on_summary = data_handler.apply(method="summarise", status="ON")
            off_summary = data_handler.apply(method="summarise", status="OFF")
            data = {"on_data": on_summary, "off_data": off_summary}

            context["form"] = form
            context["data"] = data

            return render(request, 'main/home.html', context)
    else:
        form = FileForm()

    context["form"] = form
    return render(request, "main/home.html", context)


def theft_leak(request):
    context = {"form": None, "data": None}
    form = None

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            data_handler = sdh(uploaded_file, time_field="Time", reading_field="Reading", sensor_field="Sensor", status_field="Status")
            data = data_handler.apply(method="theft_leak", status="OFF")
            
            context["form"] = form
            context["data"] = data
            return render(request, 'main/theft_leak.html', context)
    else:
        form = FileForm()

    context["form"] = form
    return render(request, "main/theft_leak.html", context)
