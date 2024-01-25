from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import ItemDetails
from .form import ItemsForm
from stock.scripts.trackparcel import getcourierdetails
from .utils import cookieCart
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
    # FIXME: improve this block of code to show the cart items value in better approach
    data = cookieCart(request)
    order = data['order']


    items = ItemDetails.objects.all()
    paginator = Paginator(items, 6)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(items)
    # {"items": items, "order": order, "cartItems": cartItems, "cart": cart}
    if items:
        return render(request, "alamode.html", {"items": page_obj, "order": order})
    else:
        return render(request, "alamode.html")


def pagedetails(request, slug):
    # FIXME: improve this block of code to show the cart items value in better approach
    data = cookieCart(request)
    order = data['order']

    # INFO: Product.objects.get(slug=slug)
    # we are using slug feature of django which uniquely identify the item.
    # {%url 'pagedetails' item.ItemSlug %} this call is invoked from the alamode.html on click on quick view
    items = ItemDetails.objects.get(ItemSlug=slug)
    return render(request, "productdetails.html", {"items": items, "order": order})


def cartdetails(request):
    #slug = 'kalash-earrings'
    #items = ItemDetails.objects.get(ItemName__icontains='jumkas')
    data = cookieCart(request)
    print(data)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    cart = data['cart']
    #request.set_cookie(cart, value=cart)
    print(type(cart))
    request.COOKIES['cart'] = cart
    print("######")
    print(type(request.COOKIES['cart']))
    print(request.COOKIES['cart'])
    #r2 = requests.post('http://www.yourapp.com/somepage', cookies=r1.cookies)

    response = render(request, "cartdetails.html", {"items": items, "order": order, "cartItems": cartItems, "cart": cart})
    print(response)
    #response.set_cookie('cart', cart)
    return response


def checkout(request):
    data = cookieCart(request)
    print(data)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    return render(request, "checkout.html", {"items": items, "order": order, "cartItems": cartItems})


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
    xl_months = ("November_2023", "December_2023", "January_2024")
    month_selection = request.POST.get("name_of_select")
    fetch_tracking = request.POST.get("fetch_tracking")
    #print(fetch_tracking)
    #print(month_selection)

    if month_selection is None:
        month_selection = "January_2024"

    if fetch_tracking is not None:
        df = pd.read_excel("C:\\Users\\Rohit\\Desktop\\AlaMode\\{}.xlsx".format(month_selection), sheet_name=None)
        df_tmp = df['Sheet1'].loc[(df['Sheet1']['Status'] != 'Delivered')]
        for num in df_tmp['TrackingNumber']:
            print("#######")
            print(type(num))
            if num == 'ReadyToDispatch':
                print("ISNAN")
                df['Sheet1'].loc[df['Sheet1'].TrackingNumber == num, 'Status'] = "ReadyToDispatch"
            else:
                result = getcourierdetails(num)
                # print(result)
                df['Sheet1'].loc[df['Sheet1'].TrackingNumber == num, 'Status'] = [result]
        with pd.ExcelWriter("C:\\Users\\Rohit\\Desktop\\AlaMode\\{}.xlsx".format(month_selection)) as writer:
            for sheet, df in df.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
            writer.save()
            #df.to_excel(writer, sheet_name="Sheet1")
        #write_excel("C:\\Users\\Rohit\\Desktop\\AlaMode\\{}.xlsx".format(month_selection), 'Sheet1', df)
        #writer.save()
        #writer.close()
        df.iloc[0:0]
    df = pd.read_excel("C:\\Users\\Rohit\\Desktop\\AlaMode\\{}.xlsx".format(month_selection), 'Sheet1')
    df_expenses = pd.read_excel("C:\\Users\\Rohit\\Desktop\\AlaMode\\{}.xlsx".format(month_selection), 'Sheet2')

    numOfEarrings, SellP, CostP, ExpenseAmount = df['NumOfEarrings'].sum(), df['SellP'].sum(), df['CostP'].sum(), \
                                                 df_expenses['ExpenseAmount'].sum()
    new_row = ["Total: ", numOfEarrings, " - ", " - ", " - ", CostP, SellP, " - "]
    df = df.append(pd.Series(new_row, index=df.columns[:len(new_row)]), ignore_index=True)
    TotalEarnings, TotalExpenses = SellP - CostP, ExpenseAmount
    total_profit = TotalEarnings - TotalExpenses
    orders_data = df.to_html(classes='table table-striped table-hover table-bordered')
    expenses_data = df_expenses.to_html(classes='table table-striped table-sm')
    return render(request, "dashboard.html", {"OrdersCount": df.shape[0] - 1, "TotalEarnings": TotalEarnings,
                                              "TotalExpenses": TotalExpenses, "orders_data": orders_data,
                                              "expenses_data": expenses_data, "total_profit": total_profit,
                                              "month_selection": month_selection,
                                              "xl_months": xl_months})


def processorder(request):
    print("processing order")
    # if order placed successfully

    return redirect('ordercompleted')
    # else if issue with placing order redirect to failure page.


def ordercompleted(request):
    return render(request, "ordercompleted.html")

