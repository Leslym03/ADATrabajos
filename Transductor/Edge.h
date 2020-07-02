#pragma once
#include <string>
using namespace std;

//Arista
template<class DataIn,class DataOut,class Tracker>
class Edge{
public:
    string sourceID;
    int destinationIndex;
    typedef bool(*Condition)(DataIn& input,Tracker& inputTracker);
    typedef void(*Action)(DataIn& input,DataOut& output,Tracker& inputTracker);
    Condition exp;
    Action act;
    
    Edge(string sourceID,int destinationIndex,Condition exp,Action act){
        this->sourceID = sourceID;
        this->destinationIndex = destinationIndex;
        this->exp = exp;
        this->act = act;
    }
    Edge(){
        sourceID = "";
        destinationIndex = -1;
    }
    void operator =(const Edge& rhs){
        this->sourceID = rhs.sourceID;
        this->destinationIndex = rhs.destinationIndex;
        this->exp = rhs.exp;
        this->act = rhs.act;
    }
    bool isNull(){
        return (sourceID == "") && (destinationIndex == -1);
    }
};
