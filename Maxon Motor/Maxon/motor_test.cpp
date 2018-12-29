#include <stdio.h>
#include <iostream>
#include <string>
#include "cmaxonmotor.h"
#include <unistd.h>
#define RES 300000
using namespace std;

long mapData(float target)
{
	return (long)((target/360)*RES);
}

int main(int argc, char *argv[])
{
	char port[]="USB1";
    CMaxonMotor motor(port,1);
    motor.initializeDevice(); // initialize EPOS2
    long TargetPosition = mapData(0);
	
    motor.Move(TargetPosition,1000,50000,50000); // move to the target position
    motor.WaitForTarget(100);
    /*
    motor.Move(TargetPosition,6200,50000,50000); // move to the target position
    motor.WaitForTarget(5);
    motor.Move(TargetPosition,6200,50000,50000); // move to the target position
    motor.WaitForTarget(5);
    motor.Move(TargetPosition,6200,50000,50000); // move to the target position
    motor.WaitForTarget(5);
    motor.Move(TargetPosition,6200,50000,50000); // move to the target position
    motor.WaitForTarget(5);
    */
     // get the current position
    cout << "Current Position: " << motor.GetCurrentPosition() << endl;

    motor.closeDevice(); // close EPOS2

    return 0;
}
