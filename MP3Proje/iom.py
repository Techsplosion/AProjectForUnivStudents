import database
import json
import datetime as dt

idx = 0
amt = 0
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

print("**** İstinye Online Market'e Hoşgeldiniz ****")


def main():
    global username, password, idx, shopping_cart, search_text

    username = input("Kullanıcı adı: ")
    password = input("Şifre: ")

    for usrname in users:
        passwd = users[usrname]
        if username == usrname and password == passwd:
            print("Başarıyla giriş yapıldı.")
            idx += 1
            break

        elif idx < len(users):
            idx += 1

    else:
        print("Şifre ve/veya kullanıcı adı yanlış girildi. Lütfen tekrar deneyin.")
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

    print(f"Hoşgeldiniz {username}! Lütfen ilgili menü numarasını girerek aşağıdaki seçeneklerden birini seçin.")

    def main_menu():
        global idx, shopping_cart, username, amt, search_text

        print("----------------------------------------------------------------------------")

        for num in actions:
            name = actions[num]
            print(f"\t{num}. {name}")


        try:
            choice = int(input("Seçiminiz: "))
            if choice == 1:
                in_name_results = []
                prod_to_print = {}
                search_text = input("Ne arıyorsunuz? ")

                def chk():
                    global search_text
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
                        search_text = input("Aramanız hiçbir öğeyle eşleşmedi. Lütfen başka bir şey deneyin (Ana menü için 0 girin): ")
                        chk()


                def show_similar_products():
                    chk()
                    global idx
                    s_prod_name = []
                    print("Benzer ürünler: ")
                    for prod_id in prod_to_print:
                        name = prod_to_print[prod_id]
                        print(f"\t{prod_id}: {name}")
                    prod = input("Sepete eklenecek ürünün kodu (ana menü için 0): ").upper()

                    if prod == "0":
                        main_menu()

                    try:
                        s_prod_name = prod_to_print[prod].split(", ")
                    except KeyError:
                        print("Ürün kodu herhangi bir kodla eşleşmedi.")
                        show_similar_products()

                    amt = int(input("Miktarı giriniz: "))

                    s_prod_name = prod_to_print[prod].split(", ")

                    while amt > int(s_prod_name[2]):
                        amt = int(input("Üzgünüm! Miktar sınırı aşıyor, Lütfen daha küçük bir miktarla tekrar deneyin: "))
                    s_prod_name[2] = f"{int(s_prod_name[2]) - amt}"
                    for prod_id in prod_to_print:
                        if prod == prod_id:
                            shopping_cart[prod_id] = [s_prod_name[0], s_prod_name[1], amt, f"{float(s_prod_name[1].removesuffix('$')) * amt}$"]

                            with open(f"{username}_shopping_cart.json", "w", encoding="windows-1254") as f:
                                json.dump(shopping_cart, f)

                            products[prod_id] = f"{s_prod_name[0]}, {s_prod_name[1]}, {s_prod_name[2]}"
                            break

                        elif idx < len(prod_to_print):
                            idx += 1

                        else:
                            print()

                    idx = 0
                    print("Ürün sepetinize başarıyla eklendi.")
                    main_menu()

                show_similar_products()

            elif choice == 2:
                total = 0.0
                if shopping_cart == {}:
                    print("\tSepetiniz boş.")
                else:
                    for prod_id in shopping_cart:
                        details = shopping_cart[prod_id]
                        print(f"\t{prod_id} | Ad: {details[0]}, Fiyat: {details[1]}, Miktar: {details[2]}, Tutar: {details[3]}")
                        total += float(details[3].removesuffix("$"))
                print(f"Toplam Tutar: {total}$")
                for cart_action_enum in cart_actions:
                    action = cart_actions[cart_action_enum]
                    print(f"\t{cart_action_enum}. {action}")

                def ca_action():
                    global shopping_cart, idx, prod_to_print, access_prod_id
                    ca_choice = int(input("Ne yapmak istiyorsunuz (ana menü için 0)? "))
                    if ca_choice == 0:
                        main_menu()
                    if ca_choice == 1:
                        access_prod_id = ""
                        access_prod_id = input("Ürün kodu: ").upper()
                        for id in products:
                            if access_prod_id == id:
                                break
                            elif idx < len(products):
                                idx += 1
                            else:
                                idx = 0
                                print("Ürün bulunamadı.")
                                main_menu()
                        s_prod_name = products[access_prod_id].split(", ")
                        new_amt = int(input("Yeni miktar: "))
                        for prod_id in products:
                            if prod_id == access_prod_id:
                                current_amt = shopping_cart[prod_id][2]
                                s_prod_name[2] = f"{int(s_prod_name[2]) - (new_amt - current_amt)}"
                                products[prod_id] = f"{s_prod_name[0]}, {s_prod_name[1]}, {s_prod_name[2]}"

                        for prod_id in shopping_cart:
                            details = shopping_cart[prod_id]
                            if access_prod_id == prod_id:
                                details[2] = new_amt
                                idx += 1
                                details[3] = f"{float(details[1].removesuffix('$')) * new_amt}$"

                            elif idx < len(shopping_cart):
                                idx += 1

                            else:
                                print("Ürün bulunamadı.")

                        idx = 0

                        with open(f"{username}_shopping_cart.json", "w") as f2:
                            json.dump(shopping_cart, f2)

                    elif ca_choice == 2:
                        prod_id = input("Ürün kodu: ").upper()
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
                                print("Ürün bulunamadı.")
                                main_menu()
                        with open(f"{username}_shopping_cart.json", "w") as f:
                            json.dump(shopping_cart, f)

                    elif ca_choice == 3:
                        for prod_id in shopping_cart:
                            spn = products[prod_id].split(", ")
                            spn[2] = f"{int(spn[2]) + shopping_cart[prod_id][2]}"
                            products[prod_id] = f"{spn[0]}, {spn[1]}, {spn[2]}"

                        shopping_cart = {}

                        with open(f"{username}_shopping_cart.json", "w") as f:
                            json.dump(shopping_cart, f)

                    elif ca_choice == 4:
                        prod_id = input("Ürün kodu: ").upper()
                        try:
                            pass
                        except KeyError:
                            print("Ürün kodu herhangi bir kodla eşleşmedi.")
                            ca_action()
                        print(f"{shopping_cart[prod_id][3]} ödenmiştir.")
                        shopping_cart.pop(prod_id)
                        with open(f"{username}_shopping_cart.json", "w") as f:
                            json.dump(shopping_cart, f)
                ca_action()
                total = 0.0

                if shopping_cart == {}:
                    print("\tSepetiniz boş.")
                else:
                    for prod_id in shopping_cart:
                        details = shopping_cart[prod_id]
                        print(f"\t{prod_id} | Ad: {details[0]}, Fiyat: {details[1]} Miktar: {details[2]}, Tutar: {details[3]}")
                        total += float(details[3].removesuffix("$"))
                print(f"Toplam Tutar: {total}$")
                print("Yapılan değişiklikler başarıyla kaydedilmiştir.")

            elif choice == 3:
                print("Makbuzunuz işleniyor...")
                print("""******* İstinye Online Market *******
*************************************""")
                print("————————————")
                print("""\t0850 283 6000
\tistinye.edu.tr""")
                print("————————————")
                for prod_id in shopping_cart:
                    details = shopping_cart[prod_id]
                    print(f"{details[0]}, birim fiyat: {details[1]}, miktar: {details[2]}, tutar: {details[3]}")
                print("————————————")
                total = 0.0
                for prod_id in shopping_cart:
                    details = shopping_cart[prod_id]
                    total += float(details[3].removesuffix("$"))
                print(f"Toplam tutar: {total}$")
                print("————————————")
                now = dt.datetime.now()
                print(f"{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}:{now.second}")
                print("Online Market’imizi kullandığınız için teşekkür ederiz!")
                shopping_cart = {}
                with open(f"{username}_shopping_cart.json", "w") as f:
                    json.dump(shopping_cart, f)

                main_menu()

            elif choice == 4:
                main()

            elif choice == 5:
                for prod_id in products:
                    prod_details = products[prod_id]
                    print(f"\t{prod_id}: {prod_details}")

            elif choice == 6:
                print("Görüşürüz!")
                exit(0)

            else:
                print("Girişiniz verilen seçenekleden biriyle ilişkili değildir. Lütfen aşağıdaki şeçeneklerden birini seçiniz.")
                main_menu()
        except ValueError:
            print("Girişiniz numaralar dışında herhangi bir şey içeremez. Lütfen aşağıdaki şeçeneklerden birini seçiniz.")
            main_menu()
        main_menu()

    main_menu()


main()
