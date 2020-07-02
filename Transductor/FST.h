#pragma once
#include "Node.h"
#include <vector>

template  <class DataIn,class DataOut,class Tracker>
class FST{
private:
    Edge<DataIn,DataOut,Tracker> getValidEdge(Node<DataIn,DataOut,Tracker>& n){
        auto it = n.edges.begin();
        while (it != n.edges.end()) {
            if (it->sourceID == n.getID() && it->exp(input,inputTracker)) {
                return *it;
            }
            it++;
        }
        return Edge<DataIn,DataOut,Tracker>();
    }
public:
    vector<Node<DataIn,DataOut,Tracker>> nodes;
    Node<DataIn,DataOut,Tracker> currentNode;
    Node<DataIn,DataOut,Tracker> intialNode;
    DataIn input;
    DataOut output;
    Tracker inputTracker;
    
    FST(Node<DataIn,DataOut,Tracker> intialNode,vector<Node<DataIn,DataOut,Tracker>> nodes,DataIn input){
        this->intialNode = intialNode;
        this->nodes = nodes;
        this->input = input;
        currentNode = this->intialNode;
    }
    int transition(){
        Edge<DataIn,DataOut,Tracker> validEdge = getValidEdge(currentNode);
        if (validEdge.isNull()) {
            cout<<"FST está estancado\n";
            return -1;
        }
        validEdge.act(input,output,inputTracker);
        currentNode = nodes[validEdge.destinationIndex];
        return 0;
    }
    void simulate(unsigned int n){
        for(int i = 0; i < n; i++){
            cout<<i<<":"<<currentNode.getID()<<endl;
            int count = transition();
            if (count == -1) {
                return;
            }
        }
        
    }
    
};
