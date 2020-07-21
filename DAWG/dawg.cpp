#include<iostream> 
#include<vector>
#include <bits/stdc++.h> 
using namespace std; 

class Estado;
class Transciones;
class DAWG;

class Estado{
private: 
    friend class Transciones;
    friend class DAWG;
    int num; 
    int altura;
    bool fin;
    Estado *e_next;
    Transciones *t_inicio;

public:

}; 

class Transciones{
private: 
    friend class Estado;
    friend class DAWG;

    Estado *e_actual;
    Estado *e_next;
    char letra;
    Transciones *t_next;

public: 

};


class DAWG{ 
private:
    vector<char> C;                //C es un alfabeto de cardenal finito
    //vector<Nodo> conjNodos;      
    //vector<Nodo> conNFinales;    //T es el subconjunto de estados terminales de Q
    Estado *e_head;                //Q es un conjunto de estados    
    Transciones *t_head;
    
public: 
    DAWG(){
        e_head = NULL;
        t_head = NULL;
    }

    ~DAWG(){
        Estado *aux1 = e_head;
        Estado *aux2;
        Transciones *aux3 = t_head;
        Transciones *aux4;
        while(aux1){
            aux2 = aux1->e_next;
            delete aux1;
            aux1 = aux2;
            aux4 = aux3->t_next;
            delete aux3;
            aux3 = aux4;
        }
    }

    void alfabetoC(vector<char> alf){
        for(int i; i<alf.size(); i++){
            C.push_back(alf[i]);
        }
    }

    void insertar_est(int n_num) {
        Estado *node = new Estado;
        node->num = n_num;

        Estado *aux1;
        Estado *aux2;
        aux1 = e_head;

        while(aux1 && aux2->num < n_num){
            aux2 = aux1;
            aux1 = aux1->e_next;
        }
        if(e_head == aux1)
            e_head = node; //q0 es el estado inicial
        else
            aux2->e_next= node;
        node->e_next=aux1;
    }

    Estado* buscar_est(int num){
        Estado *aux1=e_head;
        while(aux1->num!=num){
            aux1=aux1->e_next;
            if(!aux1)
                break;
        }
        return aux1;
    }

    void e_finales(int num){
        Estado *aux1=e_head;
        while(aux1->num !=num ){
            aux1=aux1->e_next;
            if(!aux1)
                break;
        }
        aux1->fin = true;
    }

    void mostrar_est(){
        Estado *aux1=e_head;
        while(aux1){
            cout<<aux1->num<<" ";
            aux1=aux1->e_next;
        }
        cout<<endl;
    }

    //F es una función de Q x C en Q que define las transiciones (arcos) del autómata
    void insertar_trans(int actual, int next, char aris){
        Transciones *trans = new Transciones;
        trans->e_actual = buscar_est(actual);
        trans->e_next = buscar_est(next);
        trans->letra = aris;

        Transciones *aux1;
        Transciones *aux2;
        aux1 = t_head;
        while(aux1){
            aux2 = aux1;
            aux1 = aux1->t_next;
        }
        if(t_head == aux1)
            t_head = trans;
        else
            aux2->t_next = trans;
        trans->t_next = aux1;
    }

    void mostrar_trans(){
        Transciones *aux1=t_head;
        while(aux1){
            cout << aux1->e_actual->num << " " << aux1->letra << " " << aux1->e_next->num << endl;
            aux1=aux1->t_next;
        }
        cout<<endl;
    }

    void altura(){

    }

}; 
  

int main(){
    DAWG a;
    /**
    vector<char> alf;
    alf.push_back('a');
    alf.push_back('b');
    alf.push_back('c');
    a.alfabetoC(alf);
    **/
    a.insertar_est(1);
    a.insertar_est(2);
    a.insertar_est(3);
    a.insertar_est(4);
    a.insertar_est(5);
    a.insertar_est(6);
    a.insertar_est(7);
    a.insertar_est(8);
    a.mostrar_est();

    
    a.insertar_trans(1,2,'a');
    a.insertar_trans(1,3,'b');
    a.insertar_trans(1,4,'c');

    a.insertar_trans(2,5,'a');
    a.insertar_trans(2,6,'b');
    a.insertar_trans(3,5,'a');
    a.insertar_trans(3,6,'b');
    a.insertar_trans(4,7,'a');
    a.insertar_trans(4,8,'c');

    a.insertar_trans(5,8,'a');
    a.insertar_trans(6,8,'b');
    
    a.mostrar_trans();
    return 0;
}
