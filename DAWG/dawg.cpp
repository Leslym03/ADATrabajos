#include <iostream> 
#include <vector>
#include <bits/stdc++.h> 
#include <algorithm>
using namespace std; 

class Estado;
class Transciones;
class DAWG;
class Lista;

class Estado{
private: 
    friend class Transciones;
    friend class DAWG;
    friend class Lista;

    int num; 
    int altura;
    bool fin;
    Estado *e_next;
    Estado *e_ant;
    Transciones *t_inicio;
    int sizeTrans;
public:
    Estado(){
        e_next=NULL;
        e_ant;
        t_inicio = NULL;
        sizeTrans = 0;
    }
}; 

class Transciones{
private: 
    friend class Estado;
    friend class DAWG;
    friend class Lista;

    Estado *e_actual;
    Estado *e_next;
    char letra;
    Transciones *t_next;
public: 

};

class DAWG{ 
private:
    vector<char> C;                //C es un alfabeto de cardenal finito
    Estado *e_head;                //Q es un conjunto de estados  
    Estado *e_tail;                //T es el subconjunto de estados terminales de Q
    int max_altura;

    int tam;
public: 
    DAWG(){
        e_head = NULL;
        e_tail = NULL;
        tam = 0;
    }

    ~DAWG(){
        Estado *aux1 = e_head;
        Estado *aux2;
        while(aux1){
            aux2 = aux1->e_next;
            delete aux1;
            aux1 = aux2;
        }
    }

    int sizeTransicion(int num){
        Estado *aux1 = buscar_est(num);
        return aux1->sizeTrans;
    }

    void insertar_est(int n_num) {
        Estado *node = new Estado;
        node->num = n_num;

        Estado *aux1;
        Estado *aux2;
        aux1 = e_head;

        while(aux1){
            aux2 = aux1;
            aux1 = aux1->e_next;
        }
        if(e_head == aux1){
            e_head = node; //q0 es el estado inicial
            node->e_next = NULL;
            node->e_ant = NULL;
        }
        else
            aux2->e_next= node;
        node->e_next=aux1;
        node->e_ant=aux2;
        e_tail = node;
        tam++;
        node->sizeTrans = 0;
    }

    int size(){
        return tam;
    }

    int alturaDawg(){
        return max_altura;
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
        Estado *aux1;
        Estado *aux2;

        aux1 = buscar_est(num);
        aux1->fin = true;
        
        //Enviar al final
        if(aux1->e_next != NULL){
            aux2 = aux1->e_next;
            aux2->e_ant = aux1->e_ant;
            aux1->e_ant->e_next = aux2;
            aux1->e_next = NULL;
            aux1->e_ant = e_tail;
            e_tail->e_next = aux1;
            e_tail = aux1;
        }
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
        int count=0;
        if(C.size() == 0)
            C.push_back(aris);
        for(int i=0; i<C.size(); i++){
            if(C[i] !=  aris)
                count++;
        }
        if(C.size() == count)
            C.push_back(aris);
        
        Transciones *trans = new Transciones;
        Estado *estado_trans = buscar_est(actual);
        trans->e_actual = estado_trans;
        trans->e_next = buscar_est(next);
        trans->letra = aris;
        int temp = estado_trans->sizeTrans;
        estado_trans->sizeTrans = ++temp;

        Transciones *aux1;
        Transciones *aux2;
        aux1 = estado_trans->t_inicio;
        while(aux1){
            aux2 = aux1;
            aux1 = aux1->t_next;
        }
        if(estado_trans->t_inicio == aux1){
            estado_trans->t_inicio = trans;
            trans->t_next = NULL;
        }
        else
            aux2->t_next = trans;
        trans->t_next = aux1;
    }

    void mostrar_trans(){
        Estado *aux1=e_head;
        while(aux1){
            Transciones *aux2 = aux1->t_inicio;
            cout << aux1->num <<": ";
            while(aux2){
                cout << aux2->e_next->num <<" ";
                aux2 = aux2->t_next;
            }
            cout<<endl;
            aux1=aux1->e_next;
        }
        cout<<endl;
    }

    void mostrar_alfabeto(){
        for(int i=0; i<C.size(); i++){
            cout<< C[i] << " ";
        }
        cout << endl;
    }

    int altura_est(Estado *est){
        int cont_altura = 0;
        int aux_max = 0;

        Transciones *t_aux1 = est->t_inicio;
        Estado *e_aux1 = est;

        if(est->t_inicio == NULL)
            return 0;

        return 1 +altura_est(est->t_inicio->e_next);
        
    }

    void alturas(){
        Estado *aux1=e_head;
        int temp=0;
        int temp_max=0;

        temp_max = altura_est(aux1);
        aux1->altura = temp_max;
        cout << temp_max << " ";
        aux1=aux1->e_next; 

        while(aux1){
            temp = altura_est(aux1);
            aux1->altura = temp;
            cout << temp << " ";
            aux1=aux1->e_next;

            temp_max = max(temp_max,temp);

            if(!aux1)
                break;
            
        }
        max_altura = temp_max;
    }

    void minimizacion(){
        Estado *aux1= e_head->e_next;
        Estado *aux2=aux1->e_next;
        Transciones * trans1;
        Transciones * trans2;
        int cont;
        
        for(int i=max_altura-1; i=0; i--){
            while (aux2->altura == i){
                if(aux1->sizeTrans == aux2->sizeTrans){
                    cont = 0;
                    trans1 = aux1->t_inicio;
                    trans2 = aux2->t_inicio;
                    for(int i=0; i<aux1->sizeTrans; i++){
                        if(trans1->letra == trans2->letra){
                            cont ++;
                        }
                        trans1 = trans1->t_next;
                        trans2 = trans2->t_next;
                    }
                    if(cont == aux1->sizeTrans){
                        aux2->e_ant = aux1->e_ant;
                        aux1->e_ant->e_next = aux2;
                        delete aux1;
                    }
                }
                aux1 = aux2;
                aux2 = aux2->e_next;
            }
            
                
        }
        
    }

}; 
  

int main(){
    DAWG a;

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
    a.insertar_trans(7,8,'c');

    
    a.e_finales(6);
    a.e_finales(8);

    a.mostrar_alfabeto();
    a.mostrar_est();

    //a.alturas();

    //cout << a.alturaDawg() << endl;

    //a.mostrar_trans();

    //cout << endl << a.sizeTransicion(1) << endl;
    a.minimizacion();
    a.mostrar_est();


    return 0;
}
