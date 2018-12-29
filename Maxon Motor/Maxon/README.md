## Maxon Motor Control
Currently has been implmented for one motor gait cycle play
Use Cmake to build the code
* Find the EPOS2 shared libraries in the previous directory
* Copy them to the /usr/lib directory
* Copy the .rules file to the /etc/udev/rules.d folder
* If the motor is new, first configure it and auto-tune it in the EPOS studio
* After auto-tuning the green light of the EPOS motor driver flashes with an attached power supply
* Go to the build directory
* $ camke .
  $ make
* Run the code with the USB attached to the system
