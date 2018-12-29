#include <stdio.h>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
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
    return 0;
}
