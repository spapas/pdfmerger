import tkinter as tk
from pypdf import PdfWriter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinterdnd2 import DND_FILES, TkinterDnD

root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()
root.geometry("800x600")
root.title("PDF Merger")
root.maxsize(800, 800)

pdf_filetypes = (("PDF files", "*.pdf"), )


def drop_files(event):
    filenames = root.tk.splitlist(event.data)
    for f in filenames:
        if f.lower().endswith(".pdf"):
            lb.insert(tk.END, f)


class DragDropListbox(tk.Listbox):
    """A Tkinter listbox with drag'n'drop reordering of entries."""

    def __init__(self, master, **kw):
        kw["selectmode"] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind("<Button-1>", self.setCurrent)
        self.bind("<B1-Motion>", self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


lb = DragDropListbox(root, width=100)
lb.grid(row=0, column=0, padx=5, pady=5, rowspan=3)
tk.Label(root, text="Drop PDFs here", font=("Helvetica", 16)).grid(
    row=3, column=0, padx=5, pady=5
)
lb.drop_target_register(DND_FILES)
lb.dnd_bind("<<Drop>>", drop_files)


def select_files():
    filenames = fd.askopenfilenames(
        title="Open files", initialdir=".", filetypes=pdf_filetypes
    )

    for f in filenames:
        lb.insert(tk.END, f)


def merge_pdfs():
    items = lb.get(0, tk.END)

    if len(items) < 2:
        showinfo(title="Error", message="Please select at least 2 files to merge")
        return

    output = fd.asksaveasfilename(
        title="Save file as",
        defaultextension=".pdf",
        initialdir=".",
        filetypes=pdf_filetypes,
    )
    if not output:
        showinfo(title="Error", message="Select output file")
        return

    merger = PdfWriter()

    for pdf in items:
        merger.append(pdf)

    merger.write(output)
    merger.close()

    showinfo(
        title="Done!",
        message="OK, {} files merged on: {}".format(len(items), output),
    )


open_button = ttk.Button(root, text="Open Files", command=select_files)
open_button.grid(row=0, column=1, padx=5, pady=5)

merge_button = ttk.Button(root, text="Merge PDFs", command=merge_pdfs)
merge_button.grid(row=1, column=1, padx=5, pady=5)


def clear_listbox():
    lb.delete(0, tk.END)


clear_button = ttk.Button(root, text="Clear selection", command=clear_listbox)
clear_button.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
