function message(message, color, div) {
  if (div == null)
    $msg = $("#message");
  else
    $msg = $(div);

  if (color == null)
    $msg.css('color', 'black');
  else
    $msg.css('color', color);
  $msg.html(message);
  $msg.slideDown();
  setTimeout('$("#' + $msg.attr("id") + '").slideUp()',3000);
}
