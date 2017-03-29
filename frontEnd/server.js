/**
 * required modules
 */
var express = require("express");
var path = require("path");
var logger = require("morgan");
var bodyParser = require("body-parser");

var config = require("./config");
/**
 * Config Variables
 */
var CURRENT_VERSION = config.version || 1;

/**
 * express instance
 */
var app = express();
if(config.isDev){
	app.use(logger("dev"));
}
app.use(bodyParser.json())

// load or run all active versions
var versions = [CURRENT_VERSION];
if(config.legacy){
	versions.concat(config.legacy.versions);
}

// run all active versions.
for(var versionId in versions){
	var VERSION = versions[versionId];
	try{
		var router = require("./api/v"+VERSION+"/");
		app.use("/api/v"+VERSION,router);
		if(VERSION == CURRENT_VERSION){
			app.use("/api/",router);
		}
	}catch(error){
		console.log("ERROR: could not run api version "+VERSION);
		// ignore only if it's live.
		if(config.isDev) throw error;
	}
}


app.use("/",express.static(path.join(__dirname, "public")));

// fallback is a basic version endpoint
app.use("/", function(req, res){
	res.json({name: config.name, version: CURRENT_VERSION+"-"+config.environment});
});

module.exports =  app;
