#include<fuzzy_controller.h>

/////////////////////////////////////////////////////////////////////////Fuzzy/////////////////////////////////////////////////////////////
vector<LingVar> Fuzzy::getParticipatingVector(float inp,int type)
{
	vector<LingVar> out;
	if(type==1)
	{
		for(int i=0;i<input1.size();i++)
		{
			if(inp>=input1[i].minl && inp<=input1[i].maxl)
				{out.push_back(input1[i]);}
		}
		if(inp<input1[0].minl)
			out.push_back(input1[0]);
		if(inp>input1[input1.size()-1].maxl)
			out.push_back(input1[input1.size()-1]);
	}
	else if(type==2)
	{
		for(int i=0;i<input2.size();i++)
		{
			if(inp>=input2[i].minl && inp<=input2[i].maxl)
				{out.push_back(input2[i]);}
		}
		if(inp<input2[0].minl)
			out.push_back(input2[0]);
		if(inp>input2[input2.size()-1].maxl)
			out.push_back(input2[input2.size()-1]);
	}
	return out;
}
/////////////////////////////////////////////////////////////////////////Mamdani Model//////////////////////////////////////////////////////
FuzzyMamdani::FuzzyMamdani(string path)
{
	map<string,int> track;
	fstream kb;
	kb.open(path); //open the knowledge base in read
	if(kb.is_open())
	{
		cout<<"File opened\n";
	}
	else
	{
		cout<<"Couldnt open the file\n";
		return;
	}
	string line,parm; //required string variables
	int state=1;
	while(getline(kb,line)) //extract lines one by one
	{
		parm="";
		if(state==1 || state==2 || state==3)
		{
			int i=0,k=0;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					LingVar temp;
					temp.name=parm;
					if(state==1)
						{input1.push_back(temp);mp1[temp.name]=k++;}
					else if(state==2)
						{input2.push_back(temp);mp2[temp.name]=k++;}
					else if(state==3)
						{output.push_back(temp);track[temp.name]=k++;}
					parm="";
					i++;
				}
				parm.push_back(line[i]);i++;
			}
		}
		else if(state==4 || state==5 || state==6)
		{
			int i=0,k=0;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					string m="";
					int j=0;
					while(j<parm.size())
					{
						if(parm[j]=='_')
						{
							if(state==4)
								input1[k].minl=stof(m.c_str());
							else if(state==5)
								input2[k].minl=stof(m.c_str());
							else if(state==6)
								output[k].minl=stof(m.c_str());
							
							m="";
							j++;
						}
						m.push_back(parm[j]);
						j++;
					}
					if(state==4)
						{input1[k].maxl=stof(m.c_str());input1[k].mid=(input1[k].maxl+input1[k].minl)/2;}
					else if(state==5)
						{input2[k].maxl=stof(m.c_str());input2[k].mid=(input2[k].maxl+input2[k].minl)/2;}
					else if(state==6)
						{output[k].maxl=stof(m.c_str());output[k].mid=(output[k].maxl+output[k].minl)/2;}
					parm="";
					i++;k++;
				}
				parm.push_back(line[i]);i++;
			}
			if(state==6)
			{
				input1[0].isTerminal=-1;
				input1[input1.size()-1].isTerminal=1;
				input2[0].isTerminal=-1;
				input2[input2.size()-1].isTerminal=1;
				output[0].isTerminal=-1;
				output[output.size()-1].isTerminal=1;
			}
		}
		else if(state>=7)
		{
			int i=0;
			vector<LingVar> v;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					v.push_back(output[track[parm]]);
					parm="";
					i++;
				}
				parm.push_back(line[i]);i++;
			}
			knowledge.push_back(v);
		}
		state++;
	}
	kb.close();
}

