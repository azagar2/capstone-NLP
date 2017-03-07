var express = require('express')
var router = express.Router()
var adapter = require("../../pythonAdapter.js");

const DEFAULT_NUMBER_OF_RECOMMENDARIONS = 100;

/**
 * @post impressions/buy
 * Post a buy impression
 * @body {userId:{int}}
 */
router.get("/anonymous",function(req, res) {
	var count = parseInt(req.query.count) || DEFAULT_NUMBER_OF_RECOMMENDARIONS;
	adapter.send(adapter.Recommender.ANONYMOUS, count, (error,response)=>{
		if(error){
			return res.json({error});
		}
		res.json(response);
	});
});

module.exports = router;