$(document).ready(function() {
  // Gestione del form di prenotazione
  $('#booking-form').submit(function(event) {
    event.preventDefault();
    $('#booking-feedback').empty();

    var bookFirstname = $('#book-firstname').val();
    var bookLastname = $('#book-lastname').val();
    var bookClientNumber = $('#book-client-number').val();
    var bookDate = $('#book-date').val();
    var bookTime = $('#book-time').val();
    var bookPeople = $('#book-people').val();
    var bookNotes = $('#book-notes').val();

    if (!bookFirstname || !bookLastname || !bookClientNumber || !bookDate || !bookTime || !bookPeople) {
      $('#booking-feedback').html('<p style="color:red;">Per favore, compila tutti i campi obbligatori.</p>');
      return;
    }

    var bookingData = {
      firstname: bookFirstname,
      lastname: bookLastname,
      clientNumber: bookClientNumber,
      date: bookDate,
      time: bookTime,
      people: parseInt(bookPeople),
      notes: bookNotes
    };

    console.log('Dati prenotazione:', bookingData);

    // Simulazione della chiamata API 
    setTimeout(function() {
      $('#booking-feedback').html('<p style="color:green;">Prenotazione inviata con successo!</p>');
      $('#booking-form')[0].reset();
    }, 1000);
  });

  // Gestione del form per la cancellazione della prenotazione
  $('#cancel-form').submit(function(event) {
    event.preventDefault();
    $('#cancel-feedback').empty();

    var cancelFirstname = $('#cancel-firstname').val();
    var cancelLastname = $('#cancel-lastname').val();
    var cancelReservationNumber = $('#cancel-reservation-number').val();

    if (!cancelFirstname || !cancelLastname || !cancelReservationNumber) {
      $('#cancel-feedback').html('<p style="color:red;">Per favore, compila tutti i campi obbligatori per la cancellazione.</p>');
      return;
    }

    var cancelData = {
      firstname: cancelFirstname,
      lastname: cancelLastname,
      reservationNumber: cancelReservationNumber
    };

    console.log('Dati cancellazione:', cancelData);

    // Simulazione della chiamata API per la cancellazione 
    setTimeout(function() {
      $('#cancel-feedback').html('<p style="color:green;">Prenotazione cancellata con successo!</p>');
      $('#cancel-form')[0].reset();
    }, 1000);
  });
});
