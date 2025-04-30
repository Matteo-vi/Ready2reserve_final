
  $(document).ready(function(){
  $("#booking-form").submit(function(e){
    e.preventDefault();
    
    // Raccogli i dati dal form
    var formData = {
      first_name: $("#first_name").val(),
      last_name: $("#last_name").val(),
      phone: $("#phone").val(),
      email: $("#email").val(),
      service_type: $("#service_type").val(),
      people: $("#people").val(),
      booking_date: $("#booking_date").val(),
      booking_time: $("#booking_time").val(),
      notes: $("#notes").val()
    };
    
    // Chiamata AJAX al backend
    $.ajax({
      url: "http://127.0.0.1:5000/bookings",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(formData),
      success: function(response){
        $("#booking-feedback")
          .removeClass("alert-danger")
          .addClass("alert-success")
          .html(response.message + "<br>Codice Prenotazione: " + response.booking.unique_code)
          .show();
      },
      error: function(xhr){
        var err = "Errore sconosciuto";
        try {
          var json = JSON.parse(xhr.responseText);
          err = json.error;
        } catch(e){}
        $("#booking-feedback")
          .removeClass("alert-success")
          .addClass("alert-danger")
          .html(err)
          .show();
      }
    });
  });
});
