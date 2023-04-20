/*
  Author: Bo Parker
  Date: 03/30/2022
*/

// nav menu button function
function menu() {
  var links = document.getElementById("mobile-nav");
  if (links.style.display === "block") {
    links.style.display = "none";
  } else {
    links.style.display = "block";
  }
}
