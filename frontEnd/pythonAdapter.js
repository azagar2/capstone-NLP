var net = require("net");

const BLUE_SHIFT_ADAPTER = '/tmp/blue-shift-adapter';

function PythonAdapter(){
	this.commandId = 1;
	this.callbacks ={};
	this.error = console.log.bind(this,"PYTHON::ERROR::");
	this.debug = console.log.bind(this,"PYTHON::DEBUG::");
	this.client = net.connect({path: BLUE_SHIFT_ADAPTER},()=>{
		this.debug('connected to server!');
	});
	this.client.on('error',(error)=>{
		if (error.syscall !== 'connect' && error.code !== 'ECONNREFUSED') {
			throw error;
		}
		this.error("no server running on "+BLUE_SHIFT_ADAPTER);
		process.exit(1);
	});
	this.client.on('data', (data) => {
		data = JSON.parse(data);
		if(data.error){
			this.error(data.error);
			if(data.id !== undefined) delete this.callbacks[data.id];
		} else {
			this.callbacks[data.id](data.response);
		}
		delete this.callbacks[data.id];
	});
	this.client.on('end', () => {
		this.error('disconnected from server');
		this.close();
		process.exit(1);
	});
}

PythonAdapter.prototype = {
	/**
	 * send arbitary command.
	 * for example:
	 * 		send(PythonAdapter.Biases.LIST, true, ()=>{//callback})
	 * 		send(PythonAdapter.Biases.ADD, 4,"admin",100,1485957433624,1486907833624, ()=>{//callback})
	 * NOTE: first param must be the **NAME** of the command
	 * NOTE: last param must be callback
	 */
	send: function(){
		var params = Array.prototype.slice.call(arguments);
		// don't make me check this.
		var command = params.shift();
		var callback = params.pop();
		// check callback.
		if(typeof callback !== "function") return console.log("ERROR: last parameter must be a callback");
		// NOTE: if multiple servers are deployed, this will need to be adjusted.
		var id = this.commandId++;
		this.callbacks[id] = callback;
		this.client.write(JSON.stringify({command,params,id}));
	},

	close: function(){
		this.error("shutting down");
		this.client.destroy();
	}
}

PythonAdapter.prototype.Impressions = {
	CLICK : "clickImpression",
	EXCLUDE: "excludeImpression",
	BUY : "buyImpression"
}

PythonAdapter.prototype.Biases = {
	ADD:'addBias',
	DELETE:'deleteBias',
	LIST:'listBiases',
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
			instance = new PythonAdapter();
		}

		return instance;
	}

	// Public API definition
	return getInstance();
})();