var homeDir = require('path').join(require('os').homedir());
var app =  require('./server.js')
require('greenlock-express').init({
  packageRoot: __dirname,
  version: 'draft-11'
, server: 'https://acme-v02.api.letsencrypt.org/directory'
//, server: 'https://acme-staging-v02.api.letsencrypt.org/directory'  // staging
, maintainerEmail: 'tejaswi@asu.edu'                                     // CHANGE THIS
, agreeTos: true
, approveDomains: [ 'mlserve.tejaswigowda.com', 'www.mlserve.tejaswigowda.com' ]              // CHANGE THIS
, store: require('greenlock-store-fs')
, configDir: homeDir

}).serve(app);

//, app: require('express')().use('/', function (req, res) {
//    res.setHeader('Content-Type', 'text/html; charset=utf-8')
//    res.end('Hello, World!\n\n💚 🔒.js');
//  })
//, communityMember: true