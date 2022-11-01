import tkinter as tk
from tkinter import filedialog as fd
from functions import (
    deep_folders,
    rename_and_relocation,
    rename_and_relocation_without_arch,
    del_empty_dirs,
    result_sorting_with_arch,
    result_sorting_without_arch,
)

root = tk.Tk()
root.title("Сортувалка")
root.geometry("+350+300")


def main():
    try:
        adress = str(way_for_sort.get())
        if unpack_var.get() == 1 and deep_var.get() == 1:
            deep_folders(adress)
            rename_and_relocation(adress)
            result_sorting_with_arch(adress)
        if unpack_var.get() == 1 and deep_var.get() != 1:
            rename_and_relocation(adress)
            result_sorting_with_arch(adress)
        if unpack_var.get() != 1 and deep_var.get() == 1:
            deep_folders(adress)
            rename_and_relocation_without_arch(adress)
            result_sorting_without_arch(adress)
        if unpack_var.get() != 1 and deep_var.get() != 1:
            rename_and_relocation_without_arch(adress)
            del_empty_dirs(adress)
            result_sorting_without_arch(adress)
    except:
        err_win = tk.Tk()
        tk.Label(err_win, text="Спочатку вкажіть шлях до папки!").grid(
            pady=5, padx=5)
        err_win.geometry("+550+350")

        def exit_err():
            err_win.destroy()

        tk.Button(err_win, text="Ok", command=exit_err).grid(pady=5, padx=5)


tk.Label(root, text="Папка для сортування:").grid(
    row=0, column=0, pady=5, padx=5)
tk.Label(
    root,
    text="ПОПЕРЕДЖЕННЯ! Назви файлів з кириличними символами будуть транслітеровані!",
    font=("Times new roman", 10, "italic"),
).grid(row=4, column=1, columnspan=2, pady=5, padx=5, sticky="e")

unpack_var = tk.IntVar()
unpack = tk.Checkbutton(
    root, text="Розпаковка архівів", variable=unpack_var)
unpack.grid(row=3, column=0, columnspan=2, sticky="w")

deep_var = tk.IntVar()
deppest = tk.Checkbutton(
    root, text="Сортувати у вкладених папках", variable=deep_var)
deppest.grid(row=4, column=0, columnspan=2, sticky="w")

way_for_sort = tk.Entry(root, width=100)
way_for_sort.grid(row=0, column=1)


def callback():
    name = fd.askdirectory()
    way_for_sort.insert(0, name)
    return str(name)


tk.Button(text="Знайти папку",
          command=callback).grid(row=1, column=1)

tk.Button(root, text="Сортувати!", command=main).grid(
    row=1, column=1, pady=5, padx=5, sticky="e"
)

if __name__ == "__main__":
    root.mainloop()
