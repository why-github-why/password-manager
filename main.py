from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import json
from password_data import generate_password

FONT = ("Roboto", 16, "bold")
FONT_BUTTON = ("Roboto", 12, "bold")
RED = "#d4483b"

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=60)

website = StringVar()
email = StringVar()
password = StringVar()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_new_password():
    users_password = password.get()
    if len(users_password) == 0:
        new_password = generate_password()
        password_entry.insert(0, new_password)
        window.clipboard_clear()
        window.clipboard_append(new_password)
    else:
        password_entry.delete(0, END)
        new_password = generate_password()
        password_entry.insert(0, new_password)
        window.clipboard_clear()
        window.clipboard_append(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    users_website = website.get()
    users_email = email.get()
    users_password = password.get()
    new_data = {
        users_website: {
            "email": users_email,
            "password": users_password,
        }
    }

    if len(users_website) == 0:
        messagebox.showerror(title="Info missing", message="Please provide Website.")
    elif len(users_email) == 0:
        messagebox.showerror(title="Info missing", message="Please provide Email/Username.")
    elif len(users_password) == 0:
        messagebox.showerror(title="Info missing", message="Please provide Password.")
    else:
        ok_to_save = messagebox.askokcancel(title="Confirmation.", message=f"These are the details entered:\n"
                                                                           f"Website: {users_website}\n"
                                                                           f"Email: {users_email}\n"
                                                                           f"Password: {users_password}\n"
                                                                           f"Is it OK to save?")
        if ok_to_save:
            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)  # read JSON data
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)  # update JSON data

                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)  # save JSON data
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

            # with open("data.txt", mode="a") as data_file:
            #     data_file.write(f"{users_website} | {users_email} | {users_password}\n")  # write to txt file
            #     website_entry.delete(0, END)
            #     password_entry.delete(0, END)
            #     confirmation = Label(foreground="green")
            #     confirmation.config(text="Password saved!", font=FONT)
            #     confirmation.grid(column=1, row=5, pady=5)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    queried_website = website.get()
    try:
        with open("data.json", mode="r") as data_file:
            queried_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if queried_website in queried_data:
            queried_email = queried_data[queried_website]["email"]
            queried_password = queried_data[queried_website]["password"]
            messagebox.showinfo(title=queried_website, message=f"Email: {queried_email}\n"
                                                               f"Password: {queried_password}")
        else:
            messagebox.showerror(title="Website missing", message=f"No details for {queried_website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
# Canvas
canvas = Canvas(width=400, height=400)
image = PhotoImage(file="./media/logo.png")
canvas.create_image(200, 200, image=image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label()
website_label.config(text="Website:", font=FONT)
website_label.grid(column=0, row=1)

email_label = Label()
email_label.config(text="Email/Username:", font=FONT)
email_label.grid(column=0, row=2)

password_label = Label()
password_label.config(text="Password:", font=FONT)
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=70, textvariable=website)
website_entry.grid(column=1, row=1, pady=2, ipady=3)
website_entry.focus()

email_entry = Entry(width=105, textvariable=email)
email_entry.grid(column=1, row=2, columnspan=2, pady=2, ipady=3)
email_entry.insert(0, "llkleinhans@gmail.com")

password_entry = Entry(width=70, textvariable=password)
password_entry.grid(column=1, row=3, pady=2, ipady=3)

# Style
style = Style()
style.configure("TButton", font=FONT_BUTTON, foreground=RED)

# Buttons
search_button = Button(text="Search", style="TButton", width=22, command=find_password)
search_button.grid(column=2, row=1)

generate_password_button = Button(text="Generate Password", width=22, command=generate_new_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=70, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
