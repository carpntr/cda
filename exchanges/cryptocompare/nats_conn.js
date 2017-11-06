const NATS = require('nats');

function createNATSClient(config) {
    return NATS.connect(config.NATS_HOST);
}

module.exports = {
    createNATSClient: createNATSClient
};
