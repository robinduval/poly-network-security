var all = document.getElementsByTagName("*");
for (var i=0, max=all.length; i < max; i++) {
 all[i].style.color = "green";
 all[i].style.background = "black";
 all[i].style.fontFamily = "Courier New";
 all[i].classList.remove("bg-white");
}
