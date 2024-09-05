var navbar = document.getElementById("navbar");
var nav = document.getElementById("nav");
window.onscroll = function(){
  if (window.pageYOffset>=nav.offsetTop){
    navbar.classList.add("sticky")
  }
  else{
    navbar.classList.remove("sticky")
  }
}