import os.path
from Categories import Categories
import platform
import time
try:
    # Function to return the current income which is saved to totalMoney.txt
    def get_current_income():
        get_income = open('totalMoney.txt')
        current_income = round(float(get_income.read()), 2)
        get_income.close()
        return current_income

    # Function to set a new value which will be saved in totalMoney.txt (overwrites previously saved)
    def set_current_income(income):
        while True:
            clear_console()
            print(f"current income: £{income}")
            set_income_input = input("Enter a new income:\n£")
            try:
                float(set_income_input)
            except ValueError:
                print("Enter a valid value.")
                time.sleep(2)
                continue
            set_income_input = str(abs(float(set_income_input)))
            set_income = open('totalMoney.txt', 'w')
            set_income.write(set_income_input)
            set_income.close()
            break

    # Function to detect the operating system being used by the user and clears terminal/cmd
    def clear_console():
        system = platform.system()
        if system == "Linux" or system == "Darwin":
            os.system('clear')
        else:
            os.system('cls')

    # returns the allocated values as a list, read from categories.txt
    def get_allocated(are_you_setting):
        allocated_list = []
        read_file = open('categories.txt')
        for line in read_file:
            if are_you_setting is False:
                allocated_list.append(float(line.rstrip()))
            else:
                allocated_list.append(line)
        read_file.close()
        return allocated_list

    # Overwrites categories.txt with a new list which is heavily sanitized to ensure
    # the overall value doesn't exceed the user inputted income (saved in totalMoney.txt).
    # Its size is a result of the sanitization
    def set_allocated(index_of_change, list_of_allocation, list_of_categories, cannot_exceed):
        while True:
            clear_console()
            allocated_list = list_of_allocation.copy()
            float_allocated_list = []
            for float_allocated in allocated_list:
                float_allocated = float((float_allocated.rstrip()))
                float_allocated_list.append(float_allocated)
            print(f"you have £{cannot_exceed - sum(float_allocated_list)} left to allocate")
            print(f"{int(allocated_list[index_of_change])}")
            user_alloc = input(f"Type the amount you would like to allocate to {list_of_categories[index_of_change].category_name}\n£")
            try:
                float(user_alloc)
            except ValueError:
                print("Invalid Input.")
                time.sleep(2)
                continue
            if cannot_exceed < (sum(float_allocated_list) + float(user_alloc)):
                print(f"Your input of {user_alloc} is too big for your income.")
                input()
                clear_console()
                continue
            allocated_list[index_of_change] = user_alloc + '\n'
            write_file = open('categories.txt', 'w')
            string_to_write = ''.join(allocated_list)
            write_file.write(string_to_write)
            write_file.close()
            clear_console()
            break

    # Main program
    def main():
        clear_console()
        if os.path.exists('totalMoney.txt') is False or os.path.getsize('totalMoney.txt') == 0:
            create_new = open('totalMoney.txt', 'w')
            create_new.write('0')
            create_new.close()
        if os.path.exists('categories.txt') is False or os.path.getsize('categories.txt') == 0:
            create_new_cat = open('categories.txt', 'w')
            create_new_cat.write('0\n0\n0\n0\n0\n0')
            create_new_cat.close()
        get_allocated(False)

        print(f"Your current income is £{get_current_income()}")
        choice0 = input("type 'budget' to manage budget, or 'income' to change your income: \n")

        if "income" in choice0:
            clear_console()
            set_current_income(get_current_income())
            main()

        elif "budget" in choice0:
            clear_console()
            while True:
                print("Category  :  Money Allocated  :  Access Number")
                # Easily modifiable by adding another element to this list
                category_list = [
                    Categories("Bills", get_allocated(False)[0], 0),
                    Categories("Shopping", get_allocated(False)[1], 1),
                    Categories("Food Shopping", get_allocated(False)[2], 2),
                    Categories("Luxury", get_allocated(False)[3], 3),
                    Categories("Savings", get_allocated(False)[4], 4),
                    Categories("Other", get_allocated(False)[5], 5)
                ]
                # Loops throughout the list and prints the attributes
                for category in category_list:
                    print(f"{category.category_name} : £{category.money_allocated} : {category.index_inside_list}")
                budget_change = input("Enter the access number of the category you'd like to change"
                                      " when you are done, type 'quit'\n")
                if 'quit' in budget_change:
                    main()
                try:
                    int(budget_change)
                    if int(budget_change) > (len(category_list) - 1):
                        raise ValueError
                except ValueError:
                    print("Please enter a valid input.")
                    time.sleep(2)
                    clear_console()
                    continue
                set_allocated(int(budget_change), get_allocated(True), category_list, get_current_income())

        else:
            print("please enter a valid input.")
            time.sleep(2)
            main()


    # Checks to ensure this is being ran as a script
    if __name__ == '__main__':
        main()
    else:
        raise Exception("Standalone app - not a module therefore must not be imported")

except KeyboardInterrupt:
    print("Thanks for using!")

