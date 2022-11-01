import os
import shutil
import constants as CON
import tkinter as tk

all_resume = ""


def find_images(adress):
    files = os.listdir(adress)
    type_img = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), CON.IMAGES)),
            files,
        )
    )
    return type_img


def find_video(adress):
    files = os.listdir(adress)
    type_video = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), CON.VIDEO)),
            files,
        )
    )
    return type_video


def find_docs(adress):
    files = os.listdir(adress)
    type_docs = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), CON.DOCS)),
            files,
        )
    )
    return type_docs


def find_music(adress):
    files = os.listdir(adress)
    type_mus = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), CON.MUSIC)),
            files,
        )
    )
    return type_mus


def find_archives(adress):
    files = os.listdir(adress)
    type_arch = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), CON.ARCHIVES)
            ),
            files,
        )
    )
    return type_arch


def dont_know_files(adress):
    all_in = find_images(adress)
    all_in.extend(find_video(adress))
    all_in.extend(find_docs(adress))
    all_in.extend(find_music(adress))
    all_in.extend(find_archives(adress))
    files = os.listdir(adress)
    type_any = []
    for i in files:
        if i not in all_in:
            type_any.append(i)
    return type_any


def del_empty_dirs(adress):
    for d in os.listdir(adress):
        a = os.path.join(adress, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)


def deep_folders(adress):
    for el in os.listdir(adress):
        way = os.path.join(adress, el)
        if os.path.isdir(way):
            files_in_way = os.listdir(way)
            for i in files_in_way:
                shutil.move(os.path.join(way, i), adress)
                del_empty_dirs(adress)
            if not os.path.isdir(adress):
                break
            else:
                deep_folders(adress)


def normalize(adress, filename):
    find_kyrill = [x for x in CON.CYRILLIC_SYMBOLS if x in filename.lower()]
    name_cln = ""
    if len(find_kyrill) > 0:
        result = filename.translate(CON.TRANS)
        for el in result:
            if el.isalpha() or el.isalnum() or el == ".":
                name_cln += el
            if el in CON.SUMB:
                name_cln += el.replace(el, "_")
        oldname = os.path.join(adress, filename)
        newname = os.path.join(adress, name_cln)
        os.rename(oldname, newname)


def transfer_files(adress, folder_name, files):
    if folder_name not in adress:
        os.chdir(adress)
        os.mkdir(folder_name)
    if folder_name == "archives":
        to_unpack_folder = os.path.join(adress, folder_name)
        os.chdir(to_unpack_folder)
        for arch_name in files:
            named = arch_name.split(".")
            name = named[0]
            os.mkdir(name)
            path_to_unpack = os.path.join(to_unpack_folder, name)
            file_for_unpack = os.path.join(adress, arch_name)
            try:
                shutil.unpack_archive(file_for_unpack, path_to_unpack)
                os.remove(file_for_unpack)
            except shutil.ReadError:
                all_err_arch = []
                error_name = os.path.split(file_for_unpack)
                all_err_arch.append(error_name[-1])
                del_empty_dirs(os.path.join(adress, "archives"))
                global all_resume
                all_resume += (
                    f"Файл {all_err_arch} має розширення архіву, проте не є ним.\n"
                )
    if folder_name != "archives":
        file_destination = os.path.join(adress, folder_name)
        get_files = files
        for files in get_files:
            shutil.move(os.path.join(adress, files), file_destination)


def transfer_without_archives(adress, folder_name, files):
    if folder_name not in adress:
        os.chdir(adress)
        os.mkdir(folder_name)
    if folder_name != "archives":
        file_destination = os.path.join(adress, folder_name)
        get_files = files
        for files in get_files:
            shutil.move(os.path.join(adress, files), file_destination)


def rename_and_relocation_without_arch(adress):

    dont_know_files(adress)
    no_type = dont_know_files(adress)

    files = os.listdir(adress)
    for file in files:
        if file not in no_type:
            normalize(adress, file)

    find_images(adress)
    image_files = find_images(adress)
    transfer_without_archives(adress, "images", image_files)

    find_music(adress)
    music_files = find_music(adress)
    transfer_without_archives(adress, "music", music_files)

    find_video(adress)
    video_files = find_video(adress)
    transfer_without_archives(adress, "video", video_files)

    find_docs(adress)
    documents_files = find_docs(adress)
    transfer_without_archives(adress, "documents", documents_files)

    find_archives(adress)
    archice_files = find_archives(adress)
    transfer_without_archives(adress, "archives", archice_files)
    global all_resume
    all_resume += f"Ось це залишилося там, де й було: {no_type}\n"


