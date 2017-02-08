var net = require("net");

const BLUE_SHIFT_ADAPTER = '/tmp/blue-shift-adapter';

function PythonAdapter(){
	this.commandId = 1;
	this.callbacks ={};
	this.error = console.log.bind(this,"PYTHON::ERROR::");
	this.client = net.connect({path: BLUE_SHIFT_ADAPTER},()=>{
		console.log('connected to server!');
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
	}
}

PythonAdapter.Impressions = {
	CLICK : "clickImpression",
	EXCLUDE: "excludeImpression",
	BUY : "buyImpression"
}

PythonAdapter.Biases = {
	ADD:'addBias',
	DELETE:'deleteBias',
	LIST:'listBiases',
}

module.exports = PythonAdapter;