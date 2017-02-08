var express = require('express')
var router = express.Router()

router.use("/impression",require("./impressions"));

module.exports = router;
