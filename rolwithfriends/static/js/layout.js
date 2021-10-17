$(document).ready(function(){
    
    
    var findings=[];
    console.log("Hola mundo");
})

async function SearchAssets(weapons){
    var x = document.getElementById("search-input").value.toLowerCase();
    var j = "";
    for(const weapon of weapons){
        if (weapon.weaponName.toLowerCase().includes(x)){
            j = j + "<a class='dropdown-item' href='asset/Weapon/" + weapon._id + "'>" + weapon.weaponName + "</a>";
        }
        document.getElementById("algolia-autocomplete-listbox-0").innerHTML = j;
    }
}