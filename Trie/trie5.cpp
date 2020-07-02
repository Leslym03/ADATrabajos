#include <iostream>
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
private:
    TrieNode* root;
public:
    /** Initialize your data structure here. */

    Trie() {
        root = new TrieNode();
    }
    ~Trie(){
        delete(root);
    }
    
    /** Inserts a word into the trie. */
    void insert(string word) {
        TrieNode* node = root;
        int index;
        for(int i = 0; i<word.length(); i++){
            index = word[i]  - 'a';
            if(node->children[index] == NULL)
                node->children[index] = new TrieNode();
            node = node->children[index];
        }
        node->isLast = true;
    }
    
    /** Returns if the word is in the trie. */
    bool search(string word) {
        TrieNode* node = root;
        int index;
        for(int i = 0; i<word.length(); i++){
            index = word[i]  - 'a';
            node = node->children[index];
            if(node == NULL)
                return false;
        }
        return node->isLast;
    }
    
    /** Returns if there is any word in the trie that starts with the given prefix. */
    bool startsWith(string prefix) {
        TrieNode* node = root;
        int index;
        for(int i = 0; i<prefix.length(); i++){
            index = prefix[i]  - 'a';
            node = node->children[index];
            if(node == NULL)
                return false;
        }    
        return true;
    }
};


int main(){
	Trie* head = new Trie();
	head->insert("hello");
	cout << head->search("hello") << " ";
	return 0;
}
