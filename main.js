// ----------------------------------
// CUSTOM JAVASCRIPT
// ----------------------------------

// Iframe url
function loadIframe(iframeName, url) {
  var $iframe = $('#' + iframeName);
  if ($iframe.length) {
    $iframe.attr('src', url);
    return false;
  }
  return true;
}

// Collapse sidebar on click
$('.sidebarContent>li>a').on('click', function() {
  $('.sidebar').collapse('hide');
});
