import database
import json
import datetime as dt
import tkinter as tk
login_window = tk.Tk()
idx = 0
qty = 0
users = database.users
products = database.products
actions = database.actions
cart_actions = database.cart_actions
username = ""
password = ""
search_text = ""
access_prod_id = ""
shopping_cart = {}
prod_to_print = {}
login_window.title("Y8 Online Market")
login_window.geometry("800x600")
title = tk.Label(login_window, text="Welcome to Y8 Online Market", font=("Helvetica", 25))
log_label = tk.Label(login_window, text="", font=("Helvetica", 15))
username_label = tk.Label(login_window, text="Username:", font=("Helvetica", 15))
username_entry = tk.Entry(login_window, font=("Helvetica", 15))
password_label = tk.Label(login_window, text="Password:", font=("Helvetica", 15))
password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 15))

def show_password():
    password_entry.config(show="")
    show_hide_button.config(text="Hide Password", command=hide_password)
def hide_password():
    password_entry.config(show="*"),
    show_hide_button.config(text="Show Password", command=show_password)
    show_hide_button = tk.Button(login_window, text="Show Password", font=("Helvetica", 15), command=show_password)

def main():
    global username, password, idx, shopping_cart, search_text
    username = username_entry.get()
    password = password_entry.get()
    for usrname in users:
        passwd = users[usrname]
        if username == usrname and password == passwd:
            login_window.destroy()
            break
        elif idx < len(users):
            idx += 1 
        else:
            if username == "":
                log_label.config(text="Username cannot be empty!", fg="red")

            elif password == "":
                log_label.config(text="Password cannot be empty!", fg="red")

                elif username == "" and password == "":
                    log_label.config(text="Username and Password cannot be empty!", fg="red")
                else:
                    log_label.config(text="Error: Invalid username or password.", fg="red")
                    idx = 0
                    main()
                try:
                    with open(f"{username}_shopping_cart.json", "r") as f:
                        shopping_cart = json.loads(f.read())
                    except FileNotFoundError:
                        with open(f"{username}_shopping_cart.json", "w") as f:
                            f.write("{}")
                        with open(f"{username}_shopping_cart.json", "r") as f:
                            shopping_cart = json.loads(f.read())
    def destroy_and_run(tk_wigdet: tk.Widget, func):
        tk_wigdet.destroy()
        func()
        greetings_window = tk.Tk()
        message = tk.Label(greetings_window, text=f"Hi {username}! Please click the button below to proceed.", font=("Helvetica", 15))
