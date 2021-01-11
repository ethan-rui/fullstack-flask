$(document).ready(dropdown_toggle());

function dropdown_toggle() {
  var keys = Object.keys(localStorage);
  for (x of keys) {
    console.log(x);
    $(x).addClass("show");
  }
}

function dropdown_save(target) {
  var id = $(target).attr("data-target").substring(1);
  var menu = "#".concat(id);
  var list_classes = $(menu).attr("class").split(/\s+/);
  if (list_classes.includes("show")) {
    localStorage.removeItem(menu);
  } else {
    localStorage.setItem(menu, menu);
  }
}

$(function () {
  $('#sidebarCollapse').on('click', function () {
    $('#sidebar, #content').toggleClass('active');
  });
});