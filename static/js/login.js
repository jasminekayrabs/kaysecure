$(document).ready(function() {
  // Close the error message when the close button is clicked
  $('.close-btn').click(function() {
      $(this).closest('.message').fadeOut();
  });
});