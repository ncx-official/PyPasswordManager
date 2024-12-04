from database.initialize_db import initialize_database as init_db 

def test():
    # init_db()
    pass


def main():
    print("Console Password Manager v1.0")

    while True:
        print("1) Add password")
        print("2) Edit Password")
        print("3) Delete Password")
        print("4) Retrieve Password")
        print("0) Exit")

        userInput = input("\nChoose an option:")
        if userInput == '1':
            # add_password
            pass
        elif userInput == '2':
            # edit_password
            pass
        elif userInput == '3':
            # delete_password
            pass
        elif userInput == '4':
            # retrieve_password
            pass
        else: #exit
            break
            


if __name__ == "__main__":
    # main()
    test()