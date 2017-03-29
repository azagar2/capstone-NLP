var express = require('express')
var router = express.Router()

router.use("/impression",require("./impressions"));
router.use("/recommendations",require("./recommendations"));

module.exports = router;
