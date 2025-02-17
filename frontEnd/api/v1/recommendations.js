var express = require('express')
var router = express.Router()
var adapter = require("../../pythonAdapter.js");

const DEFAULT_NUMBER_OF_RECOMMENDARIONS = 20;
const RESPONSE_DELAY_WARNING = 2000;
/**
 * @post impressions/buy
 * Post a buy impression
 * @body {userId:{int}}
 */
router.get("/anonymous",function(req, res) {
	var messageRecievedTime = Date.now();
	var count = parseInt(req.query.count) || DEFAULT_NUMBER_OF_RECOMMENDARIONS;
	console.log("JUST AN I GOT HERE");
	adapter.send(adapter.Recommender.ANONYMOUS, count, (error,response)=>{
		if(error){
			return res.json({error});
		}
		var now = Date.now()
		if(now - messageRecievedTime > RESPONSE_DELAY_WARNING){
			console.log("WARNING:HIGH LOAD:"+now);
		}
		res.json(response);
	});
});

router.get("/user",function(req, res) {
	var event1 = req.query.event1 || "None";
	var event2 = req.query.event2 || "None";
	var event3 = req.query.event3 || "None";
	adapter.send(adapter.Recommender.USER, event1, event2, event3, (error,response)=>{
		if(error){
			return res.json({error});
		}
		res.json(response);
	});
});

module.exports = router;
