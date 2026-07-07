import tkinter as tk
from tkinter import filedialog, messagebox

def generate_script():
    name = name_entry.get()

    script = f"""[Unit]
Description=I2C Display Script
After=multi-user.target

[Service]
User={name}
WorkingDirectory=/home/{name}/dht20-env
ExecStart=/home/{name}/dht20-env/bin/python /home/{name}/temphumiditydisplay.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

    with open("display.service", "w") as f:
        f.write(script)

    messagebox.showinfo("Done", "Script created successfully! Place display.service in /etc/systemd/system/")

# windows size
root = tk.Tk()
root.title("Script Configurator")
root.geometry("280x100")

# name input field
tk.Label(root, text="Raspberry Pi Username:").pack()
name_entry = tk.Entry(root)
name_entry.pack()


# generate button
tk.Button(root, text="Generate Script", command=generate_script).pack(pady=18)

root.mainloop()