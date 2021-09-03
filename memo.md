# note, memo for learning how SlimeVR Tracker USP runs

Find it hard to understand how it runs...

## main.cpp

+ setup

+ + setupBNO080 sensor

+ loop

+ + clientUpdate

  + + receive packets from server

  + + view udpclient.cpp for detail

  + call sensor's motion loop

  + + updates sensor's data
    + view bno080sensor.cpp for detail
    
  + processBlinking, blinks the LEDs?
  
  + call sensors' sendData
  
  + + sends data

## bno080sensor.cpp

## doubt

how handshake and heartbeat is done

# consider how my implemention should run

+ init 5 udp clients for waist, left/right upper-leg/ankle
+ loop:
+ + detect body pose
  + calc rotations
  + send rotations

## doubt

how handshake and heartbeat is done
