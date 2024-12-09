def build_suffix_array(text):
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    # Sort the suffixes lexicographically
    suffixes.sort()
    # Extract and return the indices
    suffix_array = [suffix[1] for suffix in suffixes]
    return suffix_array

if __name__ == "__main__":
    text = "banana$"
    suffix_array = build_suffix_array(text)
    print("Suffix Array:", suffix_array)
