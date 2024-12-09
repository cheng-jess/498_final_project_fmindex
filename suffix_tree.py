class SuffixTreeNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.children = {}
        self.suffix_link = None
        self.index = -1

class SuffixTree:
    def __init__(self, text):
        self.text = text + '$'
        self.root = SuffixTreeNode(-1, -1)  # Root node has no valid substring
        self.build_tree()

    def build_tree(self):
        n = len(self.text)
        for i in range(n):
            self._add_suffix(i)

    def _add_suffix(self, start_index):
        current_node = self.root
        j = start_index
        
        while j < len(self.text):
            current_char = self.text[j]
            
            # If no child exists for current character
            if current_char not in current_node.children:
                # Create new leaf node
                new_leaf = SuffixTreeNode(j, len(self.text) - 1)
                new_leaf.index = start_index
                current_node.children[current_char] = new_leaf
                break
            
            # Child exists, traverse or split edge
            child_node = current_node.children[current_char]
            edge_length = child_node.end - child_node.start + 1
            
            # Compare characters along the edge
            k = child_node.start
            while k <= child_node.end and j < len(self.text) and self.text[k] == self.text[j]:
                k += 1
                j += 1
            
            # If we've fully traversed the edge
            if k > child_node.end:
                current_node = child_node
                continue
            
            # Split the edge
            split_node = SuffixTreeNode(child_node.start, k - 1)
            current_node.children[current_char] = split_node
            
            # Adjust original child node
            child_node.start = k
            split_node.children[self.text[k]] = child_node
            
            # Add new leaf for the remaining suffix
            new_leaf = SuffixTreeNode(j, len(self.text) - 1)
            new_leaf.index = start_index
            split_node.children[self.text[j]] = new_leaf
            
            break

    def search(self, pattern):
        current_node = self.root
        i = 0
        
        while i < len(pattern):
            current_char = pattern[i]
            
            # No child for current character
            if current_char not in current_node.children:
                return False
            
            # Get the matching child node
            child = current_node.children[current_char]
            
            # Match characters on this edge
            edge_chars = self.text[child.start:child.end+1]
            pattern_segment = pattern[i:i+len(edge_chars)]
            
            if edge_chars != pattern_segment:
                return False
            
            # Update indices
            i += len(edge_chars)
            
            # Move to next node if pattern is fully matched
            if i >= len(pattern):
                return True
            
            current_node = child
        
        return True

    def get_suffixes(self):
        suffixes = []
        
        def dfs(node):
            # Leaf nodes store the suffix
            if node.index != -1:
                suffixes.append(self.text[node.index:])
            
            # Traverse children
            for child in node.children.values():
                dfs(child)
        
        dfs(self.root)
        return sorted(set(suffixes))

    def print_tree(self):
        def print_node(node, depth=0):
            indent = "  " * depth  # Indentation to represent tree depth
            if node == self.root:
                print(f"{indent}Root")
            else:
                edge_label = self.text[node.start:node.end+1]
                # Only show $ at the leaf level (end of string)
                if edge_label != '$':  # Don't print '$' unless it's at the leaf
                    print(f"{indent}Edge: '{edge_label}' [{node.start}, {node.end}]")
                else:
                    print(f"{indent}Edge: '$' [{node.start}, {node.end}]")
            
            # Traverse children and print recursively
            for child in node.children.values():
                print_node(child, depth + 1)
        
        print_node(self.root)

if __name__ == "__main__":
    text = "banana"
    st = SuffixTree(text)
    
    print("Suffixes:")
    for suffix in st.get_suffixes():
        print(suffix)
    
    print("\nSearch examples:")
    print("'ana' in tree:", st.search("ana"))
    print("'ban' in tree:", st.search("ban"))
    print("'xyz' in tree:", st.search("xyz"))
    
    print("\nTree Structure:")
    st.print_tree()
