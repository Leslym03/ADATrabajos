#include <iostream>
#include <fstream>
#define MAX 100
using namespace std;
class TrieNode{
        private:
            TrieNode* children[26];
            bool isLast;
        public:
            TrieNode(){
                for(int i =0; i<26; i++)
                    this->children[i] = NULL;
                this->isLast = false;
            }
            
        friend class Trie;
};

class Trie {
	public:
		TrieNode* root;
		Trie() {
			root = new TrieNode();
		}
		~Trie(){
			delete(root);
		}
		void insert(string word){
			TrieNode* node = root;
			int index;
			for(int i = 0; i<word.length(); i++){
				index = word[i]  - 'a';
				if(node->children[index] == NULL){
					node->children[index] = new TrieNode();
				}
				node = node->children[index];
			}
			node->isLast = true;	
		}
		
		bool search(string word){
			TrieNode* node = root;
			int index;
			for(int i = 0; i<word.length(); i++){
				index = word[i]  - 'a';
				node = node->children[index];
				if(node == NULL){
					return false;
				}
			}
			return node->isLast;			
		}
		bool isLastNode(TrieNode* root){
			return root->isLast!= false;
		}
		void display(TrieNode* root,char *str,int level){
			
			if (isLastNode(root)){
				str[level] = '\0';
				cout << str << endl; 
			}
			for (int i = 0; i <26; i++){
				if (root->children[i]){
					str[level] = i + 'a';
					display(root->children[i],str, level + 1);
				}
			}
		}

};


int main(){
	Trie* head = new Trie();
    char *cad=NULL;
    char *palabras =new char[MAX];
    cad=new char[50];
	ifstream f( "teste.txt" );
	while( !f.eof() ) {
		f.getline(cad,50);
		string c(cad);
		head->insert(c);
    }
    
	f.close();
	cout << head->search("abasedly") << " "<<endl;
	int level=0;
	//head->display(head->root,palabras,level);
	
	delete []cad;
	delete []palabras;
	return 0;
}
