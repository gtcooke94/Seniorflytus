var df = require('dateformat')
  , autonomy = require('../')
  , mission  = autonomy.createMission()
  , arDrone = require('ar-drone')
  , arDroneConstants = require('ar-drone/lib/constants')
  ;

function navdata_option_mask(c) {
  return 1 << c;
}

// From the SDK.
var navdata_options = (
    navdata_option_mask(arDroneConstants.options.DEMO)
  | navdata_option_mask(arDroneConstants.options.VISION_DETECT)
  | navdata_option_mask(arDroneConstants.options.MAGNETO)
  | navdata_option_mask(arDroneConstants.options.WIFI)
);

var exiting = false;
process.on('SIGINT', function() {
    if (exiting) {
        process.exit(0);
    } else {
        console.log('Got SIGINT. Landing, press Control-C again to force exit.');
        exiting = true;
        mission.control().disable();
        mission.client().land(function() {
            process.exit(0);
        });
    }
});

// Connect and configure the drone
mission.client().config('general:navdata_demo', true);
mission.client().config('general:navdata_options', navdata_options);
mission.client().config('video:video_channel', 1);
mission.client().config('detect:detect_type', 12);

mission.log("mission-" + df(new Date(), "yyyy-mm-dd_hh-MM-ss") + ".txt");


function moveForward(distance) {
  mission.backward(distance)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("moveForward");
        process.exit(0);
    }
  });
}

function moveBackward(distance) {
  mission.forward(distance)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("We are done!");
        process.exit(0);
    }
  });
}

function moveLeft(distance) {
  mission.right(distance)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("We are done!");
        process.exit(0);
    }
  });
}


function moveRight(distance) {
  mission.left(distance)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("We are done!");
        process.exit(0);
    }
  });
}

function moveCW(angle) {
  mission.cw(angle)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("We are done!");
        process.exit(0);
    }
  });
}

function moveCCW(angle) {
  mission.ccw(angle)
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("We are done!");
        process.exit(0);
    }
  });
}

function takeoff() {
  mission.takeoff()
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("takeoff");
        process.exit(0);
    }
  });
}

function land() {
  mission.land()
  mission.run(function (err, result) {
    if (err) {
        console.trace("Oops, something bad happened: %s", err.message);
        mission.client().stop();
        mission.client().land();
    } else {
        console.log("land");
        process.exit(0);
    }
  });
}


takeoff();
moveForward(1);
land();