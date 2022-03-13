/* ###################################################################
**     Filename    : main.c
**     Project     : K64F_UART_test
**     Processor   : MK64FN1M0VLL12
**     Version     : Driver 01.01
**     Compiler    : GNU C Compiler
**     Date/Time   : 2022-01-13, 12:09, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.01
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "clockMan1.h"
#include "pin_init.h"
#include "osa1.h"
#include "DbgCs1.h"
#if CPU_INIT_CONFIG
  #include "Init_Config.h"
#endif
/* User includes (#include below this line is not maintained by Processor Expert) */
#include "moistureLevel.h"
#include "Sensors.h"


/*lint -save  -e970 Disable MISRA rule (6.3) checking. */
int main(void)
/*lint -restore Enable MISRA rule (6.3) checking. */
{

  /* Write your local variable definition here */

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
	PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */
	unsigned int data2, LightCount, LightFlag;
	int temp, hum, lux, motion, motionCount;

  	SIM_SCGC5 |= SIM_SCGC5_PORTC_MASK; /* Enable Port C Clock Gate Control*/
  	SIM_SCGC5 |= SIM_SCGC5_PORTD_MASK; /* Enable Port D Clock Gate Control*/
  	SIM_SCGC5 |= SIM_SCGC5_PORTB_MASK; // Port B clock enable
  	SIM_SCGC5 |= SIM_SCGC5_PORTA_MASK; // Port A clock enable


   	SIM_SCGC6 |= SIM_SCGC6_ADC0_MASK; // 0x8000000u; Enable ADC0 Clock

  	//PORTC_GPCLR = 0x01BF0100; /* Configures Pins 0-5 7-8 on Port C to be GPIO */
  	PORTD_GPCLR = 0x000F0100; /* Configures Pins 0-3 on Port D to be GPIO */
   	PORTC_GPCLR = 0x000F0100; /* Configures Pins 0-5 7-8 on Port C to be GPIO */
   	PORTA_GPCLR = 0x00020100;            // enable port a pin 1
   	PORTB_GPCLR = 0x000C0100;            // enable port b pin 2:3




  	ADC0_CFG1 = 0x0C; // 16bits ADC; Bus Clock
   	ADC0_SC1A = 0x1F; // Disable the module, ADCH = 11111

   	GPIOC_PDDR = 0x0000000F; // Output mode for Port C
   	GPIOD_PDDR = 0x0000000F; // Output mode for Port D
   	GPIOA_PDDR = 0x00000000;            //set port A to input;
   	GPIOB_PDDR = 0x000000FF;            //set port b to output



   	char *choice;
   	char *UpdateText = 'get';

   	int updateMoisture1 = 40;
   	int updateMoisture2 = 40;

   	int *WaterSetting1;
   	int *WaterSetting2;
   	int *LightSetting;
   	int *FanSetting;

   	motion = 0;
  	for(;;) {
  		choice = 0;
  		//debug_printf("%s", "[K64f]\n");
  		//debug_printf("UARTStarts\n");
  		if(debug_scanf("%s", &choice)!=0);
  		//debug_printf("Reply: %s\n",&choice);



  		if(choice == 'get'){
  			if(debug_scanf("%i", &WaterSetting1)!=0);

  			if(debug_scanf("%i", &WaterSetting2)!=0);

  			if(debug_scanf("%i", &LightSetting)!=0);

  			if(debug_scanf("%i", &FanSetting)!=0);

  			updateMoisture1 = (int) WaterSetting1;
  			updateMoisture2 = (int) WaterSetting2;
  			moistureLevelRead(4, updateMoisture1, updateMoisture2);
  			temp = tempSensor();
  			hum = humSensor();
  			//debug_printf("RoomTemp_Status = RoomTempText\n");
  			//debug_printf("Humidity_Status = HumidText\n");
  			debug_printf("Light_Status = %i\n", LightSetting);
  			debug_printf("Fan_Status = %i\n", FanSetting);
  			debug_printf("WG1_Set = %i\n", WaterSetting1);
  			debug_printf("WG2_Set = %i\n", WaterSetting2);

  			//debug_printf("Motion = %i\n", motion);




  		}
  		motion = motionSensor(GPIOA_PDIR);

		lux = luxSensor();
		FanControl(temp, hum, FanSetting);
		//GPIOB_PSOR = 0x00000008;
		LightControl(lux,motion, LightSetting);

		if(motion || LightSetting){
			LightCount = 0;
			LightFlag = 0;
		}
		else if(motion == 0 && LightSetting != 1){
			LightCount++;
			LightFlag = 1;
		}

		if(LightFlag == 1 && LightSetting != 1){
			//GPIOB_PSOR = 0x00000008;	//turn on light
			if(LightCount > 50){
				LightFlag = 0;
				GPIOB_PCOR = 0x00000008;
			}
		}


  	}


  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.5 [05.21]
**     for the Freescale Kinetis series of microcontrollers.
**
** ###################################################################
*/
