#include<iostream>
#include<vector>
#include<fstream>
#include<string>
#include<map>
using namespace std;

struct LingVar
{
	string name;
	float maxl,minl,mid;
	float coeff;
	int isTerminal;
	LingVar():isTerminal(0){}
	
	float calcMid(float h)
	{
		float midV;
		if(isTerminal==0)
		{
			midV=(maxl+minl)/2;
		}
		else if(isTerminal==1)
		{
			float B=maxl-minl;
			midV=(h*(minl+2*B*h/3)+(1-h)*((1+h)*B+2*minl))/(2-h);
		}
		else
		{
			
			float B=maxl-minl;
			midV=(h*((-maxl)+2*B*h/3)+(1-h)*((1+h)*B+2*(-maxl)))/(2-h);
			midV*=-1;
		}
		return midV;
	}
	
	float getMembership(float x)
	{
		//cout<<name<<"\t"<<isTerminal<<endl;
		if(isTerminal==-1)
		{
			return (maxl-x)/(maxl-minl);
		}
		else if(isTerminal==1)
		{
			return (x-minl)/(maxl-minl);
		}
		else
		{
			return max(min((x-minl)/(mid-minl),(maxl-x)/(maxl-mid)),(float)0);
		}
	}
	
	float getArea(float ht)
	{
		return 0.5*(maxl-minl)*ht*(2-ht);
	}
};

class Fuzzy
{
	public:
		vector<LingVar> input1,input2;
		map<string,int> mp1,mp2;
		vector<LingVar> getParticipatingVector(float,int);
};

class FuzzyMamdani:private Fuzzy
{
	private:
		vector<LingVar> output;
		vector<vector<LingVar>> knowledge;
	public:
		FuzzyMamdani(string);
		float getFuzzyVal(float,float);		
};

class FuzzyTakagiSugeno:private Fuzzy
{
	public:
		FuzzyTakagiSugeno(string);
		float getFuzzyVal(float,float);		
};
