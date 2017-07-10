const express = require('express')
const bodyParser = require('body-parser')
const fs = require('fs')
const url = require('url')
const app = express()
const PythonShell = require('python-shell')

app.use(express.static(__dirname));

const urlencodedParser = bodyParser.urlencoded({ extended: false })

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html')
})

app.post('/save', urlencodedParser, (req, res) => {
  filePath = __dirname + '/test-results.txt'
  let body = JSON.stringify(req.body['message[]']);
  body = ',' + body;
  body = body.replace(/\\n/g, '\n').replace(/\[/g, '').replace(/\]/g, '').replace(/"/g, '');

  fs.writeFile(filePath, body, () => {
    PythonShell.run('dscore_parser.py', function (err, results) { });
    res.end();
  })

})

app.listen(3000, () => {
  console.log('Example app listening on port 3000!')
})