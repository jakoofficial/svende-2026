//Loading of the pages is done here

const pages = ["login.html", "overview.html"];

let selected_page = pages[1];

$(document).ready(function () {
  GotoPage(selected_page)
  // $("#page").append($("<section>").load(selected_page));

  $("#headerInfo").append($("<header>").load("./extras/header.html"));
});

// Checks and removes old page info if existing
function GotoPage(page) {
  if (document.getElementById("page").childNodes.length > 0) {
    document.getElementById("page").firstChild.remove();
  }
  $("#page").append($("<section>").load("./pages/" + page));
}

