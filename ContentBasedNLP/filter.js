var fs = require("fs");

var fileName = process.argv[3] || "output.json";

var data = '';
var keys = [];
var index = 0;
var lastInput = "";
var renaming = false;
var renamingBuffer = "";
var renamedKeys = {};
if(process.argv.length < 3){
	display("please input a file",true);
	process.stdin.resume();
	process.stdin.setEncoding('utf8');
	process.stdin.once("data", function (input) {
		display("loading...")
		try{
			data = require("./"+input.trim());
		} catch(error){
			display("ERROR: no such file",true);
			process.exit(1);
		}
		display("file loaded",true);
		filter();
	});
} else {
	try{
		data = require("./"+process.argv[2].trim());
	} catch(error){
		display("ERROR: no such file",true);
		process.exit(1);
	}
	filter();
}

function filter(){
	keys = Object.keys(data[0]).map((element)=>{
		renamedKeys[element] = element;
		return {name:element,enabled:true}
	});
	render();
	process.stdin.setRawMode( true );
	process.stdin.setEncoding( 'utf8' );
	process.stdin.on("data", function (key) {
		if(renaming){
			renamingBuffer += key;
			if( key === '\r'){
				renaming = false;
				rename();
				render();
				return;
			}
			renderRename();
			return;
		}

		if (key == '\u001B\u005B\u0041') {
			if(index > 0){
				index--
			}
		}
		if (key == '\u001B\u005B\u0042') {
			if(index < keys.length){
				index++
			}
		}
		if( key === '\r'){
			if(index !== keys.length){
				keys[index].enabled = !keys[index].enabled;				
			} else {
				output();
			}
		}
		if( key === 'r'){
			renaming = true;
			renamingBuffer = "";
			process.stdout.write('\033c');
			renderRename();
			return;
		}
		if(index == keys.length){
			if( key == 'n'){
				process.stdout.write('\033c');
				process.exit();
			}
			if( key == 'y'){
				output();
			}
		}
		render();
		if ( key === '\u0003' ) {
			process.stdout.write('\033c');
			process.exit();
		}
		return false;
	});
}

function render(){
	process.stdout.write('\033c');
	keys.forEach((key, idx)=>{
		
		var message = "";
		if(idx == index){
			message = "> "
		}
		message += "key: "+renamedKeys[key.name];
		var length = (30 - message.length > 0)?30 - message.length:5;
		message += " ".repeat(length) + "enabled: "+key.enabled;
		console.log(message);
	})
	display("done");
	if(index == keys.length){
		display("filter? (y/enter) exit? (n)")
	}
}

function renderRename(){
	display("renaming \""+keys[index].name+"\" to "+renamingBuffer);
}

function rename(){
	renamedKeys[keys[index].name] = renamingBuffer.trim();
}

function output(){
	process.stdout.write('\033c');
	display("writing");

	fs.writeFile(fileName,JSON.stringify(data.map((event)=>{
		var item = {};
		keys.forEach((key)=>{
			if(key.enabled){
				item[renamedKeys[key.name]] = event[key.name];
			}
		});
		return item;
	}), null, 4), function (err){
		if(err){
			console.log(err);
			return
		}
		display("write successful",true);
		process.exit(1);
	});
}

function display(line,newLine){
	process.stdout.write("\b".repeat(lastInput+1));
	process.stdout.write(line);
	if(lastInput > line.length){
		process.stdout.write(" ".repeat(lastInput - line.length));
		process.stdout.write("\b".repeat(lastInput - line.length));
	}
	if(newLine){
		process.stdout.write("\n");
		line = "";
	}
	lastInput = line.length;
}