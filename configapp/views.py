from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BrandForm, CarForm, SearchForm, LoginForm
from .models import Brand,Car
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
import qrcode

def index(request):
    brand = Brand.objects.all()
    car = Car.objects.all()
    context = {
        "brand":brand,
        'car':car
    }
    return render(request,'index.html',context=context)

def info(request):
    brand = Brand.objects.all()
    car = Car.objects.all()
    form = SearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('name')
        if query:
            car = car.filter(name__icontains=query)
    context = { 'car': car, 'form': form, 'brand': brand, }
    return render(request, 'index.html', context)

def add_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BrandForm()
    return render(request,'add_brand.html',{'form':form})
def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm()
    return render(request,'add_car.html',{'form':form})

def brand_detail(request, pk):
    brand_obj = get_object_or_404(Brand, id=pk)       # tanlangan brand
    cars = Car.objects.filter(brand=brand_obj)        # shu brand mashinalari
    brand = Brand.objects.all()                  # sidebar uchun barcha brandlar

    # Search form
    form = SearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('name')        # form field nomi
        if query:
            cars = cars.filter(name__icontains=query)  # shu brand ichida qidiruv

    context = {
        "car": cars,
        "brand": brand,
        "form": form
    }
    return render(request,'brand.html', context)

def detail_car(request,pk):
    car = get_object_or_404(Car,id = pk)
    site_url = f"http://{request.get_host()}/"
    context = {
        'car':car,
        'site_url':site_url
    }
    return render(request,'detail_car.html',context=context)

def download_car_pdf(request, pk):
    car = Car.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{car.name}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4

    # 🔹 Mashina nomi
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, page_height - 50, car.name)

    # 🔹 Year, Price, Create Date
    c.setFont("Helvetica", 14)
    c.drawString(50, page_height - 100, f"Year: {car.year}")
    c.drawString(50, page_height - 130, f"Price: {car.price}")
    c.drawString(50, page_height - 160, f"Create Date: {car.create_date}")

    # 🔹 Mashina rasmi
    if car.photo:
        image_path = os.path.join(settings.MEDIA_ROOT, car.photo.name)
        max_width = page_width - 100
        max_height = page_height - 300
        c.drawImage(image_path, 50, 200, width=max_width, height=max_height, preserveAspectRatio=True, mask='auto')

    # 🔹 Web sayt manziliga QR kod
    site_url = f"http://{request.get_host()}/"
    qr_img = qrcode.make(site_url)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    qr_reader = ImageReader(buffer)
    c.drawImage(qr_reader, page_width - 200, 50, width=120, height=120)  # o‘ng pastda joylashadi

    c.showPage()
    c.save()
    return response




@login_required(login_url='login')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # session ochiladi
                return redirect("home")   # login bo‘lgandan keyin home page
            else:
                form.add_error(None, "Username yoki parol xato!")

    return render(request, "login.html", {"form": form})


