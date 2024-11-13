document.addEventListener('DOMContentLoaded', function () {
  // Initialize QuaggaJS once the document is ready
  let currentEventId = null;

  // Event listener for barcode scan button click
  document.querySelectorAll('.barcode-scan-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      currentEventId = this.dataset.eventId;
      startBarcodeScan();
    });
  });

  function startBarcodeScan() {
    // Clear any previous results
    document.getElementById('barcode-result').innerHTML = '';

    // Initialize QuaggaJS
    Quagga.init(
      {
        inputStream: {
          name: 'Live',
          type: 'LiveStream',
          target: document.querySelector('#barcode-result') // This is where the webcam feed will be displayed
        },
        decoder: {
          readers: ['code_128_reader'] // Change to other barcode types as needed
        }
      },
      function (err) {
        if (err) {
          console.log(err);
          return;
        }
        Quagga.start();
      }
    );

    // Detect barcode
    Quagga.onDetected(function (result) {
      const barcode = result.codeResult.code;
      alert('Scanned Barcode: ' + barcode);

      // Send the barcode to the server to check if the event exists
      fetch(`/admin/events/check_barcode/${barcode}/`)
        .then(response => response.json())
        .then(data => {
          if (data.exists) {
            alert('Event Found: ' + data.event_title);
          } else {
            alert('Event not found.');
          }
        })
        .catch(err => {
          console.error('Error checking event:', err);
        });
    });
  }
});
