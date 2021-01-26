window.onload = dropdown_toggle();

function dropdown_toggle() {
  var keys = Object.keys(localStorage);
  for (x of keys) {
    console.log(x);
    if (x != "#sidebar" && x != "#content") {
      $(x).addClass("show");
    } else {
      $(x).addClass("active")
    }
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

function sidebar_state() {
  var sidebar_state = $("#sidebar").attr("class").split(/\s+/)
  var page_content = $("#content").attr("class").split(/\s+/)
  if ((sidebar_state.includes("active")) && page_content.includes("active")) {
    localStorage.removeItem("#sidebar")
    localStorage.removeItem("#content")
  } else {
    localStorage.setItem("#sidebar", "active")
    localStorage.setItem("#content", "active")
  }
}

$(function () {
  $('#sidebarCollapse').on('click', function () {
    $('#sidebar, #content').toggleClass('active');
  });
});