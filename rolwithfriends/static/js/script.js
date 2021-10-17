

$('#assetTypes li a').on('click', function(){
    var newWeapon = document.getElementById("newWeaponLayer");
    var newClothing = document.getElementById("newClotheLayer");
    var newObject = document.getElementById("newObjectLayer");

    switch($(this).text()){
        case "Weapons":
            if (newWeapon.style.display == "none"){
                newWeapon.style.display = "block";
            }
            else{
                newWeapon.style.display = "none";
            }
            break;
        case "Clothes":
            if (newClothing.style.display == "none"){
                newClothing.style.display = "block";
            }
            else{
                newClothing.style.display = "none";
            }
            break;
        case "Objects":
            if (newObject.style.display == "none"){
                newObject.style.display = "block";
            }
            else{
                newObject.style.display = "none";
            }
            break;
    }
})