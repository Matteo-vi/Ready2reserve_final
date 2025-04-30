$(document).ready(function(){
  function displayReservations(reservations) {
    if(reservations.length === 0) {
      $("#reservations-container").html("<p>Nessuna prenotazione trovata.</p>");
      return;
    }
    var html = '<div class="responsive-table"><table class="table table-bordered"><thead><tr>';
    html += '<th>Codice</th><th>Nome</th><th>Cognome</th><th>Servizio</th><th>Data</th><th>Orario</th><th>Azioni</th>';
    html += '</tr></thead><tbody>';
    $.each(reservations, function(i, res) {
      html += '<tr>';
      html += '<td>' + res.unique_code + '</td>';
      html += '<td>' + res.first_name + '</td>';
      html += '<td>' + res.last_name + '</td>';
      html += '<td>' + res.service_type + '</td>';
      html += '<td>' + res.booking_date + '</td>';
      html += '<td>' + res.booking_time + '</td>';
      html += '<td>';
      html += '<button class="btn btn-warning btn-sm btn-update" data-code="' + res.unique_code + '">Modifica</button> ';
      html += '<button class="btn btn-danger btn-sm btn-delete" data-code="' + res.unique_code + '">Cancella</button>';
      html += '</td>';
      html += '</tr>';
    });
    html += '</tbody></table></div>';
    $("#reservations-container").html(html);
  }
  
  // Funzione per recuperare prenotazioni tramite dati di prenotazione
  function getReservationsByData() {
    var queryParams = {
      first_name: $("#first_name").val().trim(),
      last_name: $("#last_name").val().trim(),
      phone: $("#phone").val().trim(),
      booking_date: $("#booking_date").val().trim()
    };
    var queryString = $.param(queryParams);
    $.ajax({
      url: "http://127.0.0.1:5000/bookings?" + queryString,
      type: "GET",
      success: function(response){
        $("#retrieve-data-feedback").removeClass("alert-danger").addClass("alert-success").html("Prenotazioni trovate.").show();
        displayReservations(response);
      },
      error: function(xhr){
        var err = "Errore sconosciuto";
        try {
          var json = JSON.parse(xhr.responseText);
          err = json.error;
        } catch(e){}
        $("#retrieve-data-feedback").removeClass("alert-success").addClass("alert-danger").html(err).show();
      }
    });
  }
  
  // Funzione per recuperare prenotazioni tramite codice e numero di cellulare
  function reSearchByCode() {
    var code = $("#unique_code").val().trim();
    var rc_phone = $("#rc_phone").val().trim();
    if (code === "" || rc_phone === "") {
      $("#reservations-container").html("<p>Nessuna prenotazione trovata.</p>");
      return;
    }
    $.ajax({
      url: "http://127.0.0.1:5000/bookings/" + code,
      type: "GET",
      success: function(response){
        if(response.phone && response.phone.trim() !== rc_phone) {
          $("#retrieve-code-feedback").removeClass("alert-success").addClass("alert-danger")
            .html("Il numero di cellulare non corrisponde alla prenotazione.").show();
          displayReservations([]);
        } else {
          displayReservations([response]);
          $("#retrieve-code-feedback").removeClass("alert-danger").addClass("alert-success")
            .html("Prenotazione trovata.").show();
        }
      },
      error: function(xhr){
        var err = "Errore sconosciuto";
        try {
          var json = JSON.parse(xhr.responseText);
          err = json.error;
        } catch(e){}
        $("#retrieve-code-feedback").removeClass("alert-success").addClass("alert-danger").html(err).show();
      }
    });
  }
  
  $("#retrieve-code-form").submit(function(e){
    e.preventDefault();
    reSearchByCode();
  });
  
  $("#retrieve-data-form").submit(function(e){
    e.preventDefault();
    getReservationsByData();
  });
  
  // Pulsante per cancellare prenotazione
  $(document).on("click", ".btn-delete", function(){
    var code = $(this).data("code");
    if(confirm("Sei sicuro di voler cancellare la tua prenotazione ?")) {
      $.ajax({
        url: "http://127.0.0.1:5000/bookings/" + code,
        type: "DELETE",
        success: function(response){
          alert(response.message);
          // Refresh della pagina dopo la cancellazione
          location.reload();
        },
        error: function(xhr){
          alert("Errore nella cancellazione: " + xhr.responseText);
        }
      });
    }
  });
  
  // Modal e precompilazione del form di modifica 
  $(document).on("click", ".btn-update", function(){
    var code = $(this).data("code");
    $.ajax({
      url: "http://127.0.0.1:5000/bookings/" + code,
      type: "GET",
      success: function(response){
        // Precompila il form con i dati ricevuti
        $("#update_unique_code").val(response.unique_code);
        $("#update_service_type").val(response.service_type);
        $("#update_booking_date").val(response.booking_date);
        $("#update_booking_time").val(response.booking_time);
        $("#update_people").val(response.people);
        $("#updateModal").modal("show");
      },
      error: function(xhr){
        alert("Errore nel recupero della prenotazione: " + xhr.responseText);
      }
    });
  });
  
  // Gestione del form per aggiornare la prenotazione
  $("#update-form").submit(function(e){
    e.preventDefault();
    var code = $("#update_unique_code").val().trim();
    var updateData = {
      service_type: $("#update_service_type").val(),
      booking_date: $("#update_booking_date").val(),
      booking_time: $("#update_booking_time").val(),
      people: $("#update_people").val()
    };
    $.ajax({
      url: "http://127.0.0.1:5000/bookings/" + code,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify(updateData),
      success: function(response){
        alert(response.message);
        $("#updateModal").modal("hide");
        displayReservations([response.booking]);
      },
      error: function(xhr){
        alert("Errore nella modifica: " + xhr.responseText);
      }
    });
  });
});
