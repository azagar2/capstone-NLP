var net = require("net");

const BLUE_SHIFT_ADAPTER = '/tmp/blue-shift-adapter';
const REQUESTS_PER_SECOND = 5;
const RATE_LIMIT = 1000/REQUESTS_PER_SECOND;

function PythonAdapter(){
	this.lastTimeStamp = Date.now();
	this.debounceActive = false;
	this.commandId = 1;
	this.commandBuffer = [];
	this.buffer = {};
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
		//process.exit(1);
	});
	this.client.on('data', (data) => {
		data = data.toString();
		data = data.split("&&");
		var lastDatagram = data.pop();
		// reconstruct overflow
		if(this.overflow){
			data[0] = this.overflow + data[0];
			this.overflow = false;
		}
		// more overflow
		if(lastDatagram != ""){
			this.overflow = lastDatagram;
		}
		data.forEach(this.assembleMessage.bind(this));
	});
	this.client.on('end', () => {
		this.error('disconnected from server');
		this.close();
		//process.exit(1);
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
		var now = Date.now();
		var params = Array.prototype.slice.call(arguments);
		// don't make me check this.
		var command = params.shift();
		var callback = params.pop();
		// check callback.
		if(typeof callback !== "function") return console.log("ERROR: last parameter must be a callback");
		// NOTE: if multiple servers are deployed, this will need to be adjusted.
		var id = this.commandId++;
		this.callbacks[id] = callback;
		var commandString = JSON.stringify({command,params,id});
		// debounce code
		if(this.debounceActive){
			this.commandBuffer.push(commandString);
			return;
		}
		// start debounce, too many consecutive messages
		if((now - this.lastTimeStamp) < RATE_LIMIT){
			this.debounceActive = true;
			this.commandBuffer.push(commandString);
			this.rateLimit();
			console.log("WARNING:MEDIUM LOAD:"+now);
			return;
		}
		// update
		this.lastTimeStamp = now;
		this.client.write(commandString);
	},

	/**
	 * Rate Limit
	 * High load! python server can only handle a
	 * certain number requests/second.
	 */
	rateLimit(){
		this.debounceClear = setInterval(()=>{
			if(!this.commandBuffer.length){
				this.debounceActive = false;
				clearInterval(this.debounceClear);
				return;
			}
			this.client.write(this.commandBuffer.shift());
		},RATE_LIMIT);
	},

	/**
	 * Assemble Message
	 * Assemble message from message datagrams
	 * and parse it into a message
	 * @param {String} data
	 */
	assembleMessage: function(data){
		control = data.substr(0,data.indexOf("|"));
		data = data.substr(data.indexOf("|")+1);
		control = control.split(":");
		//this.debug("response "+control[0]+ ": got message "+(parseInt(control[1])+1)+" of "+(parseInt(control[2])+1));
		// single frame message or error message
		if(control[0] == "e" || control[2] == "1"){
			return this.gotMessage(JSON.parse(data));
		}
		// message incomplete, wait for the rest
		if(!this.buffer[control[0]]){
			this.buffer[control[0]] = {remaining:control[2]};
		}
		this.buffer[control[0]][control[1]] = data;
		if(this.buffer[control[0]].remaining-- !== 0){
			return
		}
		// message complete, assemble it.
		var buffer = "";
		for (var i = 0; i <= control[2]; i++) {
			buffer+= this.buffer[control[0]][i];
			delete this.buffer[control[0]][i];
		}
		delete this.buffer[control[0]]
		return this.gotMessage(JSON.parse(buffer));
	},

	/**
	 * Got Message
	 * got a complete message from the server
	 * @param {json object} message
	 */
	gotMessage: function(message){
		if(message.error){
			this.error(message.error);
			this.callbacks[message.id](message.error)
			if(message.id !== undefined) delete this.callbacks[message.id];
		} else {
			this.callbacks[message.id](null,message.response);
		}
		delete this.callbacks[message.id];
	},

	/**
	 * Close
	 * Lost connection to python :(
	 */
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

PythonAdapter.prototype.Recommender = {
	ANONYMOUS:'getAnonymousRecommendations',
	USER: 'getRecommendations'
}

module.exports = (function() {
	// Singleton instance goes into this variable
	var instance;

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
