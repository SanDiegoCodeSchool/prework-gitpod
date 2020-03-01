const http = require('http');
const fs = require("fs");
const { exec } = require("child_process");

/* 

BUILDS THE HTML FROM INDIVIDUAL FILES, ADDS TESTS

*/

var htmlInput = fs.readFileSync('/workspace/prework-gitpod/prework/commenting/index.html');
var cssInput = fs.readFileSync('/workspace/prework-gitpod/prework/commenting/styles.css');
var jsInput = fs.readFileSync('/workspace/prework-gitpod/prework/commenting/app.js');
var tests = fs.readFileSync('/workspace/prework-gitpod/prework/commenting/test.js');

const jquery = `<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>`;

const mochaScripts = `<script src="https://cdn.rawgit.com/jquery/jquery/2.1.4/dist/jquery.min.js"></script>
    <script src="https://cdn.rawgit.com/Automattic/expect.js/0.3.1/index.js"></script>
    <script src="https://cdn.rawgit.com/mochajs/mocha/2.2.5/mocha.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chai/4.1.2/chai.min.js"></script>
    <script src="https://oca-start-now.s3.amazonaws.com/libs/sinon-chai.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sinon.js/4.1.2/sinon.min.js"></script>
    <script>mocha.setup({ui:'bdd', ignoreLeaks: false});</script>`;

const mochaCSS = '<link href="https://cdn.rawgit.com/mochajs/mocha/2.2.5/mocha.css" rel="stylesheet" />';
const beforeTests = '\nvar expect = chai.expect;\n';

function mochaHelper() {
    return `
      var passedTestCount = 0;
      var failures = [];
      var complete = false;
  
      mocha.checkLeaks();
      mocha.globals(['jQuery']);
  
      mocha.run()
        .on('suite end', function(test) {
          // suite is finished
        })
        .on('end', function(err) {
          // all tests are finished
          complete = (failures.length === 0) ? true : false;
          let results = {
            passed: passedTestCount,
            failed: failures.length,
            failureDetails: failures,
            complete
          }
          console.log({ type: '$$IFRAME$$', results }, "*");
        })
        .on('pass', function(test) {
          // single test passed
          passedTestCount++;
        })
        .on('fail', function(test, err) {
          // single test failed
          failures.push({ title: test.title, errors: err.toString() });
        })`;
  }

const blobString = `
<!DOCTYPE HTML><html>
    <head>
        ${mochaCSS}
        <style>${cssInput}</style>
    </head>
    <body>
        </div>
        ${htmlInput}
        <div id="mocha">
            ${jquery}
            ${mochaScripts}
            <script>
                ${jsInput}
                ${beforeTests}
                ${tests}
                ${mochaHelper()}
            </script>
    </body>
</html>
`
/* 

WRITES THE FILE AND SERVES ON PORT 3000

*/
fs.writeFile('/workspace/prework-gitpod/live.html', blobString, (err) => {
    if (err) throw err;
})

http.createServer(function (req, res) {
  fs.readFile('/workspace/prework-gitpod/live.html', function (err,data) {
    if (err) {
      res.writeHead(404);
      return;
    } else {
      res.writeHead(200);
      res.end(data);
      return;
    }
  });
}).listen(3000);

exec('gp preview $(gp url 3000) && gp url 3000', (error, stdout, stderr) => {
    console.log('\n============== LOADING TEST ENVIRONMENT ==============\n')
    console.log('View the results of your test: ' + stdout);
    console.log(` - To re-run the tests, exit the current test session and re-run the test command.\n\n - You can exit the test session anytime by pressing Control + 'c'`)
})