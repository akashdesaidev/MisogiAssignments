def userInput():
    try:
        age= int(input("Enter your age (1-120): "))
        if age < 0 or age>120:
            raise ValueError("out of range. Please enter between 1 and 120")
        else:
            print("You enetered a valid age")
    except Exception as e:
        print(e)
        userInput()

userInput()
