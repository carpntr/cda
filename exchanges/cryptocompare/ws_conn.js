const io = require('socket.io-client');

function createWSClient(config) {
    const socket = io.connect(config.WS_HOST);
    socket.on('connect', function(){
        console.log('socket connected')
    });
    return socket;
}

module.exports = {
    createWSClient: createWSClient
};

// socket.on('connect', function () {
//     console.log("socket connected");
// });
//
// socket.on("m", function(message){
//     console.log(message)
// });
//
// var subscriptions = [
//     '5~CCCAGG~BTC~USD'
// ];
//
// socket.emit('SubAdd', {subs:subscriptions} );


