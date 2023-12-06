from django.shortcuts import render
from django.http import HttpResponse
from .models import ItemDetails
from .form import ItemsForm
import pandas as pd


# Create your views here.


def index(request):
    if request.method == "POST":
        form = ItemsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "index.html", {"obj": obj})
    else:
        form = ItemsForm()
    img = ItemDetails.objects.all()
    return render(request, "index.html", {"img": img, "form": form})


def alamode(request):
    return render(request, "alamode.html")


def orders(request):
    return render(request, "orders.html")


def reports(request):
    return render(request, "reports.html")


def addstock(request):
    if request.method == "POST":
        form = ItemsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "addstock.html", {"obj": obj})
    return render(request, "addstock.html")


def stockdetails(request):
    search = request.GET.get("q")
    form = ItemsForm()
    if search is not None:
        img = ItemDetails.objects.filter(ItemName__icontains=search)
    else:
        img = ItemDetails.objects.all()
    return render(request, "stockdetails.html", {"img": img, "form": form})


def dashboard(request):
    xl_months = ("November_2023", "December_2023")
    month_selection = request.POST.get("name_of_select")
    print(month_selection)
    if month_selection is not None and month_selection in xl_months:
        df = pd.read_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection))
    else:
        df = pd.read_excel(r"C:\Users\Rohit\Desktop\December_2023.xlsx")
    numOfEarrings, SellP, CostP = df['NumOfEarrings'].sum(), df['SellP'].sum(), df['CostP'].sum()
    df.loc[len(df.index)] = ["Total: ", numOfEarrings, "-", "-", "-", CostP, SellP, "-"]
    TotalEarnings, TotalExpenses = SellP - CostP, 0
    table_content = df.to_html(classes='table table-striped table-sm')
    return render(request, "dashboard.html", {"OrdersCount": df.shape[0] - 1, "TotalEarnings": TotalEarnings,
                                              "TotalExpenses": TotalExpenses, "table_content": table_content,
                                              "xl_months": xl_months})
