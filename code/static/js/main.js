$(document).ready(function() {
  // === MATERIALIZE AND MDL UI ===
  $('select').formSelect()
  $('.sidenav').sidenav()
  $('.datepicker').datepicker()
  $('#formatted_address').geocomplete({ details: 'form' })
})
