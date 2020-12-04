const Gpio = require('pigpio').Gpio;
 
const motor = new Gpio(13, {mode: Gpio.OUTPUT});
 
let pulseWidth = 1000;
let increment = 100;
 
setInterval(() => {
  motor.servoWrite(pulseWidth);
    console.log(pulseWidth);
  pulseWidth += increment;
  if (pulseWidth >= 2000) {
    increment = -100;
  } else if (pulseWidth <= 500) {
    increment = 100;
  }
}, 1000);