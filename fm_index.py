import bisect
from typing import List, Tuple

class FMIndex:
    def __init__(self, text: str):
        # Ensure the text ends with a unique termination character ($ is commonly used)
        if text[-1] != '$':
            text += '$'
        
        print("\n=== FM-INDEX INITIALIZATION ===")
        print(f"Original Text: {text}")
        
        # Generate all rotations of the text
        rotations = sorted(text[i:] + text[:i] for i in range(len(text)))
        
        print("\n1. ROTATIONS (BWT Matrix):")
        for i, rotation in enumerate(rotations):
            print(f"{i}: {rotation}")
        
        # Store the last column of the BWT matrix
        self.last_column = ''.join(rotation[-1] for rotation in rotations)
        print(f"\n2. Last Column (BWT): {self.last_column}")
        
        # Compute first column (sorted version of last column)
        self.first_column = ''.join(sorted(self.last_column))
        print(f"3. First Column: {self.first_column}")
        
        # Precompute character counts and cumulative counts
        self.char_count = {}
        self.cumulative_count = {}
        
        # Count occurrences of each character
        for char in self.first_column:
            if char not in self.char_count:
                self.char_count[char] = 0
            self.char_count[char] += 1
        
        print("\n4. CHARACTER COUNTS:")
        for char, count in sorted(self.char_count.items()):
            print(f"'{char}': {count}")
        
        # Compute cumulative counts
        total = 0
        for char in sorted(self.char_count.keys()):
            self.cumulative_count[char] = total
            total += self.char_count[char]
        
        print("\n5. CUMULATIVE COUNTS:")
        for char, cumulative in sorted(self.cumulative_count.items()):
            print(f"'{char}': {cumulative}")
        
        # Precompute occurrence table
        self.occurrence_table = self._build_occurrence_table()
        
        print("\n6. OCCURRENCE TABLE:")
        for i, counts in enumerate(self.occurrence_table):
            print(f"Position {i}: {dict(counts)}")
        
        print("\n=== END OF FM-INDEX INITIALIZATION ===\n")
    
    def _build_occurrence_table(self) -> List[dict]:
        occ_table = [{}]
        current_counts = {}
        
        for char in self.last_column:
            new_counts = current_counts.copy()
            if char not in new_counts:
                new_counts[char] = 0
            new_counts[char] += 1
            occ_table.append(new_counts)
            current_counts = new_counts
        
        return occ_table
    
    def count_occurrences(self, char: str, up_to: int) -> int:
        return self.occurrence_table[up_to].get(char, 0)
    
    def find(self, pattern: str) -> List[int]:
        print(f"\nSearching for pattern: '{pattern}'")
        
        # Start from the last character of the pattern
        if not pattern:
            return []
        
        top = 0
        bottom = len(self.last_column) - 1
        
        # Work backwards through the pattern
        for char in reversed(pattern):
            # Find the range of rows in the last column containing the character
            top = self.cumulative_count.get(char, 0) + \
                  self.count_occurrences(char, top)
            bottom = self.cumulative_count.get(char, 0) + \
                     self.count_occurrences(char, bottom + 1) - 1
            
            print(f"Processing '{char}': top = {top}, bottom = {bottom}")
            
            # If no matches found, return empty list
            if top > bottom:
                print("No matches found.")
                return []
        
        # Return all matching indices
        matches = list(range(top, bottom + 1))
        print(f"Found {len(matches)} match(es) at FM-index positions: {matches}")
        return matches
    
    def locate(self, pattern: str) -> List[int]:
        match_indices = self.find(pattern)
        
        # Convert FM-index positions to original text positions
        original_positions = [self._get_original_index(idx) for idx in match_indices]
        
        print(f"Original text positions: {original_positions}")
        return original_positions
    
    def _get_original_index(self, fm_index_pos: int) -> int:
        current_pos = fm_index_pos
        offset = 0
        
        while offset < len(self.last_column):
            current_pos = self.cumulative_count.get(self.last_column[current_pos], 0) + \
                          self.count_occurrences(self.last_column[current_pos], current_pos)
            offset += 1
        
        return current_pos

def main():
    text = "banana$"
    fm_index = FMIndex(text)
    
    patterns = ["ana", "na", "an"]
    for pattern in patterns:
        print("\n--- Pattern Search ---")
        fm_index.locate(pattern)

if __name__ == "__main__":
    main()