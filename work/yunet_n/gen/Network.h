
#ifndef __DEEPLOY_HEADER__
#define __DEEPLOY_HEADER__
#include "DeeployBasicMath.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
void RunNetwork(uint32_t core_id, uint32_t numThreads);
void InitNetwork(uint32_t core_id, uint32_t numThread);

extern float32_t *DeeployNetwork_input_0;
static const uint32_t DeeployNetwork_input_0_len = 307200;
extern float32_t *DeeployNetwork_output_0;
static const uint32_t DeeployNetwork_output_0_len = 1600;
extern float32_t *DeeployNetwork_output_1;
static const uint32_t DeeployNetwork_output_1_len = 400;
extern float32_t *DeeployNetwork_output_2;
static const uint32_t DeeployNetwork_output_2_len = 100;
extern float32_t *DeeployNetwork_output_3;
static const uint32_t DeeployNetwork_output_3_len = 1600;
extern float32_t *DeeployNetwork_output_4;
static const uint32_t DeeployNetwork_output_4_len = 400;
extern float32_t *DeeployNetwork_output_5;
static const uint32_t DeeployNetwork_output_5_len = 100;
extern float32_t *DeeployNetwork_output_6;
static const uint32_t DeeployNetwork_output_6_len = 6400;
extern float32_t *DeeployNetwork_output_7;
static const uint32_t DeeployNetwork_output_7_len = 1600;
extern float32_t *DeeployNetwork_output_8;
static const uint32_t DeeployNetwork_output_8_len = 400;
extern float32_t *DeeployNetwork_output_9;
static const uint32_t DeeployNetwork_output_9_len = 16000;
extern float32_t *DeeployNetwork_output_10;
static const uint32_t DeeployNetwork_output_10_len = 4000;
extern float32_t *DeeployNetwork_output_11;
static const uint32_t DeeployNetwork_output_11_len = 1000;
static const uint32_t DeeployNetwork_num_inputs = 1;
static const uint32_t DeeployNetwork_num_outputs = 12;
extern void *DeeployNetwork_inputs[1];
extern void *DeeployNetwork_outputs[12];
static const uint32_t DeeployNetwork_inputs_bytes[1] = {1228800};
static const uint32_t DeeployNetwork_outputs_bytes[12] = {6400, 1600, 400, 6400, 1600, 400, 25600, 6400, 1600, 64000, 16000, 4000};
#endif
