var arDrone = require('ar-drone');
var client = arDrone.createClient();

client.stop();
client.land();
process.exit(0);
