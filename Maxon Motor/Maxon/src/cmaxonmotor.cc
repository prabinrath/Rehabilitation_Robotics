#include "cmaxonmotor.h"
#include <string.h>
#include <iostream>
#include <string.h>

using namespace std;

CMaxonMotor::CMaxonMotor()
{
    strcpy(PortName,"USB0");
    ErrorCode = 0x00;
    nodeID = 1;

}


CMaxonMotor::CMaxonMotor(char* portNamestr,unsigned int input_node_Id)
{
    PortName = portNamestr;
    ErrorCode = 0x00;
    nodeID = input_node_Id;
    //cout <<"aa " << endl;
}



void CMaxonMotor::closeDevice()
{
    DisableDevice();

    unsigned int ErrorCode = 0;

    //cout<<"Closing Device!"<<endl;

    if(keyHandle != 0)
        VCS_CloseDevice(keyHandle, &ErrorCode);

    VCS_CloseAllDevices(&ErrorCode);
}

void CMaxonMotor::EnableDevice()
{

    unsigned int ErrorCode = 0;
    int IsInFault = FALSE;

    if( VCS_GetFaultState(keyHandle, nodeID, &IsInFault, &ErrorCode) )
    {
        if( IsInFault && !VCS_ClearFault(keyHandle, nodeID, &ErrorCode) )
        {
            //cout << "Clear fault failed! , error code="<<ErrorCode<<endl;
            return;
        }

        int IsEnabled = FALSE;
        if( VCS_GetEnableState(keyHandle, nodeID, &IsEnabled, &ErrorCode) )
        {
            if( !IsEnabled && !VCS_SetEnableState(keyHandle, nodeID, &ErrorCode) )
            {
                cout << "Set enable state failed!, error code="<<ErrorCode<<endl;
            }
            else
            {
                //cout << "Enable succeeded!" << endl;
            }
        }
    }
    else
    {
        cout << "Get fault state failed!, error code, error code="<<ErrorCode<<endl;
    }

}

void CMaxonMotor::WaitForTarget(float time)
{
	unsigned int ErrorCode = 0;
	if( !VCS_WaitForTargetReached(keyHandle, nodeID, (int)(time*1000), &ErrorCode) )
	{
		cout<<"Time out"<<endl;
	}
}

void CMaxonMotor::DisableDevice()
{

    unsigned int ErrorCode = 0;
    int IsInFault = FALSE;

    if( VCS_GetFaultState(keyHandle, nodeID, &IsInFault, &ErrorCode) )
    {
        if( IsInFault && !VCS_ClearFault(keyHandle, nodeID, &ErrorCode) )
        {
            cout<<"Clear fault failed!, error code="<<ErrorCode<<endl;
            return;
        }

        int IsEnabled = FALSE;
        if( VCS_GetEnableState(keyHandle, nodeID, &IsEnabled, &ErrorCode) )
        {
            if( IsEnabled && !VCS_SetDisableState(keyHandle, nodeID, &ErrorCode) )
            {
                cout<<"Set disable state failed!, error code=" <<ErrorCode<<endl;
            }
            else
            {
                //cout<<"Set disable state succeeded!"<<endl;
            }
        }
    }
    else
    {
        //cout<<"Get fault state failed!, error code="<<ErrorCode<<endl;
    }
}


void CMaxonMotor::Move(long TargetPosition, int maxV, int maxA, int maxD)
{

    unsigned int errorCode = 0;

    if( VCS_ActivateProfilePositionMode(keyHandle, nodeID, &errorCode) )
    {
        int Absolute = TRUE; // FALSE;
        int Immediately = TRUE;
		
		if(VCS_SetPositionProfile(keyHandle, nodeID, maxV, maxA, maxD, &errorCode))
		{
		    if( !VCS_MoveToPosition(keyHandle, nodeID, TargetPosition, Absolute, Immediately, &errorCode) )
		    {
		        cout << "Move to position failed!, error code="<<errorCode<<endl;

		    }
        }
    }
    else
    {
        cout << "Activate profile position mode failed!" << endl;
    }
}


long CMaxonMotor::GetCurrentPosition()
{
	int CurrentPosition;
    unsigned int errorCode = 0;

    if( !VCS_GetPositionIs(keyHandle, nodeID, &CurrentPosition, &errorCode) ){
        cout << " error while getting current position , error code="<<errorCode<<endl;
    }
	return CurrentPosition;
}

void CMaxonMotor::Halt()
{
        unsigned int ErrorCode = 0;

        if( !VCS_HaltPositionMovement(keyHandle, nodeID, &ErrorCode) )
        {
                cout<<"Halt position movement failed!, error code="<<ErrorCode<<endl;
        }
}

void CMaxonMotor::activate_device()
{
    // Configuring EPOS for analog motor control
    char DeviceName[]="EPOS2";
    char ProtocolStackName[] = "MAXON SERIAL V2";
    char InterfaceName[] = "USB";
    unsigned int ErrorCode = 0x00;
    unsigned long timeout_ = 500;
    unsigned long baudrate_ = 1000000;

	cout<<PortName<<endl;
    keyHandle = VCS_OpenDevice(DeviceName,ProtocolStackName,InterfaceName,PortName,&ErrorCode);

    if( keyHandle == 0 )
    {
        cout<<"Open device failure, error code="<<ErrorCode<<endl;
    }
    else
    {
        //cout<<"Open device success!"<<endl;
    }


    if( !VCS_SetProtocolStackSettings(keyHandle, baudrate_, timeout_, &ErrorCode) )
    {
        cout<<"Set protocol stack settings failed!, error code="<<ErrorCode<<endl;
        closeDevice();
    }

    EnableDevice();

}


void CMaxonMotor::initializeDevice()
{
    closeDevice(); // To close if opend
    activate_device();
    /*
    unsigned int errorCode = 0;
    if(!VCS_SetMaxFollowingError(keyHandle, nodeID, 100, &errorCode))
    {
    	cout<<"Minute position error: "<<errorCode<<endl;
    }
    */
}