float FuzzyMamdani::getFuzzyVal(float inp1,float inp2)
{
	vector<LingVar> part1,part2;
	part1=getParticipatingVector(inp1,1);
	part2=getParticipatingVector(inp2,2);
	
	float area_middle=0,area=0;
	for(int i=0;i<part1.size();i++)
	{
		for(int j=0;j<part2.size();j++)
		{
			//cout<<part1[i].name<<"\t"<<part2[j].name<<"\t|\t"<<knowledge[mp1[part1[i].name]][mp2[part2[j].name]].name<<"\t"<<knowledge[mp1[part1[i].name]][mp2[part2[j].name]].isTerminal<<endl;
			float mn=min(part1[i].getMembership(inp1),part2[j].getMembership(inp2));
			float ar=knowledge[mp1[part1[i].name]][mp2[part2[j].name]].getArea(mn);
			area_middle+=ar*knowledge[mp1[part1[i].name]][mp2[part2[j].name]].calcMid(mn);
			area+=ar;
		}
	}

	return area_middle/area;
}

///////////////////////////////////////////////////////////////////////////////Takagi and Sugeno Model//////////////////////////////////////

FuzzyTakagiSugeno::FuzzyTakagiSugeno(string path)
{
	fstream kb;
	kb.open(path); //open the knowledge base in read
	if(kb.is_open())
	{
		cout<<"File opened\n";
	}
	else
	{
		cout<<"Couldnt open the file\n";
		return;
	}
	string line,parm; //required string variables
	int state=1;
	while(getline(kb,line)) //extract lines one by one
	{
		parm="";
		if(state==1 || state==2)
		{
			int i=0;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					LingVar temp;
					temp.name=parm;
					if(state==1)
						{input1.push_back(temp);}
					else if(state==2)
						{input2.push_back(temp);}
					parm="";
					i++;
				}
				parm.push_back(line[i]);i++;
			}
		}
		else if(state==3 || state==4)
		{
			int i=0,k=0;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					string m="";
					int j=0;
					while(j<parm.size())
					{
						if(parm[j]=='_')
						{
							if(state==3)
								input1[k].minl=stof(m.c_str());
							else if(state==4)
								input2[k].minl=stof(m.c_str());
							m="";
							j++;
						}
						m.push_back(parm[j]);
						j++;
					}
					if(state==3)
						{input1[k].maxl=stof(m.c_str());input1[k].mid=(input1[k].maxl+input1[k].minl)/2;}
					else if(state==4)
						{input2[k].maxl=stof(m.c_str());input2[k].mid=(input2[k].maxl+input2[k].minl)/2;}
					parm="";
					i++;k++;
				}
				parm.push_back(line[i]);i++;
			}
			if(state==4)
			{
				input1[0].isTerminal=-1;
				input1[input1.size()-1].isTerminal=1;
				input2[0].isTerminal=-1;
				input2[input2.size()-1].isTerminal=1;
			}
		}
		else if(state==5 || state==6)
		{
			int i=0,k=0;
			while(i<=line.size())
			{
				if(line[i]==' ' || i==line.size())
				{
					if(state==5)
						{input1[k].coeff=stof(parm);}
					else if(state==6)
						{input2[k].coeff=stof(parm);}
					parm="";
					i++;k++;
				}
				parm.push_back(line[i]);i++;
			}
		}
		state++;
	}
	kb.close();
}

float FuzzyTakagiSugeno::getFuzzyVal(float inp1,float inp2)
{
	vector<LingVar> part1,part2;
	part1=getParticipatingVector(inp1,1);
	part2=getParticipatingVector(inp2,2);
		
	float weight=0,y_weight=0;
	for(int i=0;i<part1.size();i++)
	{
		for(int j=0;j<part2.size();j++)
		{
			float w=part1[i].getMembership(inp1)*part2[j].getMembership(inp2);
			float y=part1[i].coeff*inp1+part2[j].coeff*inp2;
			//cout<<w<<"\t"<<y<<endl;
			y_weight+=w*y;
			weight+=w;
		}
	}
	return y_weight/weight;
}
