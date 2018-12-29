#include <stdio.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include <fstream>
#include <vector>
#include "cmaxonmotor.h"
#define RES 300000
using namespace std;

long mapData(float target)
{
	return (long)((target/360)*RES);
}

int main(int argc, char *argv[])
{
	ifstream gait;
	gait.open("data_final_leftleg.txt");
	if(!gait.is_open())
	{
		cout<<"Couldnt open the file\n";
	}
	string line,parm; //required string variables
	vector<vector<float> > dataPoints;
	while(getline(gait,line) && gait.is_open()) //extract lines one by one
	{
		vector<float> temp;
		int i=0;
		while(line[i]!=',')
		{
			parm.push_back(line[i]);i++;
		}
		i++;
		temp.push_back(stof(parm));
		parm="";
		while(line[i]!=',')
		{
			parm.push_back(line[i]);i++;
		}
		temp.push_back(stof(parm));
		parm="";
		dataPoints.push_back(temp);
	}
	gait.close();
/*
	for(int i=0;i<dataPoints.size();i++)
	{
		for(int j=0;j<dataPoints[i].size();j++)
		{
			cout<<mapData(dataPoints[i][j])<<" ";
		}
		cout<<endl;
	}
*/
	char port[]="USB0";
    CMaxonMotor motor(port,1);
    motor.initializeDevice(); // initialize EPOS2

    for(int i=0;i<dataPoints.size();i++)
	{
		cout<<dataPoints[i][1]<<endl;
		//motor.Move(mapData(dataPoints[i][1]),10000,500000,500000); // move to the target position
		motor.Move(mapData(dataPoints[i][1]),6500,50000,50000);
    	motor.WaitForTarget(1);
    	//sleep(0.2);
	}
    motor.closeDevice(); // close EPOS2
    return 0;
}
