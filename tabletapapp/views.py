from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Restaurant
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Restaurant, MenuCategory, MenuItem, Table, Order, OrderItem, Menu
import qrcode
import io
import base64


from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, "homepage.html")

    
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        restaurant_name = request.POST.get("restaurant_name")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")
        # create user
        user = User.objects.create_user(username=username, email=email, password=password)
        # create restaurant data and connect with user
        Restaurant.objects.create(owner=user, name=restaurant_name)
        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #Check that the username and password match a user in the database
        user = authenticate(request, username=username, password=password)
        
        print("username:", username)
        print("password:", password)
        print("authenticated user:", user)

        if user is not None:
            #Certified user is marked as "logged in" and the user's information is saved in the session.
            login(request, user)
            print("Login successful, redirecting to dashboard...")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "homepage.html")

def logout_view(request):
    #logout session
    logout(request)
    return redirect("homepage")

def homepage(request):
    return render(request, "homepage.html")

#Can only be accessed after logging in
@login_required 
def dashboard(request):
    # Get logged in user's restaurant
    restaurant = Restaurant.objects.get(owner=request.user)

    # Table manage include delete
    if request.method == "POST" and "manage_tables" in request.POST:
        count = int(request.POST.get("table_count")) # the number of table to create
        Table.objects.filter(restaurant=restaurant).delete()# Delete the current tables 
        for i in range(1, count + 1):
            Table.objects.create(restaurant=restaurant, number=i)#create table
        return redirect("/tabletapbuilder/dashboard/?section=manageTables")

    # qr code manage part
    tables = restaurant.table_set.order_by("number") # Get all the tables for this restaurant by reverse query
    qr_data = []
    for table in tables:
        # Create tables url
        url = request.build_absolute_uri(f"/tabletapbuilder/client/?restaurant={restaurant.id}&table={table.number}")
        
        qr = qrcode.make(url)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")# temp save to buffer
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()# encoding base 64

        # save to qr_data and send to dashboard page.
        qr_data.append({
            "table_number": table.number,
            "qr_code": qr_base64,
            "id": table.id
        })


    if request.method == "POST" and "delete_table_id" in request.POST:
        table_id = request.POST.get("delete_table_id")
        if table_id:
            Table.objects.filter(id=table_id, restaurant=restaurant).delete()
            return redirect("/tabletapbuilder/dashboard/?section=manageTables")

    # manage order status

    if request.method == "POST" and "complete_order_id" in request.POST:
        order_id = request.POST.get("complete_order_id")
        Order.objects.filter(id=order_id, table__restaurant=restaurant).update(status="completed")
        return redirect("/tabletapbuilder/dashboard/?section=viewOrders")


    # Swith menu to present
    current_menu_id = request.GET.get("menu_id") # get the menu id first
    if current_menu_id: # has menu if
        selected_menu = get_object_or_404(Menu, id=current_menu_id, restaurant=restaurant)# search menu base on menuid and restaturant info
    else:

        selected_menu = Menu.objects.filter(restaurant=restaurant).first()#get the first menu of this restaurant bt default

    # manu name edit
    if request.method == "POST" and "edit_menu_name" in request.POST:
        menu_id = request.POST.get("menu_id")
        new_name = request.POST.get("new_menu_name")
        Menu.objects.filter(id=menu_id, restaurant=restaurant).update(name=new_name)
        return redirect(f"/tabletapbuilder/dashboard/?menu_id={menu_id}")

    

    # menu addition 
    if request.method == "POST" and "add_menu" in request.POST:
        new_menu_name = request.POST.get("menu_name")
        if new_menu_name:
            Menu.objects.create(name=new_menu_name, restaurant=restaurant)
            return redirect("dashboard")
    
    # menu deletion 
    if request.method == "POST" and "delete_menu_id" in request.POST:
        menu_id = request.POST.get("delete_menu_id")
        Menu.objects.filter(id=menu_id, restaurant=restaurant).delete()
        return redirect("dashboard")


    # category addition
    if request.method == "POST" and "add_category" in request.POST:
        category_name = request.POST.get("category_name")
        if category_name:
            MenuCategory.objects.create(name=category_name, menu=selected_menu)
        return redirect(f"/tabletapbuilder/dashboard/?menu_id={selected_menu.id}")


    # item addition
    if request.method == "POST" and "add_menu_item" in request.POST:
        name = request.POST.get("item_name")
        price = request.POST.get("price")
        category_id = request.POST.get("category_id")
        if name and price and category_id:
            category = MenuCategory.objects.get(id=category_id)
            MenuItem.objects.create(name=name, price=price, category=category)
        return redirect(f"/tabletapbuilder/dashboard/?menu_id={category.menu.id}")


    # item edition
    if request.method == "POST" and "edit_item_id" in request.POST:
        item_id = request.POST.get("edit_item_id")
        new_name = request.POST.get("new_name")
        new_price = request.POST.get("new_price")
        MenuItem.objects.filter(id=item_id).update(name=new_name, price=new_price)
        item = MenuItem.objects.get(id=item_id)

        return redirect(f"/tabletapbuilder/dashboard/?menu_id={item.category.menu.id}")

    # item deletion
    if request.method == "POST" and "delete_item_id" in request.POST:
        item_id = request.POST.get("delete_item_id")
        item = MenuItem.objects.get(id=item_id)
        menu_id = item.category.menu.id
        item.delete() 

        return redirect(f"/tabletapbuilder/dashboard/?menu_id={menu_id}")
    


    # category edition
    if request.method == "POST" and "edit_category_id" in request.POST:
        cat_id = request.POST.get("edit_category_id")
        new_name = request.POST.get("new_category_name")
        MenuCategory.objects.filter(id=cat_id, menu__restaurant=restaurant).update(name=new_name)
        menu_id= MenuCategory.objects.get(id=cat_id)
        return redirect(f"/tabletapbuilder/dashboard/?menu_id={menu_id.menu.id}")

    # category deletion
    if request.method == "POST" and "delete_category_id" in request.POST:
        cat_id = request.POST.get("delete_category_id")
        category = MenuCategory.objects.get(id=cat_id)
        menu_id = category.menu.id
        category.delete()
        return redirect(f"/tabletapbuilder/dashboard/?menu_id={menu_id}")


    # menu_categories present at frontend
    
    if selected_menu:
        #From currently selected menu, get a list of all its associated MenuCategory objects.
        menu_categories = selected_menu.menucategory_set.all()
        for category in menu_categories:
            # Add an attribute menu_items, which holds all item in the category 
            category.menu_items = category.menuitem_set.all()
    else:
        menu_categories = []
    

    # Get all orders at this restaurant
    tables = restaurant.table_set.all()# Get all the tables in this restaurant
    orders_with_total = [] # calaulate total price

    for table in tables:
        for order in table.order_set.all():  # Get all orders for this table
            order_items = order.orderitem_set.all()  # et all order items under this order
            total = 0
            for item in order_items:
                total += item.item.price * item.quantity  # price calculation
            orders_with_total.append({
                "order": order,
                "total": total,
            })


    # get all menu of this restaurant
    menus = Menu.objects.filter(restaurant=restaurant)


    return render(request, "dashboard.html", {
        "restaurant": restaurant,
        "menu_categories": menu_categories,
        "tables": tables,
        "orders_with_total": orders_with_total,
        "qr_data": qr_data,
        "selected_menu": selected_menu,
        "menus": menus,


    })




