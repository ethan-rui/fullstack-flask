$(document).ready(function () {
  dropdown_load()
})

// loads the state of each dropdown when page is loaded
function dropdown_load() {
  var keys = Object.keys(localStorage);
  for (x of keys) {
    if (x.substring(1).startsWith("submenu")) {
      $(x).addClass("show");
    } else {
      // if true, changes background of dropdown menu
      $(`#${x}`).attr("aria-expanded", "true")
    }
  }
}

//saves the state of each dropdown in the sidebar
function dropdown_save(target) {
  var submenu = $(target).attr("data-target");
  var list_classes = $(submenu).attr("class").split(/\s+/);
  // target id is used to set the color of the dropdown menu head
  // submenu is the targeted dropdown menu
  if (list_classes.includes("show")) {
    localStorage.removeItem(submenu);
    localStorage.removeItem(target.id)
  } else {
    localStorage.setItem(submenu, submenu);
    localStorage.setItem(target.id, target.id)
  }
}

// changes the width of the content and the sidebar
$('#sidebarCollapse').on('click', function () {
  $('#sidebar, #content').toggleClass('active');
});

