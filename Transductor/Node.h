#pragma once
#include <string>
#include <list>
#include "Edge.h"
#include <iostream>
using namespace std;

template<class DataIn,class DataOut,class Tracker>
class Node{
private:
    string id;
    string name;
public:
    static unsigned int count;
    list<Edge<DataIn,DataOut,Tracker>> edges;
    typedef bool(*Condition)(DataIn& data,Tracker& inputTracker);
    typedef void(*Action)(DataIn& input,DataOut& output,Tracker& inputTracker);
    Node(){
        count++;
        id = "N" + to_string(count);
        name = "";
    }
    
    ~Node(){
        count--;
    }
    string getID(){
        return id;
    }
    string getName(){
        return name;
    }
    void setName(string name){
        this->name = name;
    }
    bool operator ==(const Node& rhs){
        return this->id == rhs.id;
    }
    void operator =(const Node<DataIn,DataOut,Tracker>&rhs){
        this->id = rhs.id;
        this->edges = rhs.edges;
    }
    void pushEdge(int destinationIndex,Condition exp,Action act){
        edges.push_back(Edge<DataIn,DataOut,Tracker>(this->id,destinationIndex,exp,act));
    }
    friend ostream& operator<<(ostream& os,Node node){
        os<<node.id;
        return os;
    }
};
template<class DataIn,class DataOut,class Tracker>
unsigned int Node<DataIn,DataOut,Tracker>::count = 0;
