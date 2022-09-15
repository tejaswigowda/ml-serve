var fs = require('fs');

var express = require("express");
var app = express();
var bodyParser = require('body-parser');

var errorHandler = require('errorhandler');
var methodOverride = require('method-override');
var hostname = process.env.HOSTNAME || 'localhost';
var port = 8080;
app.use(methodOverride());
//app.use(bodyParser());
app.use(require('connect').bodyParser());
var Client = require('node-rest-client').Client;

var client = new Client();


// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

app.use(express.static(__dirname + '/public'));
app.use(errorHandler());

app.get("/", function (req, res) {
      res.redirect("/index.html");
});

app.post('/sendFrame', function(req, res){
    var base64Data = decodeURIComponent(req.body[Object.keys(req.body)[0]]);
   // base64Data = base64Data.split("------")[0];
    // set content-type header and data as json in args parameter
    var args = {
        data: base64Data,
        headers: { "Content-Type": "application/json" }
    };
    client.post("http://localhost:1234/sendFrame", args, function (data, response) {
        // parsed response body as js object
        console.log(data);
        // raw response
        res.send(response);
    }
        
});


console.log("Simple static server listening at http://" + hostname + ":" + port);
//app.listen(port);
// DO NOT DO app.listen() unless we're testing this directly
if (require.main === module) { app.listen(8080); }
// Instead do export the app:
else{ module.exports = app; }
