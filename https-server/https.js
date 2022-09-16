
var app =  require('./server.js')
 
require("greenlock-express")
    .init({
        packageRoot: __dirname,
        configDir: "./greenlock.d",
        server: 'https://acme-v02.api.letsencrypt.org/directory',
 
        // contact for security and critical bug notices
        maintainerEmail: 'tejaswi@asu.edu',
 
        // whether or not to run at cloudscale
        cluster: false
    })
    // Serves on 80 and 443
    // Get's SSL certificates magically!
    .serve(app);