var fs = require('fs');
var ENVIRONMENT = false;

var DEVELOPMENT = "dev";
var LIVE = "live";

function getConfig(){
	if(!ENVIRONMENT){
		if(checkConfig(LIVE)){
			ENVIRONMENT = LIVE;
		} else if (checkConfig(DEVELOPMENT)){
			ENVIRONMENT = DEVELOPMENT;
		} else {
			console.log("No config file available");
			process.exit(1);
		}
	}
	return loadEnvironment();
}

/**
 * checkConfig
 * safely checks if a config file is there, and if it's accessible 
 * environment name;
 * @param {boolean} success
 */
function checkConfig(env){
	var path = getEnvironmentPath(env);
	try {
		return fs.existsSync(path) && !fs.accessSync(path, fs.F_OK);
	} catch (e) {
		// It isn't accessible
		console.log("access error while accessing config files");
		console.log(e);
		process.exit(1);
		return false;
	}
}

/**
 * gets the location of the environment config file.
 * @param {String} env
 */
function getEnvironmentPath(env){
	return process.cwd() + "/config/config." + env + ".json"
}

/**
 * loadEnvironment
 * appropriately loads the environment you want
 */
function loadEnvironment(){
	var config = require(getEnvironmentPath(ENVIRONMENT));
	config.environment = ENVIRONMENT;
	config.isLive = ENVIRONMENT == LIVE;
	config.isDev = ENVIRONMENT == DEVELOPMENT;
	return config;
}

module.exports = (function() {  
	// Singleton instance goes into this variable
	var instance;

	// Singleton factory method
	function factory() {
		return Math.random();
	}

	// Singleton instance getter
	function getInstance() {
		// If the instance does not exists, creates it
		if (instance === undefined) {
			instance = getConfig();
		}

		return instance;
	}

	// Public API definition
	return getInstance();
})();