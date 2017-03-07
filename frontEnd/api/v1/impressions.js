var express = require('express')
var router = express.Router()
var adapter = require("../../pythonAdapter.js");

const requiredParams = {
	userId:true
}

/**
 * @post impressions/buy
 * Post a buy impression
 * @body {userId:{int}}
 */
router.post("/buy",function(req, res) {
	var error = getParamError(req.body,requiredParams);
	if(error){
		return res.json(error);
	}
	adapter.send(adapter.Impressions.BUY, req.body.userId, (error,response)=>{
		if(error){
			return res.json({error});
		}
		res.json(response);
	});
});

/**
 * @post impressions/exclude
 * Post a exclude impression
 * @body {userId:{int}}
 */
router.post("/exclude",function(req, res) {
	var error = getParamError(req.body,requiredParams);
	if(error){
		return res.json(error);
	}
	adapter.send(adapter.Impressions.EXCLUDE, req.body.userId, (error,response)=>{
		if(error){
			return res.json({error});
		}
		res.json(response);
	});
});

/**
 * @post impressions/click
 * Post a click impression
 * @body {userId:{int}}
 */
router.post("/click",function(req, res) {
	var error = getParamError(req.body,requiredParams);
	if(error){
		return res.json(error);
	}
	adapter.send(adapter.Impressions.CLICK, req.body.userId, (error,response)=>{
		if(error){
			return res.json({error});
		}
		res.json(response);
	});
});

/**
 * get Parameter Error
 * parameter Error is in the format. We don't check types, service does that.
 * { "({String} parameter name)":({Class} required)}
 * @param {Object} params
 * @param {Object} configParams
 */
function getParamError(params,configParams){
	var keys = Object.keys(params);
	if(keys.length > params.length){
		return {
			"error":"too many params"
		};
	}
	for (var i = 0; i < keys.length; i++) {
		if(!(keys[i] in configParams)){
			return {
				"error":"unknown parameter "+keys[i]
			};
		}
	}
	for (var key in configParams) {
		if(configParams[key] && !(key in  params)){
			return {
				"error":"missing required parameter "+ key
			};
		}
	}
	return null;
}

module.exports = router;