def main_menu():
    global idx, shopping_cart, username, qty, search_text
    greetings_window.destroy()
    main_window = tk.Tk()
    main_window.title("Y8 Online Market")
    main_window.geometry("800x600")
    title_2 = tk.Label(main_window, text="Y8 Online Market", font=("Helvetica", 30))
    title_2.pack()
    action_buttons = []
    def search():
        global search_text
        in_name_results = []
        prod_to_print = {}
        shop_window = tk.Tk()
        shop_window.title("Y8 Online Market")
        title = tk.Label(shop_window, text="Y8 Online Market - Shopping", font=("Helvetica", 25))
        search_lbl = tk.Label(shop_window, text="Search for: ", font=("Helvetica", 15))
        search = tk.Entry(shop_window, font=("Helvetica", 15))
        error_lbl = tk.Label(shop_window, text="", font=("Helvetica", 15), fg="red")
        def chk():
            search_text = search.get()
            if search_text == "0":
                main_menu()
            for prod_id in products:
                name = products[prod_id]
                if search_text.lower() in name:
                    prod_to_print[prod_id] = name
                    in_name_results.append(search_text.lower() in name)
                for result in in_name_results:
                    if result:
                        break
                    else:
                        error_lbl.config(text="Your search didn't match with anything. Please try again (0 for main menu).")
                        chk()
        def show_similar_products():
            chk()
            global idx
            similar_products_window = tk.Tk()
            s_prod_name = []
            similar_products_window.title("Y8 Online Market - Shopping")
            shop_window.geometry("1000x800")
            match_prod_lbl = tk.Label(similar_products_window, text="Matching products", font=("Helvetica", 20))
            for prod_id in prod_to_print:
                name = prod_to_print[prod_id]
                tk.Label(similar_products_window, text=f"{prod_id}: {name}", font=("Helvetica", 15), relief=tk.SUNKEN).pack(anchor="w")
                prod_lbl = tk.Label(similar_products_window, text="Product code for the wanted product (0 for main menu): ", font=("Helvetica", 15))
                prod_code = tk.StringVar()
                prod_entry = tk.Entry(similar_products_window, font=("Helvetica", 15), textvariable=prod_code)
                add_to_cart_btn = tk.Button(similar_products_window, text="Add to cart", font=("Helvetica", 15))
                error_lbl = tk.Label(similar_products_window, text="", font=("Helvetica", 15), fg="red")
                prod_lbl.pack(anchor="w")
                prod_entry.pack()
                def get_qty():
                    global idx, shopping_cart, username, qty, search_text
                    if (prod := prod_entry.get()) == "0":
                        main_menu()
                        try:
                            s_prod_name = prod_to_print[prod].split(", ")
                        except KeyError:
                            print("Product code didn't match.")
                            show_similar_products()
                        qty = tk.IntVar()
                        qty_lbl = tk.Label(similar_products_window, text="Quantity: ", font=("Helvetica", 15))
                        qty_entry = tk.Entry(similar_products_window, font=("Helvetica", 15), textvariable=qty)
                        qty_lbl.pack(anchor="w")
                        qty_entry.pack()
                        s_prod_name = prod_to_print[prod].split(", ")
                        while qty > int(s_prod_name[2]):
                            qty = int(input("Sorry, the amount passes the limit, please try again with a smaller amount: "))
                            s_prod_name[2] = f"{int(s_prod_name[2]) - qty}"
                            for prod_id in prod_to_print:
                                if prod == prod_id:
                                    shopping_cart[prod_id] = [s_prod_name[0], s_prod_name[1], qty, f"{float(s_prod_name[1].removesuffix('$')) * qty}$"]
                                    with open(f"{username}_shopping_cart.json", "w", encoding="windows-1254") as f:
                                        json.dump(shopping_cart, f)
                                    products[prod_id] = f"{s_prod_name[0]}, {s_prod_name[1]}, {s_prod_name[2]}"
                                    break
                                elif idx < len(prod_to_print):
                                    idx += 1
                                else:
                                    print()
                                idx = 0
                                print("Product successfully added to the shopping cart.")
                        main_menu()
                    add_to_cart_btn.config(command=get_qty)
                    add_to_cart_btn.pack()
                    similar_products_window.mainloop()
                    search_btn = tk.Button(shop_window, text="Search", font=("Helvetica", 15), command=show_similar_products)
                    search_lbl.pack(anchor="w")
                    search.pack()
                    search_btn.pack()
                    search.pack()
            def cart():
                global shopping_cart
                cart_window = tk.Tk()
                empty_cart_lbl = tk.Label(cart_window, text="Your shopping cart is empty.", font=("Helvetica", 15))
                total = 0.0
                if shopping_cart == {}:
                    empty_cart_lbl.pack()
                else:
                    for prod_id in shopping_cart:
                        details = shopping_cart[prod_id]
                        print(f"\t{prod_id} | Name: {details[0]}, Price: {details[1]}, Quantity: {details[2]}, Total Amount: {details[3]}")
                        total += float(details[3].removesuffix("$"))
                    print(f"Total Amount: {total}$")
                for cart_action_enum in cart_actions:
                    action = cart_actions[cart_action_enum]
                    print(f"\t{cart_action_enum}. {action}")
                    def ca_action():
                        global shopping_cart, idx, prod_to_print, access_prod_id
                        ca_choice = int(input("What would you like to do (0 for main menu)? "))
                        if ca_choice == 0:
                            main_menu()
                        if ca_choice == 1:
                            access_prod_id = ""
                            access_prod_id = input("Product code: ").upper()
                            for id in products:
                                if access_prod_id == id:
                                    break
                                elif idx < len(products):
                                    idx += 1
                                else:
                                    idx = 0
                                    print("Product not found.")
                                    main_menu()
                            s_prod_name = products[access_prod_id].split(", ")
                            new_qty = int(input("New quantity: "))
                            for prod_id in products:
                                if prod_id == access_prod_id:
                                    current_qty = shopping_cart[prod_id][2]
                                    s_prod_name[2] = f"{int(s_prod_name[2]) - (new_qty - current_qty)}"
                                    products[prod_id] = f"{s_prod_name[0]}, {s_prod_name[1]}, {s_prod_name[2]}"
                                    for prod_id in shopping_cart:
                                        details = shopping_cart[prod_id]
                                        if access_prod_id == prod_id:
                                            details[2] = new_qty
                                            idx += 1
                                            details[3] = f"{float(details[1].removesuffix('$')) * new_qty}$"
                                        elif idx < len(shopping_cart):
                                            idx += 1
                                        else:
                                            print("Product not found.")
                                            idx = 0
                                            with open(f"{username}_shopping_cart.json", "w") as f2:
                                                json.dump(shopping_cart, f2)
                        elif ca_choice == 2:
                            prod_id = input("Product code: ").upper()
                            for pid in products:
                                if prod_id == pid:
                                    spn = products[pid].split(", ")
                                    spn[2] = f"{int(spn[2]) + shopping_cart[pid][2]}"
                                    products[pid] = f"{spn[0]}, {spn[1]}, {spn[2]}"
                                    shopping_cart.pop(prod_id)
                                    break
                                elif idx < len(products):
                                    idx += 1
                                else:
                                    idx = 0
                                    print("Product not found.")
