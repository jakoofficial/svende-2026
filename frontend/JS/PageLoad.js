//Loading of the pages is done here

const pages = ["login.html"]

let selected_page = "./pages/"+pages[0]

$(document).ready(function () {
  $("#page").append($("<section>").load(selected_page));
});
