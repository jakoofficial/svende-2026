//Loading of the pages is done here

const pages = ["login.html", "overview.html"];

let selected_page = pages[0];

$(document).ready(function () {
  if (window.sessionStorage.getItem("lastOpened") == null) {
    GotoPage(selected_page);
  } else {
    GotoPage(window.sessionStorage.getItem("lastOpened"));
  }

  $("#headerInfo").append($("<header>").load("./extras/header.html"));
});

// Checks and removes old page info if existing
function GotoPage(page) {
  if (document.getElementById("page").childNodes.length > 0) {
    document.getElementById("page").firstChild.remove();
  }
  if (window.sessionStorage.getItem("sessionToken") == null){
    $("#page").append($("<section>").load("./pages/" + pages[0]));
  }
  else{
    $("#page").append($("<section>").load("./pages/" + page));
  }
  window.sessionStorage.setItem("lastOpened", page);
}
