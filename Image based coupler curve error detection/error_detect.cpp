#include "opencv2/opencv.hpp"
#include <iostream>
#include <string>
#include <algorithm>
#include <thread>
#include <fstream>
#include <sstream>
using namespace cv;
using namespace std;

Mat imgS=imread("./util/simul.jpg"),imgO=imread("./util/Scan3.png"),modified;
Mat org,sim,comp;
bool flag=false;
int sim_thresh=125,org_thresh=125;
vector<Point2f> sim_transform,org_transform;

Mat rotateImage(Mat src,int angle)
{
	Point2f pc(src.cols/2, src.rows/2);
	Mat r = getRotationMatrix2D(pc, angle, 1.0),dst;
	warpAffine(src, dst, r, src.size());
	return dst;
}

Mat cropImage(Mat src,int x,int y,int width,int height)
{
	if(x<src.cols && y<src.rows && (x+width)<=src.cols && (y+height)<=src.rows)
	{
		Rect roi;
		roi.x=x;roi.y=y;roi.width=width;roi.height=height;
		src=src(roi);
	}
	else
	{
		cout<<"Out of Bound Cropping\n";
	}
	return src;
}

void getTransform()
{
	org=modified.clone();
	sim=imgS.clone();
	resize(org,org,sim.size());
	cvtColor(sim,sim,CV_RGB2GRAY);
	cvtColor(org,org,CV_RGB2GRAY);
	threshold(sim,sim, sim_thresh, 255, CV_THRESH_BINARY_INV | CV_THRESH_OTSU);
	threshold(org,org, org_thresh, 255, CV_THRESH_BINARY_INV | CV_THRESH_OTSU);
	//int morph_size = 1;
    //Mat element = getStructuringElement( MORPH_RECT, Size( 2*morph_size + 1, 2*morph_size+1 ), Point( morph_size, morph_size ) );
    //morphologyEx( org, org, MORPH_OPEN, element, Point(-1,-1), 1 );
    
    sim_transform.clear();org_transform.clear();
    for(int i=0;i<sim.cols;i++)
    {
    	Point2f crdS(0,i),crdO(0,i);
    	int Scount=0,Ocount=0;
    	for(int j=0;j<sim.rows;j++)
    	{
    		if(org.at<uchar>(j,i) == 255)
    		{
    			crdO.x+=j;Ocount++;
    		}
    		if(sim.at<uchar>(j,i) == 255)
    		{
    			crdS.x+=j;Scount++;
    		}	
    	}
    	if(Ocount!=0)
    	{
    		crdO.x=(int)crdO.x/Ocount;
    		org_transform.push_back(crdO);
    	}
    	if(Scount!=0)
    	{
    		crdS.x=(int)crdS.x/Scount;
    		sim_transform.push_back(crdS);
    	}
    }
    
 	comp=Mat::zeros(sim.size(),CV_8UC3);
 	for(int i=0;i<sim_transform.size();i++)
    {
    	//cout<<sim_transform[i].x<<"\t"<<sim_transform[i].y<<endl;
    	circle( comp, sim_transform[i], 1, Scalar( 0, 0, 255 ), -1, 8 );
    }
    for(int i=0;i<org_transform.size();i++)
    {
    	//cout<<org_transform[i].x<<"\t"<<org_transform[i].y<<endl;
    	circle( comp, org_transform[i], 1, Scalar( 255, 0, 0 ), -1, 8 );
    }
}

void userHandle()
{
	string inp;
	while(true)
	{
		cin>>inp;
		if(inp=="th")
		{
			getTransform();
			flag=true;
		}
		else if(inp=="save")
		{
			bool bSuccess = imwrite("./util/saved/comp_curve.jpg", comp); 
		 	if ( !bSuccess )
			{
		     cout << "ERROR : Failed to save the image" << endl;
			}
			else
			{
				cout<<"Saved successfully"<<endl;
			}
		}
		else if(inp=="data")
		{
			ofstream file("./data_files/hipjointExperimentalX.txt");
			for(int i=0;i<org_transform.size();i++)
			{
				ostringstream ss;
				ss<<org_transform[i].x<<"\n";
    			file<<ss.str();
			}
			file.close();
			file.open("./data_files/hipjointExperimentalY.txt");
			for(int i=0;i<org_transform.size();i++)
			{
				ostringstream ss;
				ss<<org_transform[i].y<<"\n";
    			file<<ss.str();
			}
			file.close();
			file.open("./data_files/hipjointSimulatedX.txt");
			for(int i=0;i<sim_transform.size();i++)
			{
				ostringstream ss;
				ss<<sim_transform[i].x<<"\n";
    			file<<ss.str();
			}
			file.close();
			file.open("./data_files/hipjointSimulatedY.txt");
			for(int i=0;i<sim_transform.size();i++)
			{
				ostringstream ss;
				ss<<sim_transform[i].y<<"\n";
    			file<<ss.str();
			}
			file.close();
			cout<<"Saved all data"<<endl;
		}
	}
}

int main()
{
	resize(imgO,imgO,imgS.size());

	thread input(userHandle);
	
	namedWindow("Control", CV_WINDOW_NORMAL); 
	int angle = 180;
	int xMin=51,xWidth=351,yMin=25,yHeight=248;
 	createTrackbar("Angle", "Control", &angle, 360);
 	createTrackbar("X crop Min", "Control", &xMin, imgO.cols);
 	createTrackbar("X crop Width", "Control", &xWidth, imgO.cols);
 	createTrackbar("Y crop Min", "Control", &yMin, imgO.rows);
 	createTrackbar("Y crop Height", "Control", &yHeight, imgO.rows);
 	createTrackbar("Simulated img threshold", "Control", &sim_thresh, 255);
 	createTrackbar("Original img threshold", "Control", &org_thresh, 255);

 	while(true)
 	{
 		modified=rotateImage(imgO,angle);
 		modified=cropImage(modified,xMin,yMin,xWidth,yHeight);
 		if(flag==true)
 		{
 			imshow("Simulated Threshed",sim);
			imshow("Original Threshed",org);
			imshow("Transform Curves",comp);
			flag=false;
 		}
 		imshow("Simulated",imgS);
		imshow("Original",modified);
		cvWaitKey(10);
 	}
 	
 	input.join();
	return 0;
}
