from email import message
from tkinter import Button, Entry, Label, Listbox, Menu, Scrollbar, Tk, filedialog, messagebox
from utils.afl_file import AFLFile
from utils.common_functions import file_read, to_int
from utils.csv_file import CSVFile

class Gui:
    appname='AFL File Editor'
    def __init__(self, master:Tk):
        self.master = master
        master.title(self.appname)
        w = 600 # width for the Tk root
        h = 530 # height for the Tk root
        # get screen width and height
        ws = master.winfo_screenwidth() # width of the screen
        hs = master.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        # set the dimensions of the screen 
        # and where it is placed
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.my_menu=Menu(self.master)
        master.config(menu=self.my_menu)
        self.file_menu = Menu(self.my_menu, tearoff=0)
        self.edit_menu = Menu(self.my_menu, tearoff=0)
        self.help_menu = Menu(self.my_menu, tearoff=0)

        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_afl)
        self.file_menu.add_command(label="Save", state='disabled',command=self.save_btn_action)
        self.file_menu.add_command(label="Save as...", state='disabled', command=self.save_as_btn_action)
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.my_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Create AFL from AFS", command=self.create_afl_from_afs)
        self.edit_menu.add_command(label="Export to CSV", state='disabled', command=self.export_to_csv)
        self.edit_menu.add_command(label="Import from CSV", state='disabled', command=self.import_from_csv)

        self.my_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Manual", command=self.manual)
        self.help_menu.add_command(label="About", command=self.about)

        self.files_lbl = Label(self.master, text="File list")
        self.files_lbx = Listbox(self.master, height = 31, width = 50, exportselection=False)
        self.files_sb = Scrollbar(self.master, orient="vertical") 
        self.files_sb.config(command = self.files_lbx.yview)
        self.files_lbx.config(yscrollcommand = self.files_sb.set)
        self.files_lbx.bind('<<ListboxSelect>>',lambda event: self.on_file_selected())
        self.file_name_lbl = Label(self.master,text="New file name")
        self.file_box = Entry(self.master, width=32, state='disabled')
        self.apply_btn = Button(self.master, text="Apply", state='disabled', command=self.on_apply_btn_click)
        self.clear_btn = Button(self.master, text="Clear", state='disabled', command=self.on_clear_btn_click)

        self.files_lbl.place(x=20, y=5)
        self.files_sb.place(x=0, y=30, height=500)
        self.files_lbx.place(x=17, y=30)
        self.file_name_lbl.place(x=350, y=30)
        self.file_box.place(x=350, y=60)
        self.apply_btn.place(x=400, y=90)
        self.clear_btn.place(x=460, y=90)

        # setting scrollbar command parameter 
        # to listbox.yview method its yview because
        # we need to have a vertical view
    def on_file_selected(self):
        if self.files_lbx.size() == 0:
            return 0
        # set the name to the entry box
        #
        self.file_box.delete(0,'end')
        self.file_box.insert(0,self.files_lbx.get(self.files_lbx.curselection()))

    def on_apply_btn_click(self):
        file_idx = self.files_lbx.get(0, "end").index(self.files_lbx.get(self.files_lbx.curselection()))
        self.afl_file.set_name(file_idx,self.file_box.get())
        self.reload_gui_items(file_idx)

    def on_clear_btn_click(self):
        self.file_box.delete(0,'end')

    def open_afl(self):
        filetypes = [
            ('text files', '*.AFL'),
            ('All files', '*.*')
        ]

        filename = filedialog.askopenfilename(
            title=f'{self.appname} Open a AFL file',
            initialdir='.',
            filetypes=filetypes)
        if filename == "":
            return 0
        self.afl_file = AFLFile()
        self.afl_file.from_afl(filename)
        self.reload_gui_items()

    def reload_gui_items(self,item_idx=None):
        self.file_menu.entryconfig("Save", state="normal")
        self.file_menu.entryconfig("Save as...", state="normal")
        self.edit_menu.entryconfig("Export to CSV", state="normal")
        self.edit_menu.entryconfig("Import from CSV", state="normal")
        self.files_lbx.delete(0,'end')
        self.files_lbx.insert('end',*self.afl_file.files)
        self.file_box.config(state='normal')
        self.apply_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        if item_idx!=None:
            # After we clic on the button we lost the item selection so with this we solve it
            self.files_lbx.select_set(item_idx)

    def save_btn_action(self):
        try:
            self.afl_file.save_file()
            messagebox.showinfo(title=self.appname,message=f"All changes saved at {self.afl_file.file_location}")
        except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=self.appname,message=f"Error while saving, error type={e}, try running as admin")

    def save_as_btn_action(self):
        try:
            save_as = filedialog.asksaveasfile(initialdir=".",title=self.appname, mode='wb', filetypes=([("All files", "*")]), defaultextension=".AFL")
            if save_as is None:
                return 0
            self.afl_file.save_file(save_as.name)
            messagebox.showinfo(title=self.appname,message=f"All changes saved at {self.afl_file.file_location}")
        except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=self.appname,message=f"Error while saving, error type={e}, try running as admin or saving into another location")

    def create_afl_from_afs(self):
        filetypes = [
            ('text files', '*.afs'),
            ('All files', '*.*')
        ]

        filename = filedialog.askopenfilename(
            title=f'{self.appname} Open a AFS file',
            initialdir='.',
            filetypes=filetypes)
        if filename == "":
            return 0
        nums_of_files = to_int(file_read(filename)[4:8])
        self.afl_file = AFLFile()
        self.afl_file.from_afs(nums_of_files,'')
        self.reload_gui_items()
        self.file_menu.entryconfig("Save", state="disabled")      
        messagebox.showinfo(title=self.appname,message="Operation finished!")  

    def export_to_csv(self):
        try:
            csv_file_location = filedialog.asksaveasfile(initialdir=".",title=self.appname, mode='wb', filetypes=([("All files", "*")]), defaultextension=".csv")
            if csv_file_location is None:
                return 0
            csv_headers = ["File ID", "File name"]
            csv_file = CSVFile(csv_file_location.name)
            csv_file.to_file(self.afl_file.files, csv_headers)
            messagebox.showinfo(title=self.appname,message=f"File save at {csv_file_location.name}")
        except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
            messagebox.showerror(title=self.appname,message=f"Error while saving, error type={e}, try running as admin or saving into another location")

    def import_from_csv(self):
        filetypes = [
            ('text files', '*.csv'),
            ('All files', '*.*')
        ]

        filename = filedialog.askopenfilename(
            title=f'{self.appname} Open a CSV file',
            initialdir='.',
            filetypes=filetypes)
        if filename == "":
            return 0
        csv_file = CSVFile(filename)
        csv_file_content = csv_file.load()
        for line in csv_file_content:
            self.afl_file.set_name(int(line[0]),line[1])
        self.reload_gui_items()

    def about(self):
        messagebox.showinfo(title=self.appname,message=
        """
        First of all thanks to Obocaman who created GGS and also AFL files to make it easier to us create maps for our AFS files.

        This is just a simple tool to edit the binary file and to map our stuff better, in future versions you will be able to:
        - Export as CSV
        - Import from CSV
        - Create an AFL file from a AFS file
        - Add more files into an existent AFL file
        """.replace('        ', ''))

    def manual(self):
        messagebox.showinfo(title=self.appname,message=
        r"""
        How to located AFL files?

        Your AFL files are located in: C:\Program Files or Program Files(x86)\Game Graphic Studio\dat\
        Remember to run GGS with admin rights to auto generate the AFL file if you don't and you're using win7 and later (win10)
        your files will be located in:
        C:\Users\YOUR_USERNAME\AppData\Local\VirtualStore\Program Files or Program Files(x86)\Game Graphic Studio\dat\
        GGS will create a file with a name like DEFAULT_XXXXX_FILES.AFL being XXXXX as the numbers of files inside your AFS file
        You can also rename some with GGS and try to open the file and see if your changes make effect
        
        How to use this tool?
        
        Easy! just select any file that you want to rename, at the textbox at your right just enter the name that you want
        for example unnamed_0.bin you can rename it to ball_mdl_000.bin
        then just clic on Apply button
        
        Now to save your changes just go to File -> Save or Save as... buttons
        
        Soon video tutorial...
        """.replace('        ', ''))

    def start(self):
        self.master.resizable(False, False)
        self.master.mainloop()

def main():
    Gui(Tk()).start()

if __name__ == "__main__":
    main()