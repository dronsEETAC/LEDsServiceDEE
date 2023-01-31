# LEDs service  

## Introduction

The LEDs service is an on-board module that controls the LEDs and the servo installed in the drone platform, as required by the rest of modules in the Drone Engineering Ecosystem.   
Dashboard or mobile applications will requiere the LEDs service to light certain LED with a given RGB color of to move the servo to drop and object.

## Installations
In order to run and contribute you must install Python 3.7. We recommend PyCharm as IDE for development.    
Contributions must follow the contribution protocol that you will find in the main repo of the Drone Engineering Ecosystem.
[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)


## Operation modes
Althoug it may not have much sense, the LEDs service can be run in simulation mode. In this case the service just print in console the actions that would do in poduction mode. This can be useful for debug purposes. Clone the repo in your computer and install de requirements. Be also sure that you have running the internal broker at "localhost:1884". To run the service you must edit the run/debug configuration in PyCharm in order to pass the required arguments to the script. At least two parameters are required: connection_mode (global or local) and operation_mode (simulation or production). In case of global communication mode, a third parameter is requiered indicating the external broker to be used. In case the external broker requieres credentials, two additional parameters must be includes (username and password). The figure shows and example where the external broker does not requires credentials.   
![autopilotServiceConfiguration](https://user-images.githubusercontent.com/100842082/212955034-2a9fdd8d-e654-405e-951d-605479ba9928.png)  
   
The run the LEDs service in production mode you will need the boot.py script that you will find in the main repo of the Drone Engineering Ecosystem. Follow the instruction that you will find in that repo.   
[![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE)

## Commands
In order to send a command to the LEDs service, a module must publish a message in the external (or internal) broker. The topic of the message must be in the form:
```
"XXX/LEDsService/YYY"
```
where XXX is the name of the module requiring the service and YYY is the name of the service that is required. Oviously, some of the commands include data that must be includes in the payload of the message to be published. 

The table bellow indicates all the commands that are accepted by the LEDs service in the current version.   

Command | Description | Payload 
--- | --- | --- 
*startLEDsSequence* | start a clyclic sequence: red, green, yellow | No 
*stopLEDsSequence* | stops the sequence | No 
*LEDsSequenceForNSeconds* | runs the cyclic sequience during a certain number of seconds | the number of seconds as string
*red* | put in red the first led for 5 seconds | No 
*green* | put in green the second led for 5 seconds | No 
*blue* | put in lue the third led for 5 seconds | No
*drop* | move the servo to drop the object | No
*reset* | move the servo to its initial position | No
*bluei* | fix the first led to blue | No 
*redi* | fix the first led to red | No
*yellowi* | fix the first led to yellow | No 
*greeni* | fix the first led to green | No
*pinki* | fix the first led to pink | No 
*whitei* | fix the first led to white | No
*blacki* | fix the first led to black | No
*clear* | clear the first led | No 



