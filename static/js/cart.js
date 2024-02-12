// this block of code is for pop up confirmation in cart details when deleting the item.
//$('#myModal').on('shown.bs.modal', function () {
//  $('#myInput').trigger('focus')
//})
function updateCookieQuantity(name) {
    console.log("cart button clicked we have to update the cookiee from actual availablity here")
}
function getCookie(name) {
		    // Split cookie string and get all individual name=value pairs in an array
		    var cookieArr = document.cookie.split(";");
            console.log(cookieArr)
		    // Loop through the array elements
		    for(var i = 0; i < cookieArr.length; i++) {
		        var cookiePair = cookieArr[i].split("=");
		        if(name == cookiePair[0].trim()) {
		            return decodeURIComponent(cookiePair[1]);
		        }
		    }

		    // Return null if not found
		    return null;
		}
var sPath = window.location.pathname;
var sPage = sPath.substring(sPath.lastIndexOf('/') + 1);
console.log(sPage)
var cart = JSON.parse(getCookie('cart'))
console.log("cart.js started")
console.log(cart)

// this block of code to set the item to delete in cart details page
$(function () {
        $(".identifyingClass").click(function () {
            var my_item_name= $(this).data('item');
            var my_item_color = $(this).data('color');
            console.log(my_item_name)
            console.log(my_item_color)
            $(".modal-body #ItemToDelete").val(my_item_name);
            $(".modal-body #ItemColor").val(my_item_color);
        })
});
$(function () {
        $(".confirmationclass").click(function () {
            console.log("confirm deletion")
            debugger;
            var my_item_name = document.getElementById("ItemToDelete").value;
            var my_item_color = document.getElementById("ItemColor").value;
            console.log(my_item_name)
            console.log(my_item_color)
            debugger;
            delete cart[my_item_name][my_item_color]
            document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
            debugger;
        })
});

if (sPage == 'cartdetails' || sPage == 'delcartitem'){
    console.log("do stuff cookiee udpate")
    console.log(cart)
    for (var i in cart) {
        console.log(i)
	    for (var j in cart[i]){
	        var quantity_actual = document.getElementById(i+"-"+j+"-"+"quantity")
	        //console.log(parseInt(quantity_actual.innerHTML))
	        cart[i][j]['quantity'] = parseInt(quantity_actual.innerHTML)
	    }
    }
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
if (cart == undefined){
			cart = {}
			console.log('Cart Created!', cart)
			document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		}
var updateBtn = document.getElementsByClassName("update-cart")
//console.log(updateBtn)
console.log("after actual qunatity code")
console.log(cart)

for (i = 0; i < updateBtn.length; i++) {
	updateBtn[i].addEventListener('click', function(){
		var itemSlug = this.dataset.item
		var itemColor = this.dataset.color
		var action = this.dataset.action
		console.log('itemSlug:', itemSlug, 'itemColor', itemColor, 'Action', action)
		//console.log('USER:', user)
        var cartNum = document.getElementById("cartcount").innerHTML;
        cartNum++;
        console.log(cartNum)
        addCookieItem(itemSlug,itemColor, action)
	})
	}

function addCookieItem(itemSlug, itemColor, action){
	//console.log('User is not authenticated')
	console.log(cart?.itemSlug?.itemColor)
    console.log(action)
	if (action == 'add'){
		if (cart[itemSlug] == undefined){
		//Object.assign(cart[itemSlug], {[itemColor]: {'quantity':1}});
		quantity_val = parseInt(document.getElementById("quantity_659eb96db11b2").value, 10);
		console.log(quantity_val)
		cart[itemSlug] = {[itemColor]:{'quantity':quantity_val}}
		//cart[itemSlug] = {'color':itemColor}

		}else {
		if (cart[itemSlug][itemColor] == undefined){
		    console.log("earring with one colour exists trying to add another color again");
		    console.log(cart[itemSlug]);
		    quantity_val = parseInt(document.getElementById("quantity_659eb96db11b2").value, 10);
		    cart[itemSlug][itemColor] = {'quantity':quantity_val}
		}
		else{
		    quantity_val = parseInt(document.getElementById("quantity_659eb96db11b2").value, 10);
		    //cart[itemSlug][itemColor] = {'quantity':quantity_val}
		    console.log("HHHHH")
		    console.log(cart[itemSlug][itemColor]['quantity'])
		    cart[itemSlug][itemColor]['quantity'] += quantity_val
		}
		console.log("ADD ITEM TO CART"+cart)
//		for (var i in cart) {
//	        for (var j in cart[i]){
//	            console.log(j);
//	            console.log(itemColor)
//	            if (j == itemColor){
//	                console.log("Item with same color already exists")
//	                cart[i][j]['quantity'] +=1
//	            }
//	            console.log(cart[i][j]);
//	            //cart_val = cart_val + cart[i][j]['quantity'];
//	        }
//        }
		//console.log(cart[itemSlug][itemColor]['quantity']);
		//cart[itemSlug][itemColor]['quantity'] +=1
		//console.log(cart[itemSlug][itemColor]['quantity']);
		//Object.assign(cart[itemSlug][itemColor], {[itemColor]: {'quantity':1}});
//		for (var item in cart[itemSlug]) {
//            console.log('key:' + item + ' value:' + cart[itemSlug][item]);
//            if (item == itemColor ){
//                console.log("Color is already present increase the quantity")
//                cart[itemSlug]['quantity'] += 1
//            }
//        }
//		if (cart[itemSlug]['color']){
//		    console.log("######");
//		    console.log(cart[itemSlug]['color']);
//		    console.log("######");
//		}
		    //if (cart[itemSlug][])
			//cart[itemSlug][itemColor]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[itemSlug][itemColor]['quantity'] -= 1

		if (cart[itemSlug][itemColor]['quantity'] <= 0){
			//console.log('Item should be deleted')
			delete cart[itemSlug][itemColor];
		}
	}
	console.log('CART:', cart)
	var cart_val = document.getElementById("cartcount").innerHTML;
	console.log(cart_val)

	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	//for(let i = 0; i <ca.length; i++)
	//console.log(cart[itemSlug]['quantity'])
	//console.log(document.cookie)
	var cart_val = 0;
	for (var i in cart) {
	    for (var j in cart[i]){
	        cart_val = cart_val + cart[i][j]['quantity'];
	    }
    }
    //console.log(cart_val)
    document.getElementById("cartcount").innerHTML = cart_val;
	//location.reload()
}
    console.log("@@@@@@@")
    console.log(document.cookie);

   // var cart_val = 0;
	//for (var i in cart) {
	//    for (var j in cart[i]){
	//        cart_val = cart_val + cart[i][j]['quantity'];
	//    }
    //}
    //console.log(cart_val)
   // document.getElementById("cartcount").innerHTML = cart_val;
