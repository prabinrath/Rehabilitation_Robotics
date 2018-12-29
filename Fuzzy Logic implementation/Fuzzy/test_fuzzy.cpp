#include<iostream>
#include<fuzzy_controller.h>

int main()
{
	/*
	FuzzyMamdani delKp("./KB/knowledge_baseM.txt"),delKi("./KB/knowledge_baseM.txt"),delKd("./KB/knowledge_baseM.txt");
	for(float i=0.2;i<=2.1;i+=0.01)
		cout<<delKp.getFuzzyVal(i,30)<<" "<<delKi.getFuzzyVal(i,30)<<" "<<delKd.getFuzzyVal(i,30)<<endl;
	*/
	FuzzyMamdani f1("./KB/knowledge_baseM.txt");
	FuzzyTakagiSugeno f2("./KB/knowledge_baseTS.txt");
	for(float i=0.2;i<=2.1;i+=0.01)
		cout<<f1.getFuzzyVal(i,30)<<"\t\t\t\t"<<f2.getFuzzyVal(i,30)<<endl;
}
