var express = require('express');
var router = express.Router();
var WebSocket = require('ws');
const exec = require('child_process').exec;
var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'radee',
    password: 'radee',
    database: 'radee'
});

var wss = new WebSocket.Server({
    port: 8080
});

var dataHolder = [];
var state = 'standby';
var detail = {};
var projectName;

wss.on('connection', (ws) => {
    ws.send(JSON.stringify({
        event: 'state',
        state: state,
        detail: detail
    }));
    ws.send(JSON.stringify({
        event: 'reload',
        data: dataHolder
    }));
    ws.on('message', (message) => {
        var msg = JSON.parse(message);
        if (msg.event === 'start') {
            projectName = msg.name;
            // connection.connect(function (err) {
            //     if (err) {
            //         console.error('error connecting: ' + err.stack);
            //         return;
            //     }

                connection.query('CREATE TABLE radee.' + projectName + ' (datetime varchar(30), voltage int(10));', function (err, result) {
                    if (err) throw err;
                    // console.log("Table created");
                });

            //     connection.end();
            // });
            exec('python3 /home/pi/radee-2018/measurements/measurement.py ' + msg.name + ' ' + msg.time, (err) => {
                if (err) {
                    console.log(err);
                }
            });
            broadcast(JSON.stringify({
                event: 'started',
                name: msg.name,
                time: msg.time
            }));
            state = 'working';
            detail.name = msg.name;
            detail.time = msg.time;
        } else if (msg.event === 'reset') {
            dataHolder = [];
            detail = {};
            broadcast(JSON.stringify({
                event: 'reset'
            }));
            state = 'standby';
        }
    })
});

router.post('/', function (req, res, next) {
    // console.log(req.body);
    dataHolder.push(req.body);
    // broadcast(JSON.stringify([req.body]));
    broadcast(JSON.stringify({
        event: 'new',
        data: [req.body]
    }));
    res.status(200).send('Received data!');
});

router.get('/', (req, res, next) => {
    state = 'done';
    broadcast(JSON.stringify({
        event: 'finish'
    }));
    res.status(200).send('GOOD JOB!');
    // console.log(dataHolder);
    for (let m = 0; m < dataHolder.length; m++) {
        // console.log(`INSERT INTO radee.${projectName} (datetime, voltage) VALUES ("${dataHolder[m].datetime}", ${dataHolder[m].voltage});`);
        connection.query(`INSERT INTO radee.${projectName} (datetime, voltage) VALUES ("${dataHolder[m].datetime}", ${dataHolder[m].voltage});`);
    }
});

var broadcast = function (data) {
    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(data);
        }
    });
};

module.exports = router;