def rename_and_relocation(adress):

    dont_know_files(adress)
    no_type = dont_know_files(adress)

    files = os.listdir(adress)
    for file in files:
        if file not in no_type:
            normalize(adress, file)

    find_images(adress)
    image_files = find_images(adress)
    transfer_files(adress, "images", image_files)

    find_music(adress)
    music_files = find_music(adress)
    transfer_files(adress, "music", music_files)

    find_video(adress)
    video_files = find_video(adress)
    transfer_files(adress, "video", video_files)

    find_docs(adress)
    documents_files = find_docs(adress)
    transfer_files(adress, "documents", documents_files)

    find_archives(adress)
    archice_files = find_archives(adress)
    transfer_files(adress, "archives", archice_files)
    global all_resume
    all_resume += f"Ось це залишилося там, де й було: {no_type}\n"


def resume_with_arch(*args, adress, name="archives"):
    global all_resume
    for name_fold in args:
        way_for_resume = os.path.join(adress, name_fold)
        files = os.listdir(way_for_resume)
        count_images = len(files)
        line_of_ras = []
        for el in files:
            format = el.split(".")
            line_of_ras.append(format[-1].lower())
        line_of_ras = set(line_of_ras)
        one_el_line = (
            f"До папки {name_fold} було відсортовано файли у кількості {count_images} шт. Їх формати: {[el for el in line_of_ras]}\n"
        )
        all_resume += one_el_line
    dop_way = os.path.join(adress, name)
    files = os.listdir(dop_way)
    count_ar = len(files)
    line = []
    archice_files = find_archives(adress)
    for files in archice_files:
        named = files.split(".")
        line.append(named[-1])
    line = set(line)
    arch_part_of_resume = (
        f"Також я розпакував архіви, у кількості {count_ar} шт. Вони тепер у папці {name}. До розпаковки вони були такого формату: {[el for el in line]}"
    )
    all_resume += arch_part_of_resume
    return all_resume


def resume_without_arch(*args, adress):
    global all_resume
    for name_fold in args:
        way_for_resume = os.path.join(adress, name_fold)
        files = os.listdir(way_for_resume)
        count_images = len(files)
        line_of_ras = []
        for el in files:
            format = el.split(".")
            line_of_ras.append(format[-1].lower())
        line_of_ras = set(line_of_ras)
        one_el_line = (
            f"До папки {name_fold} було відсортовано файли у кількості {count_images} шт. Їх формати: {[el for el in line_of_ras]}\n"
        )
        all_resume += one_el_line
    return all_resume


def result_sorting_with_arch(adress):
    resume_win = tk.Tk()
    resume_win.title("Звіт")
    resume_win.geometry('+400+250')
    text_resume = resume_with_arch(
        "images", "video", "documents", "music", adress=adress, name="archives"
    )
    tk.Label(resume_win, text=text_resume, font=("Times new roman", 12)).grid(
        row=0, column=0, padx=5, pady=5
    )

    def exit_resume_win():
        global all_resume
        all_resume = ''
        resume_win.destroy()

    tk.Button(resume_win, text="Ok", command=exit_resume_win, height=2, width=6).grid(
        row=1, column=0, padx=5, pady=5
    )


def result_sorting_without_arch(adress):
    resume_win = tk.Tk()
    resume_win.title("Звіт")
    resume_win.geometry('+400+250')
    text_resume = resume_without_arch(
        "images", "video", "documents", "music", adress=adress
    )
    tk.Label(resume_win, text=text_resume, font=("Times new roman", 12)).grid(
        row=0, column=0, padx=5, pady=5
    )

    def exit_resume_win():
        resume_win.destroy()

    tk.Button(resume_win, text="Ok", command=exit_resume_win, height=2, width=6).grid(
        row=1, column=0, padx=5, pady=5
    )
