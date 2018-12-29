/*
Sample code for implementing fuzzy logic controller with 2 inputs
Design of the knowlwdge base uses some parse guidelines:
-1st and 2nd lines represent the linguistic variables for 2 inputs
-3rd line represent the linguistic variables of the output
-linguistic variables for input or output should be written in a single line with sapce. Name of two variables cannot be same
	Example: VN NR FR VFR represents 4 linguistic variables for input 1 in the sample knowledge base given
-4th and 5th lines represent the ranges of the linguistic variables for the 1st and 2nd input
-6th line represents the ranges of the linguistic variables for the output
-From 7th line we put the knowlwdge base for the fuzzy
-Dont put any additional spaces or new lines in the txt files. It will crash the parser
Author: Prabin Rath
*/
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
