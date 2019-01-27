/*
 WiFi device code for collecting the data from Arduino Nano via serial and sending it to the system via UDP.
 Change the parameters 
 Author: Prabin Rath
*/
#include "WiFi.h"
#include "AsyncUDP.h"

const char * ssid = "*****";
const char * password = "*****";

AsyncUDP udp;

void setup()
{
    Serial.begin(115200);
    //Rx,Tx
    Serial1.begin(115200, SERIAL_8N1, 16, 17);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    if (WiFi.waitForConnectResult() != WL_CONNECTED)
    {
      //Serial.println("WiFi Failed");
      while(1)
      {
        delay(1000);
      }
    }
    else
    {
      //Serial.println(WiFi.localIP());
    }
    if(udp.connect(IPAddress(0,0,0,0), 44444)) 
    {
      //Serial.println("UDP connected");
    }
}

String s1="*",s2="*";

void loop()
{
    if(Serial1.available()>0)
    {
       s1="";
       char ch=Serial1.read();
       while(ch!='$')
       {
         ch=Serial1.read();
       }
       while(true)
       {
         int inp=Serial1.read();
         if(inp==-1)
          continue;
         ch=(char)inp;
         if(ch=='$')
           break;
         else
           s1+=ch;
       }
    }
    
    if(Serial.available()>0)
    {
       s2="";
       char ch=Serial.read();
       while(ch!='$')
       {
         ch=Serial.read();
       }
       while(true)
       {
         int inp=Serial.read();
         if(inp==-1)
          continue;
         ch=(char)inp;
         if(ch=='$')
           break;
         else
           s2+=ch;
       }
    }
    
    udp.broadcastTo((s1+"#"+s2).c_str(), 44444);
}
