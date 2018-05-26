var LineByLineReader = require('line-by-line'),
    lr = new LineByLineReader('/usr/local/nagios/var/nagios.log');

lr.on('error', function (err) {
	// 'err' contains error object
  console.log("err in readin file")
});

lr.on('line', function (line) {
	// 'line' contains the current line without the trailing newline character.

    console.log("a new line has been added " + line)
});

lr.on('end', function () {
	// All lines are read, file is closed now.
  console.log("ended ended ")
});




/*const accountSid = 'AC2e8a1103c805c4312d65acb5b2992aa3';
const authToken = '517bb667955097d0be15d9f1b04e4a73';
const client = require('twilio')(accountSid, authToken);

client.messages
  .create({
     body: 'This is the ship that made the Kessel Run in fourteen parsecs?',
     from: '+14234010059',
     to: '+21620140428'
   })
  .then(message => console.log(message.sid))
  .done();*/