def client_order_view(request):
    restaurant_id = request.GET.get("restaurant")
    table_number = request.GET.get("table")
    if not restaurant_id or not table_number:
        return HttpResponse("Invalid QR Code", status=400)

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    table = get_object_or_404(Table, restaurant=restaurant, number=table_number)

    menus = Menu.objects.filter(restaurant=restaurant)

    for menu in menus:
        menu.categories = menu.menucategory_set.all()  # Get all categories for this menu


        for category in menu.categories:
            category.menu_items = category.menuitem_set.all()  # Get all menu items under each category

        # structured data: menu -> categories -> item
    menu_data = []
    for menu in menus:
        categories = []
        for category in menu.menucategory_set.all():
            items = category.menuitem_set.all()
            categories.append({
                "category": category,
                "items": items
            })
        menu_data.append({
            "menu": menu,
            "categories": categories
        })

    return render(request, "client.html", {
        "restaurant": restaurant,
        "table": table,
        "menu_data": menu_data,
    })




@csrf_exempt  # Cross-Site Request Forgery
def place_order(request):
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant_id")
        table_id = request.POST.get("table_id")
        order_items_json = request.POST.get("order_items")

        if not restaurant_id or not table_id or not order_items_json:
            return HttpResponse("Missing order information", status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            table = Table.objects.get(id=table_id, restaurant=restaurant)
        except (Restaurant.DoesNotExist, Table.DoesNotExist):
            return HttpResponse("Invalid restaurant or table", status=404)

        order = Order.objects.create(table=table)

        order_items = json.loads(order_items_json)
        for item_id, details in order_items.items():
            try:
                menu_item = MenuItem.objects.get(id=item_id, category__menu__restaurant=restaurant)
                OrderItem.objects.create(
                    order=order,
                    item=menu_item,
                    quantity=details["quantity"]
                )
            except MenuItem.DoesNotExist:
                continue

        return HttpResponse(f"""
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Thank You - Tabletap</title>
                                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
                                </head>
                                <body>
                                    <div class="container text-center py-5">
                                        <h1 class="mb-3">Thank You!</h1>
                                        <p>Your order has been placed successfully.</p>
                                        <a href="/tabletapbuilder/client/?restaurant={restaurant_id}&table={table.number}" class="btn btn-primary mt-4">Back to Menu</a>
                                    </div>
                                </body>
                                </html>
                            """)

    return HttpResponse("Invalid request", status=405)