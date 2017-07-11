const express = require('express')
const bodyParser = require('body-parser')
const fs = require('fs')
const url = require('url')
const app = express()
const PythonShell = require('python-shell')
const firebase = require('firebase');

var config = {
  apiKey: "AIzaSyAidsUWUXmFBw9qoCmWFqgRTCzvOvpXPpE",
  authDomain: "implicit-association-test.firebaseapp.com",
  databaseURL: "https://implicit-association-test.firebaseio.com",
  projectId: "implicit-association-test",
  storageBucket: "",
  messagingSenderId: "299744556460"
};
firebase.initializeApp(config);

app.use(express.static(__dirname));

const urlencodedParser = bodyParser.urlencoded({ extended: false })

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html')
})

app.post('/save', urlencodedParser, (req, res) => {
  let body = JSON.stringify(req.body['message[]']);
  body = ',' + body;
  body = body.replace(/\\n/g, '\n').replace(/\[/g, '').replace(/\]/g, '').replace(/"/g, '');

  var database = firebase.database();

  let randomNumber = Math.floor(Math.random() * 1000000000);

  console.log(randomNumber);

  PythonShell.run('dscore_parser.py', function (err, results) {
    let dscore = results[1].slice(1, -1);

    console.log(dscore);

    database.ref('/' + randomNumber).set({
      dscore: dscore
    });
  });

  res.end();

})

app.listen(3000, () => {
  console.log('Example app listening on port 3000!')
})