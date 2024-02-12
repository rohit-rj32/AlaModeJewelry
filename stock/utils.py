import json
from .models import *


def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    total = 0

    for earring_name in cart:
        print("earring_name {}".format(earring_name))
        for color in cart[earring_name].keys():
            print("Color {}".format(color))
            if cart[earring_name][color]['quantity'] > 0:
                item = ItemDetails.objects.get(ItemSlug=earring_name)
                item_color = item.Item_images.get(ItemColors=color)
                quantity_in_cart = cart[earring_name][color]['quantity']
                quantity_avail_stock = item_color.ItemAvailCount
                if quantity_in_cart > quantity_avail_stock:
                    quantity_in_cart = quantity_avail_stock
                    cart[earring_name][color]['quantity'] = quantity_in_cart
                cartItems += cart[earring_name][color]['quantity']
                print("cartItems {}".format(cartItems))
                print("item {}".format(item))
                total = total + (item.ItemPrice * quantity_in_cart)
                print("total,quantity_in_cart {},{}".format(total, quantity_in_cart))
                order['get_cart_total'] = total
                order['get_cart_items'] += quantity_in_cart

                # print(item_color)
                # quantity_in_cart = cart[earring_name][color]['quantity']
                # quantity_avail_stock = item_color.ItemAvailCount
                # if quantity_in_cart > quantity_avail_stock:
                #     quantity_in_cart = quantity_avail_stock

                item = {
                    'id': item.ItemID,
                    'product': {'id': item.ItemID, 'name': item.ItemName, 'price': item.ItemPrice,
                                'imageURL': item_color.ItemImage, 'color': item_color.ItemColors,
                                'slug': item.ItemSlug},
                    'quantity': quantity_in_cart, 'get_total': total,
                }
                print(item)
                items.append(item)

        #         if product.digital == False:
        #             order['shipping'] = True
        # except:
        #     pass
        print("$$$$$$$$")
        print(cart)
        request.COOKIES['cart'] = cart
    return {'cartItems': cartItems, 'order': order, 'items': items, 'cart': cart }

# not in use updating the cart directly in js
'''
def delItemFromCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)
    print(cart)
    itemname = request.POST.get("ItemToDelete")
    itemcolor = request.POST.get("ItemColor")
    del cart[itemname][itemcolor]
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    total = 0

    for earring_name in cart:
        print("earring_name {}".format(earring_name))
        for color in cart[earring_name].keys():
            print("Color {}".format(color))
            if cart[earring_name][color]['quantity'] > 0:
                item = ItemDetails.objects.get(ItemSlug=earring_name)
                item_color = item.Item_images.get(ItemColors=color)
                quantity_in_cart = cart[earring_name][color]['quantity']
                quantity_avail_stock = item_color.ItemAvailCount
                if quantity_in_cart > quantity_avail_stock:
                    quantity_in_cart = quantity_avail_stock
                    cart[earring_name][color]['quantity'] = quantity_in_cart
                cartItems += cart[earring_name][color]['quantity']
                print("cartItems {}".format(cartItems))
                print("item {}".format(item))
                total = total + (item.ItemPrice * quantity_in_cart)
                print("total,quantity_in_cart {},{}".format(total, quantity_in_cart))
                order['get_cart_total'] = total
                order['get_cart_items'] += quantity_in_cart

                # print(item_color)
                # quantity_in_cart = cart[earring_name][color]['quantity']
                # quantity_avail_stock = item_color.ItemAvailCount
                # if quantity_in_cart > quantity_avail_stock:
                #     quantity_in_cart = quantity_avail_stock

                item = {
                    'id': item.ItemID,
                    'product': {'id': item.ItemID, 'name': item.ItemName, 'price': item.ItemPrice,
                                'imageURL': item_color.ItemImage, 'color': item_color.ItemColors,
                                'slug': item.ItemSlug},
                    'quantity': quantity_in_cart, 'get_total': total,
                }
                print(item)
                items.append(item)

        #         if product.digital == False:
        #             order['shipping'] = True
        # except:
        #     pass
        print("$$$$$$$$")
        print(cart)
        request.COOKIES['cart'] = cart
    return {'cartItems': cartItems, 'order': order, 'items': items, 'cart': cart}
'''
