#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string> 
#include <iostream>
#include <fstream>
using namespace std;

#define LEN(x)  (sizeof(x) / sizeof((x)[0]))

typedef struct State State;
typedef struct Path Path;

struct State {
	char *in; 		//Nombre nodo
	char *out;		//Salida transductor
	State *next;	
	Path *start;
};

struct Path {
	char *value;	//Nombre arista
	State *current;
	State *next_state;
	Path *next;
};

State *head;

State *new_state(const char *in, const char *out) {
	State *node = (State *)malloc(sizeof(State));
	node->in = (char*)malloc(sizeof(in));
	strcpy(node->in, in);
	node->out = (char*)malloc(sizeof(out));
	strcpy(node->out, out);
	node->next = NULL;
	node->start = NULL;
	return node;
}

Path *new_path(const char *val, State *current, State *next) {
	Path *node = (Path *)malloc(sizeof(Path));
	node->value = (char*)malloc(sizeof(val));
	strcpy(node->value, val);
	node->next = NULL;
	node->next_state = next;
	node->current = current;
	return node;
}

State *add_state(State *node) {
	if (head == NULL)
		head = node;
	else{
		State *start = head;
		while ((*start).next != NULL){
			start = (*start).next;
		}
		(*start).next = node;
	}
	return node;
}

State *add_state(const char in[20],const char out[20], bool finish) {
	State *node = new_state(in, out);
	return add_state(node);
}

Path *add_path(Path *node) {
	if (node->current->start == NULL)
		node->current->start = node;
	else {
		Path *start = node->current->start;
		while ((*start).next != NULL){
			start = (*start).next;
		}
		(*start).next = node;
	}
	return node;
}

Path *add_path(const char *val, State *current, State *next) {
	Path *node = new_path(val, current, next);
	return add_path(node);
}

void init_graf() {
	head = NULL;
	/**
	ifstream f("graf.txt");
	int n_state, n_path;
	f>> n_state;
	State states[n_state];
	for(int i=0; i<n_state; i++){
		const char *in;
		const char *out;
		f >> const_cast<char*>(in);
		f >> const_cast<char*>(out);
		states[i] = *new_state(in, out);
	}
	f>> n_path;
	Path paths[n_path];
	for(int i=0; i<n_path; i++){
		int s1, s2;
		const char *val;
		f>> const_cast<char*>(val);
		f>> s1;
		f>> s2;
		paths[i] = *new_path(val, &states[s1], &states[s2]);
	}
	**/

	//Estados
	State states[4];
	states[0] = *new_state("s0", "0");
	states[1] = *new_state("s1", "0");
	states[2] = *new_state("s2", "1");
	states[3] = *new_state("s3", "0");
	//Caminos
	Path paths[8];
	paths[0] = *new_path("a", &states[0], &states[3]);
	paths[1] = *new_path("b", &states[0], &states[2]);
	paths[2] = *new_path("a", &states[1], &states[1]);
	paths[3] = *new_path("b", &states[1], &states[0]);
	paths[4] = *new_path("a", &states[2], &states[2]);
	paths[5] = *new_path("b", &states[2], &states[3]);
	paths[6] = *new_path("a", &states[3], &states[0]);
	paths[7] = *new_path("b", &states[3], &states[1]);

	for (int i = 0; i < LEN(states); i++){
		add_state(&states[i]);
	}
	for (int i = 0; i < LEN(paths); i++){
		add_path(&paths[i]);
	}
}

int main() {
	init_graf();
	char const *inputs[7];
	//Entrada
	inputs[0] = "b";
	inputs[1] = "a";
	inputs[2] = "b";
	inputs[3] = "a";
	inputs[4] = "b";
	inputs[5] = "b";
	inputs[6] = "b";

	//Puntero para retornar salida
	const char *outputs[LEN(inputs) + 1];
	bool error = false;
	//Recorre grafo para comprobar si la entrada reconoce la salida
	State *iterator = head;
	for (int i = 0; i < LEN(inputs); i++){
		outputs[i] = iterator->out;
		Path *start_path = iterator->start;
		while (start_path != NULL){
			if (strcmp(start_path->value, inputs[i]) == 0){
				break;
			}
			start_path = start_path->next;
		}
		//Por si encuentra no encuentra la arista
		if (start_path == NULL) {
			outputs[i] = "Error - Sin caminos";
			error = true;
			break;
		}
		else
			iterator = start_path->next_state;
	}
	if(error == false)
		outputs[LEN(inputs)] = iterator->out;

	printf("Entrada:\t");
	for (int i = 0; i < LEN(inputs); i++){
		printf("%s\t", inputs[i]);
	}
	printf("\nSalida:\t\t");
	for (int i = 0; i < LEN(outputs)-1; i++){
		printf("%s\t", outputs[i]);
	}
	cout << endl;
	return 0;
}