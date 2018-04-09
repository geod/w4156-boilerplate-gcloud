$(document).ready(function() {
  // === MATERIALIZE AND MDL UI ===
  $('.modal').modal()
  $('select').formSelect()
  $('.sidenav').sidenav()
  $('.datepicker').datepicker()
  $('#formatted_address').geocomplete({ details: 'form' })
})
