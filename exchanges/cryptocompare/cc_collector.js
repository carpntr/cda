const config = require('./config');
const nats_client = require('./nats_conn').createNATSClient(config);

// Create socket connection
const socket_client = require('./ws_conn').createWSClient(config);

// Message callback
function on_message(message) {
    // console.log('WEBSOCKET DATA: ' + message)

    // Publish new data to crypto-compare topic
    nats_client.publish('crypto-compare', message)
}
socket_client.on('m', on_message);


// Determine what should be pulled.
function subscription_callback(message){
    console.log('Adding new ticker subscription: ' + message);

    // Probably need to do some validation here...
    var subscriptions = message.split(',').map(function(s) {
        return s.trim();
    });
    socket_client.emit('SubAdd', {subs:subscriptions} );
}
nats_client.subscribe('cc-subscriptions', subscription_callback);
