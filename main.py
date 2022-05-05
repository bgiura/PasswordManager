import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from random import sample, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

generate_key = Fernet.generate_key()


def generate():
    password_entry.delete(0, "end")

    low_letters = "abcdefghijklmnopqrstuvwxyz"
    up_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = r"!\#$%&'()*+-/:;<=>?@[]^_"

    ultimate_password = sample(low_letters, 1) + sample(up_letters, 1) + \
                        sample(numbers, 6) + sample(symbols, 2)

    shuffle(ultimate_password)
    pyperclip.copy("".join(ultimate_password))
    return password_entry.insert(0, "".join(ultimate_password))


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    if len(website_entry.get()) == 0 or len(user_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo(title="Uyarı!", message="Lütfen bütün alanları doldurunuz.")
    else:
        validation = messagebox.askokcancel(title="Şifre Yöneticisi",
                                            message=f"Web Sitesi: {website_entry.get().title()}\n"
                                                    f"Kullanıcı Adınız: {user_entry.get()}\n"
                                                    f"Şifreniz: {password_entry.get()}\n"
                                                    f"Onaylıyor musunuz?")
        get_user = str(encrypt(user_entry.get().encode(), generate_key))
        get_pass = str(encrypt(password_entry.get().encode(), generate_key))
        f1get_user = get_user[2:-1]  ### byte'ı stringe çevirince başında oluşan b' karakterleri yüzünden invalid token hatası veriyordu.
        f1get_pass = get_pass[2:-1]  ### baştaki b' ve ' karakterini silince sorun ortadan kalktı.
        if validation:
            new_data = {
                website_entry.get().lower():
                    {"Kullanıcı Adı": f1get_user,
                     "Şifre": f1get_pass}
            }

            try:
                with open("data.json", "r", encoding="utf8") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)

                with open("data.json", "w", encoding="utf8") as data_file:
                    json.dump(data, data_file, indent=4, ensure_ascii=False)

            except FileNotFoundError:
                with open("data.json", "w", encoding="utf8") as data_file:
                    json.dump(new_data, data_file, indent=4, ensure_ascii=False)

            except json.decoder.JSONDecodeError:
                with open("data.json", "w", encoding="utf8") as data_file:
                    json.dump(new_data, data_file, indent=4, ensure_ascii=False)

            finally:
                password_entry.delete(0, "end")
                website_entry.delete(0, "end")
                website_entry.focus()

                messagebox.showinfo(title="Başarılı!", message="Bilgileriniz Başarıyla Kaydedildi.")


def show_info():
    try:
        with open("data.json", "r", encoding="utf8") as data_file:
            data = json.load(data_file)
            user_entry.delete(0, "end")
            password_entry.delete(0, "end")
            user_ask = data[website_entry.get().lower()]
            token_user = user_ask['Kullanıcı Adı'].encode()
            token_pass = user_ask['Şifre'].encode()
            dc_user = decrypt(token_user, generate_key)
            dc_pass = decrypt(token_pass, generate_key)
            password_entry.insert(0, dc_pass.decode())
            user_entry.insert(0, dc_user.decode())



        messagebox.showinfo(title=f"{website_entry.get().title()}", message=f"Kullanıcı Adınız: "
                                                                            f"{dc_user.decode()}\n"
                                                                            f"Şifreniz: {dc_pass.decode()}")
    except KeyError:
        messagebox.showerror(title="Uyarı", message="Kayıt Bulunamadı. Web sitesi "
                                                    "ismini doğru yazdığınızdan emin olunuz "
                                                    "veya bütün karakterleri küçük harfle "
                                                    "girmeyi deneyiniz.")
    except FileNotFoundError:
        messagebox.showerror(title="Uyarı", message="Kayıt Bulunamadı")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Uyarı", message="Kayıt Bulunamadı")
    finally:
        website_entry.focus()


def copy_password():
    if len(password_entry.get()) == 0:
        messagebox.showerror(title="Uyarı", message="Lütfen şifre giriniz.")
    else:
        pyperclip.copy(password_entry.get())
        messagebox.showinfo(title="Şifre Yöneticisi", message=f"Şifreniz '{password_entry.get()}' başarılı"
                                                              f" bir şekilde kopyalandı.")


def copy_username():
    if len(user_entry.get()) == 0:
        messagebox.showerror(title="Uyarı", message="Lütfen kullanıcı adınızı giriniz.")
    else:
        pyperclip.copy(user_entry.get())
        messagebox.showinfo(title="Şifre Yöneticisi", message=f"Kullanıcı adınız '{user_entry.get()}' başarılı"
                                                              f" bir şekilde kopyalandı.")


def clear():
    website_entry.delete(0, "end")
    user_entry.delete(0, "end")
    password_entry.delete(0, "end")


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()
window.title("Şifre Yöneticisi")
window.config(padx=20, pady=50)
window.minsize(505, 412)

canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
photo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1, padx=3, pady=3)

website_label = tk.Label(text="Web Sitesi :")
website_label.grid(row=1, column=0, padx=3, pady=3)

website_entry = tk.Entry(width=24)
website_entry.grid(row=1, column=1, padx=3, pady=3, sticky="W")
website_entry.focus()

search_button = tk.Button(text="Ara", width=17, command=show_info)
search_button.grid(row=1, column=1, columnspan=2, padx=3, pady=3, sticky="E")

user_label = tk.Label(text="E-mail/Kullancı Adı :")
user_label.grid(row=2, column=0)

user_entry = tk.Entry(width=45)
user_entry.grid(row=2, column=1, padx=3, pady=3)
user_entry.insert(0, "@gmail.com")

password_label = tk.Label(text="Şifre :")
password_label.grid(row=3, column=0, padx=3, pady=3)

password_entry = tk.Entry(width=23)
password_entry.grid(row=3, column=1, padx=5, sticky="W")

generate_button = tk.Button(text="Rastgele Şifre Oluştur", width=17, command=generate)
generate_button.grid(row=3, column=1, padx=0, sticky="E")

copy_password_button = tk.Button(text="Şifreyi Kopyala", width=17, command=copy_password)
copy_password_button.grid(row=4, column=1, padx=0, sticky="E")

copy_userentry_button = tk.Button(text="Kullanıcı Adını Kopyala", width=19, command=copy_username)
copy_userentry_button.grid(row=4, column=1, padx=3, pady=3, sticky="W")

clear_button = tk.Button(text="Temizle", command=clear)
clear_button.grid(row=5, column=1, columnspan=2, padx=3, pady=3, sticky="EW")

add_button = tk.Button(text="Kaydet", width=39, command=save_data)
add_button.grid(row=6, column=1, columnspan=2, padx=3, pady=3, sticky="EW")

window.mainloop()
