#include "MPU9250.h"

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);
int status;

const double alpha = 0.5;

void setup() 
{
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

  // start communication with IMU 
  status = IMU.begin();
  if (status < 0) 
  {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
}

double accelX = 0;
double accelY = 0;
double accelZ = 0;

void loop() 
{
  // read the sensor
  IMU.readSensor();
  // display the data
  double Xg = IMU.getAccelX_mss();
  double Yg = IMU.getAccelY_mss();
  double Zg = IMU.getAccelZ_mss();

  accelX = Xg * alpha + (accelX * (1.0 - alpha));
  accelY = Yg * alpha + (accelY * (1.0 - alpha));
  accelZ = Zg * alpha + (accelZ * (1.0 - alpha));
  
  //double pitch = atan2 (accelY ,( sqrt ((accelX * accelX) + (accelZ * accelZ))));
  double roll = atan2(-accelX ,( sqrt((accelY * accelY) + (accelZ * accelZ))));
   
  roll = roll*57.3;
  //pitch = pitch*57.3;
   
  Serial.print("$"+String(roll)+"$");
  delay(10);
}
