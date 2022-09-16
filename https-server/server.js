var express = require("express");
var app = express();
var bodyParser = require('body-parser');
const axios = require('axios');
var errorHandler = require('errorhandler');

var methodOverride = require('method-override');

var hostname = process.env.HOSTNAME || 'localhost';
var port = 8080;
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));


app.post('/sendFrame', function(req, res){
    axios.post("http://127.0.0.1:8000/sendFrame/", req.body ).then(function(response){
        res.end(JSON.stringify(response.data))
    }).catch(err => console.error(err));      
});

console.log("Simple static server listening at http://" + hostname + ":" + port);
// app.listen(port);
// DO NOT DO app.listen() unless we're testing this directly
if (require.main === module) { app.listen(8080); }
// Instead do export the app:
else{ module.exports = app; }