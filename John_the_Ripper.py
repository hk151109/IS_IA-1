import hashlib
from itertools import product

def md5_hash(password):
    return hashlib.md5(password.strip().encode()).hexdigest()

def load_hash_file(filename):
    user_hashes = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')  
            if len(parts) >= 2:
                user_hashes[parts[0].strip()] = parts[1].strip()
    return user_hashes

def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def single_crack(user_hashes):
    print("Running Single Crack Mode...")

    def mangling_rules(word):
        return {word, word.upper(), word.lower(), word[::-1], word.capitalize()}
    
    found = False
    for username, actual_hash in user_hashes.items():
        candidates = mangling_rules(username)
        for candidate in candidates:
            if md5_hash(candidate) == actual_hash:
                print(f"[SUCCESS] Username: {username}, Password: {candidate}")
                found = True

    if not found:
        print("[FAILED] No match found.")

def wordlist_crack(user_hashes, wordlist):
    print("Running Wordlist Mode...")

    def case_variations(word):
        return {word, word.lower(), word.upper(), word.capitalize()}
    
    found = False
    for username, actual_hash in user_hashes.items():
        for word in wordlist:
            variations = case_variations(word)
            for variant in variations:
                if md5_hash(variant) == actual_hash:
                    print(f"[SUCCESS] Username: {username}, Password: {variant}")
                    found = True

    if not found:
        print("[FAILED] No match found.")

def generate_case_permutations(word):
    return {''.join(p) for p in product(*[(c.lower(), c.upper()) for c in word])}

def incremental_crack(user_hashes, wordlist):
    print("Running Incremental Mode (All Case Permutations)...")
    
    found = False
    for word in wordlist:
        case_variations = generate_case_permutations(word)  # Generate all mixed-case variations
        
        for case_variant in case_variations:
            hashed_variant = md5_hash(case_variant)

            for username, actual_hash in user_hashes.items():
                if hashed_variant == actual_hash:
                    print(f"[SUCCESS] Username: {username}, Password: {case_variant}")
                    found = True

    if not found:
        print("[FAILED] No match found.")

def main():
    hash_file = input("Enter the filename containing usernames and hashes: ")
    wordlist_file = input("Enter the filename containing the wordlist: ")
    
    user_hashes = load_hash_file(hash_file)
    wordlist = load_wordlist(wordlist_file)
    
    while True:
        print("\nSelect attack mode:")
        print("1. Single Crack Mode")
        print("2. Wordlist Mode")
        print("3. Incremental Mode")
        print("4. Exit")
        
        choice = input("Enter choice (1/2/3/4): ")
        
        attack_modes = {
            "1": single_crack,
            "2": wordlist_crack,
            "3": incremental_crack
        }
        
        if choice == "4":
            print("Exiting...")
            break
        elif choice in attack_modes:
            if choice == "1":
                attack_modes[choice](user_hashes)  # Call single_crack with one argument
            else:
                attack_modes[choice](user_hashes, wordlist)  # Call others with two arguments
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
