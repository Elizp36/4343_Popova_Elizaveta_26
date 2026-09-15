from collections import deque

class Node:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.output_link = None
        self.patterns = []
        self.depth = 0

class AhoCorasick:
    def __init__(self):
        self.root = Node()
        self.root.output_link = None 
        self.patterns = []
        
    def add_pattern(self, pattern, pattern_num):
        node = self.root
        for char in pattern:
            if char not in node.children:
                new_node = Node()
                new_node.depth = node.depth + 1
                node.children[char] = new_node
            node = node.children[char]
        node.patterns.append(pattern_num)
    
    def build_automaton(self):
        queue = deque()
        
        for char, child in self.root.children.items():
            child.suffix_link = self.root
            child.output_link = None
            queue.append(child)
        
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                suffix_node = current.suffix_link
                while suffix_node != self.root and char not in suffix_node.children:
                    suffix_node = suffix_node.suffix_link
                
                if char in suffix_node.children:
                    child.suffix_link = suffix_node.children[char]
                else:
                    child.suffix_link = self.root
                
                if child.suffix_link.patterns:
                    child.output_link = child.suffix_link
                else:
                    child.output_link = child.suffix_link.output_link
                
                queue.append(child)
    
    def search(self, text):
        results = []
        node = self.root
        
        for i, char in enumerate(text):
            while node != self.root and char not in node.children:
                node = node.suffix_link
            
            if char in node.children:
                node = node.children[char]
            else:
                node = self.root
            
            temp = node
            while temp is not None and temp != self.root:
                for pattern_num in temp.patterns:
                    pattern_len = len(self.patterns[pattern_num - 1])
                    start_pos = i - pattern_len + 2  
                    results.append((start_pos, pattern_num))
                temp = temp.output_link
        
        results.sort()
        return results

text = input().strip()
n = int(input().strip())

ac = AhoCorasick()

for i in range(1, n + 1):
    pattern = input().strip()
    ac.patterns.append(pattern)
    ac.add_pattern(pattern, i)

ac.build_automaton()

results = ac.search(text)
for pos, pattern_num in results:
    print(pos, pattern_num)
