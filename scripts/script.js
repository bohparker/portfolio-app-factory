// nav menu button function
function menu() {
  var links = document.getElementById("mobile-nav");
  if (links.style.display === "block") {
    links.style.display = "none";
  } else {
    links.style.display = "block";
  }
}
