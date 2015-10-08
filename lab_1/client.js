(function() {
  var net = require('net');

  var message = process.argv[2];

  var PORT = 8000,
    HOST = '0.0.0.0';

  // Create Socket connection
  var client = net.createConnection(PORT, HOST);

  client.on('connect', function() {
    console.log('Connected to: ' + HOST + ':' + PORT);
    client.write('GET /echo.php?message=' +
      encodeURI(message) +
      ' HTTP/1.0\r\n\r\n'
    );
    client.end();
  });

  var getBody = function(HTTPresponse) {
    var lastNewLinePos = HTTPresponse.lastIndexOf('\n');

    // Return body with no new preceding new line character
    return  HTTPresponse.slice(lastNewLinePos + 1);
  };

  // Add a 'data' event handler in order to process data that is sent from the
  // server
  client.on('data', function(data) {
    var message = data.toString();

    console.log('Data from Server: ' + getBody(message));

    // Close the client socket completely
    client.destroy();
  });

  // Add a 'close' event handler for the client socket
  client.on('close', function() {
    console.log('Connection closed');
  });
}());
