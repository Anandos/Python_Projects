import tkinter, random, pyperclip, json
from tkinter import messagebox
GRAY = "#737373"
WHITE = "#FFFFFF"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
alpha_num = ["a", "b", "c", "d", 'e', "f", 'g', "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "v",
             "w", "x", "y", "z",
             "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "?", "!", "@", "£", "$", "%", "&", "*", "(", ")"]

def password_gen():
    password = ""
    for i in range(12):
        password += random.choice(alpha_num)
    password_text.delete("1.0", "end")
    password_text.insert("1.0", password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_file():
    website = website_entry.get()
    email = email_entry.get()
    password = password_text.get("1.0", "end")
    if website == "":
        messagebox.showinfo(title="missing website", message="Please enter a valid website")
    elif email == "":
        messagebox.showinfo(title="missing email", message="Please enter a valid email")
    elif len(password) < 3:
        messagebox.showinfo(title="missing password", message="Please enter a valid password")
    else:
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }
        is_ok = messagebox.askyesno(title="Save these details?",
                                    message=f"These are the details entered:\nwebsite: {website}\nemail: "
                                            f"{email}\npassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("./data.json", "r") as data_file:
                    updated_data = json.load(data_file)
                    updated_data.update(new_data)  # load old data into updated_data, update it with new_data
            except FileNotFoundError:
                with open("./data.json", "w") as data_file:  # opening file in write mode, creates the file
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("./data.json", "w") as data_file:
                    json.dump(updated_data, data_file, indent=4)
            finally:
                password_text.delete("1.0", "end")
                # website_entry.delete("1.0", "end")
# Search for password---------------------------------------------------#
def search():
    return_website = website_entry.get()
    try:
        with open("./data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(message="Sorry, no data found")
    else:
        if return_website in data:
            return_password = data[return_website]["password"]
            return_email = data[return_website]["email"]
            print(return_website, return_password)
            pyperclip.copy(return_password)
            messagebox.showinfo(title="Searched for password",
                                message=f"{return_website}\n{return_email}\npassword: {return_password}\n")
        else:
            messagebox.showinfo(message=f"Sorry, password for '{return_website}' not found")

# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manager")
window.minsize(300, 300)
window.config(padx=50, pady=50, bg=GRAY)

logo_png = tkinter.PhotoImage(file="logo.png")

canvas = tkinter.Canvas(height=200, width=200, highlightthickness=0, bg=GRAY)
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

# website label
website_label = tkinter.Label(text="Website:", fg=WHITE, bg=GRAY)
website_label.grid(column=0, row=1)
# website entry
website_entry = tkinter.Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1, sticky="EW")
# email label
email_label = tkinter.Label(text="Email/Username:", fg=WHITE, bg=GRAY)
email_label.grid(column=0, row=2)
# email entry
email_entry = tkinter.Entry(width=35)
email_entry.insert(0, "dantemustdie300@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
# password label
password_label = tkinter.Label(text="Password:", fg=WHITE, bg=GRAY)
password_label.grid(column=0, row=3)
# password
password_text = tkinter.Text(height=1, width=21)
password_text.grid(column=1, row=3, sticky="EW")
# password button
password_button = tkinter.Button(text="Generate Password", bg=GRAY, highlightthickness=0, command=password_gen)
password_button.grid(column=2, row=3, sticky="EW")
# add button
add_button = tkinter.Button(text="Add", width=35, bg=GRAY, highlightthickness=0, command=save_file)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")
# search button
search_button = tkinter.Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