main_menu()
with open(f"{username}_shopping_cart.json", "w")
as f:                        json.dump(shopping_cart, f)
elif ca_choice == 3:                    for prod_id in shopping_cart:                        spn = products[prod_id].split(", ")
spn[2] = f"{int(spn[2])
+ shopping_cart[prod_id][2]}"                        products[prod_id] = f"{spn[0]}, {spn[1]}, {spn[2]}"                    shopping_cart = {}                    with open(f"{username}_shopping_cart.json", "w")
as f:                        json.dump(shopping_cart, f)
elif ca_choice == 4:                    prod_id = input("Product code: ")
.upper()
try:                        pass                    except KeyError:                        print("Code not found.")
ca_action()
print(f"{shopping_cart[prod_id][3]} has been paid.")
shopping_cart.pop(prod_id)
with open(f"{username}_shopping_cart.json", "w")
as f:                        json.dump(shopping_cart, f)
ca_action()
total = 0.0            if shopping_cart == {}:                print("\tCart is empty.")
else:                for prod_id in shopping_cart:                    details = shopping_cart[prod_id]                    print(f"\t{prod_id} | Name: {details[0]}, Price: {details[1]} Quantity: {details[2]}, Total Amount: {details[3]}")
total += float(details[3].removesuffix("$")
)
print(f"Total Amount: {total}$")
print("Changes succesfully saved.")
def check_out()
:            global shopping_cart            print("Processing receipt...")
print("""******* Y8 Online Market *******    *************************************""")
print("————————————")
for prod_id in shopping_cart:                details = shopping_cart[prod_id]                print(f"{details[0]}, unit price: {details[1]}, quantity: {details[2]}, total amount: {details[3]}")
print("————————————")
total = 0.0            for prod_id in shopping_cart:                details = shopping_cart[prod_id]                total += float(details[3].removesuffix("$")
)
print(f"Total amount: {total}$")
print("————————————")
now = dt.datetime.now()
print(f"{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}:{now.second}")
print("Thank you for shopping with us!")
shopping_cart = {}            with open(f"{username}_shopping_cart.json", "w")
as f:                json.dump(shopping_cart, f)
main_menu()
def logout()
:            main()
def stock()
:            for prod_id in products:                prod_details = products[prod_id]                print(f"\t{prod_id}: {prod_details}")
def exit_om()
:            print("Bye!")
exit(0)
for num in actions:            name = actions[num]            match num - 1:                case 0:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=search)
)
case 1:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=cart)
)
case 2:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=check_out)
)
case 3:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=logout)
)
case 4:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=stock)
)
case 5:                    action_buttons.append(tk.Button(main_window, text=name, font=("Helvetica", 15)
, command=exit_om)
)
for action_button in action_buttons:            action_button.pack()
main_window.mainloop()
greetings_window.title("Y8 Online Market - Greetings")
greetings_window.geometry("600x400")
proceed_btn_2 = tk.Button(greetings_window, text="Proceed", font=("Helvetica", 20)
, command=main_menu)
message.pack()
proceed_btn_2.pack()
greetings_window.mainloop()
proceed_btn = tk.Button(login_window, text="Proceed", font=("Helvetica", 15)
, command=lambda: main()
)
title.pack()
username_label.pack(anchor="w")
username_entry.pack()
password_label.pack(anchor="w")
password_entry.pack()
show_hide_button.pack()
proceed_btn.pack()
log_label.pack()
login_window.mainloop()
