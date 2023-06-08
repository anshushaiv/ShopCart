from django.shortcuts import render
from ecommerceapp.models import Contact,Product 
from django.contrib import messages
from math import ceil

# Create your views here.

def index(request):
    allProds=[]
    catProds=Product.objects.values('category','product_id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allprods':allProds}

    return render(request, "index.html",params) 


def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        description=request.POST.get("desc")
        ph_no=request.POST.get("pnnumber")
        my_query=Contact(name=name,email=email,desc=description,phonenumber=ph_no)
        my_query.save()
        messages.info(request,"We will back to you soon")
        return render(request, "contact.html")
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")