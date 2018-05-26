
var  nodemailer = require('nodemailer');
var  express = require('express');
var   LineByLineReader = require('line-by-line');
var  accountSid = 'AC2xxxx';
var  authToken = 'xxxxx';
var  client = require('twilio')(accountSid, authToken);







//***********read the Log file nagios **************



//************** Read the arguments passed to file *******************//















function sendEmail(args)
{



  // Generate test SMTP service account from ethereal.email
  // Only needed if you don't have a real mail account for testing
  nodemailer.createTestAccount((err, account) => {
      // create reusable transporter object using the default SMTP transport
      let transporter = nodemailer.createTransport({
          host: 'smtp.gmail.com',
          port: 587,
          secure: false, // true for 465, false for other ports
          auth: {
              user: 'yourmail.com', // generated ethereal user
              pass: 'password' // generated ethereal password
          }
      });

      // setup email data with unicode symbols
      let mailOptions = {
          from: '"nagios@notification👻" ahmed.bouhmid94@gmail.com', // sender address
          to: 'ahmed.bouhmid94@gmail.com', // list of receivers
          subject: 'Nagios notification ✔', // Subject line
          html: '<b>Alert </b>' + JSON.stringify(args),

  /*text : + 'Notification Type:'+ arg1
+ 'Service:' + 'Current Load'

+ 'Host :' + arg2
+ 'Address:' + arg3
+ 'State :'+ 'WARNING'
+ 'Date/Time:'+ 'Wed May 23 11:43:43 CEST 2018'*/

      };

      // send mail with defined transport object
      transporter.sendMail(mailOptions, (error, info) => {
          if (error) {
              return console.log(error);
          }
          console.log('Message sent: %s', info.messageId);
          // Preview only available when sending through an Ethereal account
          console.log('Preview URL: %s', nodemailer.getTestMessageUrl(info));

          // Message sent: <b658f8ca-6296-ccf4-8306-87d57a0b4321@example.com>
          // Preview URL: https://ethereal.email/message/WaQKMgKddxQDoou...
      });
  });





}





//*****************function to send sms ********************//
function sendSms(args)
{


console.log("args 0 " + args[1] + " " + args[2] + " " + args[3])
client.messages
  .create({
     body: JSON.stringify(args),
     from: '+14234010059',
     to: '+21620140428'
   })
  .then(message => console.log(message.sid))
  .done();

}



//*************send Sms *********************//
/*var spawn = require('child_process').spawn,
    ls    = spawn('ls', ['-lh', '/usr']);

ls.stdout.on('data', function (data) {
  console.log('stdout: ' + data.toString());
});

ls.stderr.on('data', function (data) {
  console.log('stderr: ' + data.toString());
});

ls.on('exit', function (code) {
  console.log('child process exited with code ' + code.toString());
});;*/


'use strict';

const args = require('minimist')(process.argv.slice(2));


console.log(args.i);

console.log("***************" + args);

const fs = require('fs');

fs.appendFile('./message.txt', args, function (err) {
  if (err) throw err;
  console.log('Saved!');
});

var argv = require('yargs').argv;
  sendEmail(argv )
  sendSms(argv)







const app = express()

app.get('/', (req, res) => res.send('Hello World!'))

app.get('/sms', (req, res) =>
{

sendSms("ok sms send")
res.send('Hello World!')}


)






/*lr.on('error', function (err) {
	// 'err' contains error object
  console.log("err in readin file")
});

lr.on('line', function (line) {
	// 'line' contains the current line without the trailing newline character.

    console.log("a new line has been added " + line)

    sendEmail(line)


//*********here we will check if it was CRITICAL error to send email and sms notiifcation


















});

lr.on('end', function () {
	// All lines are read, file is closed now.
  console.log("ended ended ")
});*/














app.listen(3000, () => console.log('Example app listening on port 3000!'))
