from tkinter import *
from PIL import Image, ImageTk
from cryptography.fernet import Fernet, InvalidToken
import tkinter.messagebox as messagebox

# Anahtar oluşturma
key = Fernet.generate_key()
cipher = Fernet(key)

wd = Tk()
wd.title("Secret Notes")
wd.config(padx=20, pady=20)

img = Image.open(r"C:\Users\arsla\Desktop\Tkinter\Top-secret.jpg")
photo = ImageTk.PhotoImage(img)
lab = Label(image=photo)
lab.pack()

def btn_click():
    title = entry_title.get()
    secret = secret_text.get("1.0", "end-1c")
    encrypted_secret = encrypt_message(secret.encode(), cipher)
    save_notes(title, encrypted_secret)
    clear_entries()

def save_notes(title, secret):
    with open(r"C:\Users\arsla\Desktop\Tkinter\notes.txt", "a") as file:
        file.write(f"Title: {title}\n")
        file.write(f"Secret: {secret.decode()}\n\n")

def encrypt_message(message, cipher):
    encrypted_message = cipher.encrypt(message)
    return encrypted_message

def decrypt_message(encrypted_message, cipher):
    try:
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode()
    except InvalidToken:
        return None

def read_notes():
    with open(r"C:\Users\arsla\Desktop\Tkinter\notes.txt", "r") as file:
        notes = file.readlines()
    return notes

def display_notes():
    notes = read_notes()
    for note in notes:
        print(note.strip())  # strip() metoduyla boşlukları kaldır

def decrypt_and_display():
    encrypted_text = secret_text.get("1.0", "end-1c").encode()
    decrypted_text = decrypt_message(encrypted_text, cipher)
    if decrypted_text is None:
        messagebox.showerror("Error", "Invalid secret or key")
    else:
        secret_text.delete("1.0", "end")
        secret_text.insert("1.0", decrypted_text)

def clear_entries():
    entry_title.delete(0, END)
    secret_text.delete("1.0", END)
    entry_text.delete(0, END)  # Key alanını da temizle

label_title = Label(text="Enter Your Title")
label_title.config(pady=10)
label_title.pack()

entry_title = Entry(width=40)
entry_title.pack()

label_title_1 = Label(text="Enter Your Secret")
label_title_1.config(pady=10)
label_title_1.pack()

secret_text = Text(width=20, height=10)
secret_text.pack()

label_title_2 = Label(text="Enter Master Key")
label_title_2.config(pady=10)
label_title_2.pack()

entry_text = Entry(width=20, show="*")
entry_text.pack()

svg_btn = Button(text="Save & Encrypt", command=btn_click)
svg_btn.pack()

dec_btn = Button(text="Decrypt", command=decrypt_and_display)
dec_btn.pack()

wd.mainloop()
