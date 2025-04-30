Questa piattaforma è stata programmata sulla base delle esigenze di un piccolo/medio ristorante a conduzione familiare,
 quindi, è stato programmato in base alle esigenze, spazi e capacità del soggetto in questione.
Questa piattaforma è composta da:
  - Front-End:
	
	-Homepage: Pagina statica che serve da presentazione del locale con sezione chi siamo, menù, galleria e una 
	 sezione per accedere alle prenotazioni in piattaforma e alla gestione delle ultime;
	
	-Pagina di Prenotazione: Form per prenotare un tavolo in piattaforma con dati personali e conferma con un id 	 	 
	 univoco che rappresenta la prenotazione stessa;

	-Pagina di gestione: Pagina dedicata alla gestione della prenotazione, quindi, contiene due form, uno per 
	 richiamare la prenotazione tramite id e numero di telefono e uno per richiamarla tramite i dati inseriti al 	 	 
	 momento della prenotazione. Per quanto riguarda l'interfaccia, una volta richiamata la prenotazione e avviata
	 la modifica, si aprirà un form modal precompilato con la possibilità di cabliare i parametri e quindi la   	 	 
	 prenotazione stessa.

  - Back-End: 
	
	-Database (SQLite) viene gestito con Flask-SqlAlchemy, sviluppato in Flask.
 	
	  -API Restful che gestiscono:
		-Creazione della prenotazione con POST /bookings;
		-Recupero tramite codice o tramite query String con Get /bookings/<unique_code>;
		-Aggiornamento della prenotazione con Put /bookings/<unique_code>;
		-Cancellazione prenotazione con Delete /bookings/<unique_code>;
		-Funzione per sviluppatore o per back-office quindi cancellazione 
		 totale delle prenotazioni con Delete /bookings/clear.
	  
	  -Logica di gestione del limite delle prenotazioni (tramite numero dei tavoli):
		-40 tavoli standard per prenotazioni da 1 a 8 persone, con incremento una volta superati le 4
		 persone di +2 persone = + 1 tavolo, quindi 4 persone= 1 tavolo, 5 o 6 persone= 2 tavoli fino a 8 
		 persone con 3 tavoli;
		-2 tavoli grandi (da 9 a 11) ;
		-Prenotazioni da 12 a 15 persone tiene conto di un tavolo grande + 1 tavolo piccolo.
	  
	  -Validazione dei campi ad ogni richiesta tramite API.
  
  -Requisiti
	
	-Python 3.7+;
	-Flask;
	-Flask-SQLAlchemy;
	-Flask-CORS (usato per testare in ambiente virtale, avviando il frontend in locale, quindi da origini diverse).


---  Installazione e Avvio  ---

1. Creare un ambiente virtuale nella directory del progetto:
	
	cd littleitaly
	python -m venv venv
	venv\Scripts\activate   #windows
	source venv/bin/activate    #macOS/Linux

2. Installa le dipendenze:

	pip install -r requirements.txt

3. Avvia il backend:

	python app.py
  	
	(Il server dovrebbe essere in ascolto su http://127.0.0.1:5000).

4. Avvia il front-end tramite un server http:

	python -m http.server 8000

	Infine apri nel browser http://localhost:8000.


---  Struttura del progetto  ---


little-italy_web_v1.0/
│
├── backend/
│   ├── app.py                <-- File principale del backend in Python         										
│   └── requirements.txt      <-- Lista delle dipendenze in Python
│
├── frontend/
│   ├── index.html            <-- Homepage del sito
│   ├── booking.html          <-- Pagina di prenotazione
│   ├── management.html       <-- Pagina di gestione delle prenotazioni
│   ├── css/
│   │   └── style.css         <-- File CSS globale
│   └── js/
│       ├── main.js           <-- Funzioni js globali 
│       ├── booking.js        <-- Logica di prenotazione 
│       └── management.js     <-- Logica di gestione
│
└── README.md

Sviluppato da Matteo Vigliarolo come Project Work per il corso di laurea in informatica per le aziende digitali l-31
