function buttonDisplay(obj) {
    if (document.getElementById(obj.id).checked == true) {
        document.getElementById("deleteselctd").style.display="block";
    } else {
         document.getElementById("deleteselctd").style.display="none";
    }
}


function checkAll(){
var cheks = document.body.getElementsByTagName("input");
var x = 0
// console.log(cheks);
// console.log(cheks[6]);
    for (var i = cheks.length-1; i>=0; i--) {
        // console.log(cheks[i]);
        if(document.getElementById("checkall").checked == true){
            document.getElementById("deleteselctd").style.display="block";


        if (cheks[i].getAttribute("class") == "items") {
            x += 1;
            console.log(x);
            // document.getElementById("checkcounter").innerHTML ="of" + " " + x + " " + "selected";
            console.log("if switch worck");
        cheks[i].checked="true";
  }
}      else {
        if (cheks[i].getAttribute("class") == "items") {


            cheks[i].checked=false;

            console.log("if switch worck2");
            document.getElementById("deleteselctd").style.display="none";
}
 }
}
}
