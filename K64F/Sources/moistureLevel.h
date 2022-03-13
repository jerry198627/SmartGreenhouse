/*
 * moistureLevel.h
 *
 *  Created on: Feb 8, 2022
 *      Author: Kenytc
 */

#ifndef SOURCES_MOISTURELEVEL_H_
#define SOURCES_MOISTURELEVEL_H_





#endif /* SOURCES_MOISTURELEVEL_H_ */



int soilMoistureLevel [] = {0, 0, 0, 0};

void moistureLevelCheck(int maximumMoisture1, int maximumMoisture2)//Use this function to decide whether to turn on the pump
{
	int averageMoisture1 = (soilMoistureLevel[0] + soilMoistureLevel[1])/2;
	int averageMoisture2 = (soilMoistureLevel[2] + soilMoistureLevel[3])/2;
	if (averageMoisture2 >= maximumMoisture2) //turn off pump if moisture level is high enough
		{GPIOC_PCOR = 0x0C; /* Turn off Pump*/}
	else if (!(averageMoisture2 >= maximumMoisture2))
		{GPIOC_PSOR = 0x0C; /* Turn on Pump*/}

	if (averageMoisture1 >= maximumMoisture1) //turn off pump if moisture level is high enough
		{GPIOC_PCOR = 0x08; /* Turn off Pump*/}
	else if (!(averageMoisture1 >= maximumMoisture1))
		{GPIOC_PSOR = 0x08; /* Turn on Pump*/}
}
void moistureLevel(int numSensor, int updateMoisture1, int updateMoisture2) // Use ADC module to read the value from the sensor
{								  // After that, print the sensor value
    unsigned int moistureWhole = 0;
	unsigned int moistureRemainder = 0;
	unsigned int finalWhole = 0;
	unsigned int finalRemainder = 0;// sensor value

    for (int i = 0; i < 100; i++){
    	unsigned int outputValue;
		/*-------------------------The following block is for ADC-------------------*/
		ADC0_SC1A = 0x1F; // Disable the module, ADCH = 11111
		ADC0_SC1A = 0x00; //Write to SC1A to start conversion from ADC_0
		while(ADC0_SC2 & ADC_SC2_ADACT_MASK); // Conversion in progress
		while(!(ADC0_SC1A & ADC_SC1_COCO_MASK)); // Until conversion complete
		outputValue = ADC0_RA;
		/*-------------------------End of ADC block---------------------------------*/

		/*-------------------------Conversion block---------------------------------*/
		unsigned int DryValue, WetValue;
		float conversion, conversion1, conversion2, conversion3, conversion4;
		unsigned int whole, remainder;
		unsigned int percentage = 100;
		DryValue = 60000; WetValue = 31500;
		conversion1 = (DryValue - outputValue);
		conversion2 =	(DryValue - WetValue);
		conversion3 = conversion1/conversion2;
		conversion4 = conversion3 * percentage;
		conversion = conversion4 * 0.35;

		whole = (int) conversion;
		remainder = (conversion*100);
		remainder = remainder % 100;
		/*--------------------------End of Conversion block-------------------------*/

		if (whole <= 100){
			moistureWhole = whole + moistureWhole;
			moistureRemainder = remainder + moistureRemainder;
		}
		else {
			moistureWhole = soilMoistureLevel[numSensor] + moistureWhole;
			moistureRemainder = remainder + moistureRemainder;
		}
    }
    finalRemainder = moistureRemainder / 100;
    finalWhole = moistureWhole /100;
	soilMoistureLevel[numSensor] = finalWhole;
	moistureLevelCheck(updateMoisture1, updateMoisture2);
	debug_printf("Moisture_Status%i = %u.%u\n", numSensor, finalWhole, finalRemainder); //print the value with sensor #
//	debug_printf("Moisture_Status%i = %u.%u\n", numSensor, whole, remainder); //print the value with sensor #
}

void moistureLevelRead(int totalSensor, int updateMoisture1, int updateMoisture2) // Use the function moistureLevelRead() to read multiple sensor values
{                                       // the values will be printed sequentially
	int i = 1;
	uint32_t GPIO [8] = {0, 1, 2, 3, 4, 5, 6, 7, 8};
	for (i = 0; i <= (totalSensor - 1); i++){
		GPIOD_PCOR = 0x000001BF;
		GPIOD_PSOR = GPIO[i];
//		OSA_TimeDelay(2000); //wait for 5 seconds for more stable values
		//debug_printf(" Input %u ", GPIO[i]);
		moistureLevel (i, updateMoisture1, updateMoisture2);
	}
}
