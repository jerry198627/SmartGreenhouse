/*
 * Sensors.h
 *
 *  Created on: Feb 19, 2022
 *      Author: Terrance
 */

#ifndef SOURCES_SENSORS_H_
#define SOURCES_SENSORS_H_

int ADCreturn(){
	int data=0;

	SIM_SCGC6 |= SIM_SCGC6_ADC0_MASK; // 0x8000000u; Enable ADC0 Clock
	ADC0_CFG1 = 0x0C; // 16bits ADC; Bus Clock
	ADC0_SC1A = 0x1F; // Disable the module, ADCH = 11111
	ADC0_SC1A = 0x00; //Write to SC1A to start conversion from ADC_0
	while(ADC0_SC2 & ADC_SC2_ADACT_MASK); // Conversion in progress
	while(!(ADC0_SC1A & ADC_SC1_COCO_MASK)); // Until conversion complete
	return data = ADC0_RA;
}

int tempSensor(){

	float voltage, tempC, mean_value = 0;
	int whole,remainder, data;
	int iter = 100;

	GPIOD_PCOR = 0x000001BF;
	GPIOD_PSOR = 4;

	for(int i = 0; i<iter; i++){
		data = ADCreturn();
		voltage = (2.6*data)/65535;
		//tempC = (voltage * (400/11));
		//tempC = (voltage-0.31)/0.0137;
		tempC = (72.56*voltage) - 21.56;
		mean_value += tempC;
	}
	mean_value = mean_value/iter;

	whole = mean_value;
	remainder = mean_value * 100;
	remainder = remainder % 100;
	//debug_printf("Temp in C: %i\r\n", data);
	debug_printf("RoomTemp_Status = %i.%i\n", whole, remainder);
	return whole;	//value return for use in fan
}

int luxSensor(){
	float voltage, lux , mean_value = 0;
	int whole, remainder, data;
	int iter = 100;

	GPIOD_PCOR = 0x000001BF;
	GPIOD_PSOR = 5;

	for(int i = 0; i<iter;i++){
		data = ADCreturn();
		voltage = (3.6*data)/65535;
		/*resistance = (10000*(5.0-voltage))/voltage;
		lux = 500.0/(resistance/1000.0);*/
		lux = (128.43*voltage) + 12.31;
		mean_value += lux;
	}
	mean_value = mean_value/iter;
	if (mean_value <= 0.0){
		mean_value = 0.0;
	}
	whole = mean_value;
	remainder = mean_value * 100;
	remainder = remainder % 100;
	//debug_printf("Data = %i\r\n",data);
	//debug_printf("LightLux_data = %i.%i\r\n\n",whole,remainder);

	/*if (whole>=80){
		debug_printf("LightLux_Status = Bright\n");
	}
	else{
		debug_printf("LightLux_Status = Dark\n");
	}*/
	return whole;
}

int humSensor(){

	float voltage, hum, mean_value = 0;
	unsigned int whole;
	int remainder, data;
	int iter = 100;

	GPIOD_PCOR = 0x000001BF;
	GPIOD_PSOR = 6;

	for(int i = 0; i<iter;i++){
		data = ADCreturn();
		voltage = (3.2*data)/65535.0;
		hum = (36.47*voltage) - 27.64;
		mean_value += hum;
	}
	mean_value = mean_value/iter;

	if(mean_value >= 100.0){
		mean_value = 100.0;
	}
	else if(mean_value <= 0.0){
		mean_value = 0.0;
	}

	whole = mean_value;
	remainder = mean_value * 100;
	remainder = remainder % 100;
	//debug_printf("Data = %i\r\n", data);
	debug_printf("Humidity_Status = %i.%i%\n", whole, remainder);
	return whole;
}

int motionSensor(int motion){
	/*
	 * Motion sensor connected to PortA Pin1
	 */
	int motionCountY, motionCountN;
	motionCountY = 0;
	motionCountN = 0;
	for(int i = 0; i<50; i++){
		if(motion >= 18){
			motionCountY++;
		}else{
			motionCountN++;
		}

	}
	if (motionCountN > motionCountY){
		motion = 0;			//no motion
	}
	else{
		motion = 1;
	}
	return motion;
}


void FanControl(int temp, int hum, int FanSetting){
	if(FanSetting == 1){
		GPIOB_PSOR = 0x00000004;		// turn on fan from FanSetting
	}
	else if(FanSetting != 1){
		if(temp >= 40 || hum >= 60){
			GPIOB_PSOR = 0x00000004;	// turn on fan when temp >=20 or hum >= 60
		}
		else{
			GPIOB_PCOR = 0x00000004;	// turn off fan
		}
	}
}

void LightControl(int lux, int motion, int LightSetting){
	if(LightSetting == 1){
		GPIOB_PSOR = 0x00000008;		// turn on light from LightSetting
	}
	else{
		if(lux <= 70 && motion == 1){	// turn on light when dark and motion detected
			GPIOB_PSOR = 0x00000008;
		}
		/*
		else{
			GPIOB_PCOR = 0x00000008;	// turn off light
		}
		*/
	}
}





#endif /* SOURCES_SENSORS_H_ */
