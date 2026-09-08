//Loading of the pages is done here

const pages = ["login.html", "overview.html"]

let selected_page = "./pages/"+pages[1]

$(document).ready(function () {
  $("#page").append($("<section>").load(selected_page));

  $("#headerInfo").append($("<header>").load("./extras/header.html"));
});
