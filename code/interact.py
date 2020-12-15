import loadindexfromdisk as lix

scoring = 'TFIDF'
other = 'BM25'

def exploration_mode(index):
    print("## Exploration mode ##\n Please provide a search query:")
    query = input('> ')
    ui_loop(index)

def evaluation_mode(index):
    print("## Evaluation mode ##\n Please choose a topic from the list below")
    print(" (1) Topic \n (2) Topic \n (p) previous 10 | (n) next 10")
    input('> ')
    ui_loop(index)

def ui_loop(index):
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
        ui_loop(index)
    else:
        print("Unknown command...")
        ui_loop(index)


def main():
    print(" ~ Welcome to our search engine! ~ ")
    print('Preparing index...')
    index = lix.load('../data/eval-set_index')
    print('Index ready, let\'s go!')
    ui_loop(index)

if __name__ == "__main__":
    main()

