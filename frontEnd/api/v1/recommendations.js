var express = require('express')
var router = express.Router()
var adapter = require("../../pythonAdapter.js");


/**
 * @post impressions/buy
 * Post a buy impression
 * @body {userId:{int}}
 */
router.get("/anonymous",function(req, res) {
	console.log(adapter.Recommender.ANONYMOUS);
	adapter.send(adapter.Recommender.ANONYMOUS, 100, (response)=>{
		res.json(response);
	});
});

module.exports = router;