from crawller import start, clear_data

def show_options():
    print("1. Resume crawlling from last state.")
    print("2. Clear previous data and restart crawlling.")
    print("3. Just clear data and do nothing more.")
    print("Q. Quit.")

def get_option():
    op = input("Press option number: ")
    return op

if __name__ == "__main__":
    print("Choose options:")
    show_options()
    while True:
        option = get_option()
        if option == '1':
            start()
        elif option == '2':
            clear_data()
            start() 
        elif option == '3':
            clear_data()
        elif option.lower() == 'q':
            break
        else:
            print("Please choose one of the options mentioned below.!!")
            show_options()