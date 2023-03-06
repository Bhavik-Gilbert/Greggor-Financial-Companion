function showAlert(name) {
  confirm("Are you sure you want to delete this " + name + "?");
}

function autocomplete(id){
  $(document).ready(function() {
    $(id).select2();
  });
}
