

scoring = 'TFIDF'
other = 'BM25'

def exploration_mode():
    print("## Exploration mode ##\n Please provide a search query:")
    query = input('> ')
    ui_loop()

def evaluation_mode():
    print("## Evaluation mode ##\n Please choose a topic from the list below")
    print(" (1) Topic \n (2) Topic \n (p) previous 10 | (n) next 10")
    input('> ')
    ui_loop()

def ui_loop():
    global scoring, other
    print("### Main menu ###")
    print("Scoring: [{}]\nChoose a mode \n (X) Exploration mode \n (E) Evaluation mode \n (S) Switch to {} \n (Q) Quit".format(scoring,other)) 
    cmd =  input('> ').lower()
    if cmd in ['x', 'exploration']:
        exploration_mode()
    elif cmd in ['e', 'Evaluation']:
        evaluation_mode()   
    elif cmd in ['q', 'quit']:
        print("Exiting!")
        exit()
    elif cmd in ['s', 'switch']:
        scoring, other = other, scoring
        print("Switch to {}".format(scoring))
        ui_loop()
    else:
        print("Unknown command...")
        ui_loop()


def main():
    print(" ~ Welcome to our search engine! ~ ")    
    ui_loop()

if __name__ == "__main__":
    main()

