var http = require("http");
var express = require("express");
var path = require("path");
var logger = require("morgan");
var bodyParser = require("body-parser");

var app = express();
app.use(logger("dev"));
app.use(bodyParser.json());
app.use("/",express.static(path.join(__dirname, "public")));

app.set('port', 9000);
var server = http.createServer(app);

/**
 * Listen on provided port, on all network interfaces.
 */

server.listen(9000,'localhost');
server.on('error', console.log);
server.on('listening', console.log);

PythonAdapter = require("./pythonAdapter.js")
var adapter = new PythonAdapter();


