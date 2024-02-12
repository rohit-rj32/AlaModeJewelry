console.log("Product details page");

function updatemainphoto(image){
    var mainimage = document.getElementById("main-image");
    mainimage.src = image.src;
}

function updateAvailablity(color){
    document.getElementById("add_to_cart_info").hidden =true;
    var divsToHide = document.getElementsByClassName("availablity_text"); //divsToHide is an array
    for(var i = 0; i < divsToHide.length; i++){
        divsToHide[i].hidden = true; // or
        //divsToHide[i].style.display = "none"; // depending on what you're doing
    }
    if (color.value != "Choose"){
        console.log(color.value);
        console.log("update the availability here")
        var add_to_cart_btn = document.getElementById("add_to_cart_pd");
        console.log(add_to_cart_btn);
        add_to_cart_btn.setAttribute("data-color", color.value);
        sel_color_img = document.getElementById(color.value);
        var mainimage = document.getElementById("main-image");
        mainimage.src = sel_color_img.src;



        document.getElementById("availablity_text_"+color.value).hidden = false;
        var availablity_text_element = document.getElementsByClassName("availablity_text_"+color.value)[0].value;
        document.getElementById("quantity_659eb96db11b2").max = availablity_text_element;
        document.getElementById("quantity_659eb96db11b2").value = 1;
        if( availablity_text_element > 0){
            console.log("products available");
            document.getElementById("quantity_659eb96db11b2").disabled = false;
            document.getElementById("add_to_cart_pd").style.pointerEvents = "auto";

        }
        else{
            document.getElementById("add_to_cart_pd").style.pointerEvents = "none";
            document.getElementById("quantity_659eb96db11b2").disabled = true;
        }

    }
    else{
        document.getElementById("add_to_cart_info").hidden =false;
        document.getElementById("add_to_cart_pd").style.pointerEvents = "none";
        //document.getElementById("add_to_cart_pd").data-color = "xxx";
    }
}