from django.shortcuts import render
from django.http import HttpResponse
from .models import ItemDetails
from .form import ItemsForm
import pandas as pd
from stock.scripts.trackparcel import getcourierdetails
from openpyxl import load_workbook


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
    items = ItemDetails.objects.filter(ItemAvailCount__gte=1)
    print(items)
    return render(request, "alamode.html", {"items": items})


def pagedetails(request, slug):
    items = ItemDetails.objects.filter(ItemSlug__iexact=slug)
    return render(request, "productdetails.html", {"items": items})


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


def write_excel(filename, sheetname, dataframe):
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        workBook = writer.book
        # try:
        #     workBook.remove(workBook[sheetname])
        # except:
        #     print("Worksheet does not exist")
        # finally:
        dataframe.to_excel(writer, sheet_name=sheetname, index=False)
        writer.save()


def dashboard(request):
    xl_months = ("November_2023", "December_2023")
    month_selection = request.POST.get("name_of_select")
    fetch_tracking = request.POST.get("fetch_tracking")
    print(fetch_tracking)

    if month_selection is None:
        month_selection = "December_2023"

    if fetch_tracking is not None:
        print("Fetching the tracking details of the orders")
        df = pd.read_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), 'Sheet1')
        df_tmp = df.loc[(df['Status'] == 'Pending')]
        print(df)
        for num in df_tmp['TrackingNumber']:
            result = getcourierdetails(num)
            print(result)
            if result == 0:
                df.loc[df.TrackingNumber == num, 'Status'] = ['Delivered']
                # df.loc[df['TrackingNumber'].isin(num), 'Status'] = ['Delivered']
                # with pd.ExcelWriter("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), engine='openpyxl') as writer:
                #     writer.book = load_workbook("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection))
                #     writer.save()
                #     df.to_excel(writer, "Sheet1", cols=['Status'])
                # df.to_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), 'Sheet1')
        write_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), 'Sheet1', df)
        print(df)
        # for row in df.loc[(df['Status'] == 'Pending')]:
        #     print(row)
        # if stat != 'Delivered':
        #    print(df['TrackingNumber'])

    df = pd.read_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), 'Sheet1')
    df_expenses = pd.read_excel("C:\\Users\\Rohit\\Desktop\\{}.xlsx".format(month_selection), 'Sheet2')

    numOfEarrings, SellP, CostP, ExpenseAmount = df['NumOfEarrings'].sum(), df['SellP'].sum(), df['CostP'].sum(), \
                                                 df_expenses['ExpenseAmount'].sum()
    df.loc[len(df.index)] = ["Total: ", numOfEarrings, "-", "-", "-", CostP, SellP, "-"]
    TotalEarnings, TotalExpenses = SellP - CostP, ExpenseAmount
    total_profit = TotalEarnings - TotalExpenses
    orders_data = df.to_html(classes='table table-striped table-hover table-bordered')
    expenses_data = df_expenses.to_html(classes='table table-striped table-sm')
    return render(request, "dashboard.html", {"OrdersCount": df.shape[0] - 1, "TotalEarnings": TotalEarnings,
                                              "TotalExpenses": TotalExpenses, "orders_data": orders_data,
                                              "expenses_data": expenses_data, "total_profit": total_profit,
                                              "month_selection": month_selection,
                                              "xl_months": xl_months})
