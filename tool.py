#!/usr/bin/env python3.11

import os
import tkinter as tk
import xlrd
import webbrowser
import hashlib
import urllib.request

class App(tk.Tk):
    def __init__(self):
         
        super().__init__()
        self.title("[*T*O*O*L*]")
        self.geometry("475x250")
        self.resizable(True, True)
        self.code = ""
        self.columnconfigure(2,minsize=5)
        #self.configure(bg='gray')
    # Labels for file check status
        menubar= tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
       
        menubar.add_cascade(label="File", menu=file_menu) 
        file_menu.add_command(label="Update Appendix K", command=self.update_appendixK)
        file_menu.add_separator()
        file_menu.add_command(label="Hash", command=self.hash_file)
        file_menu.add_separator()
        
        file_menu.add_command(label="<Exit>", command=self.quit)
    # Search bar and suggestions listbox
        self.search_label = tk.Label(self, text="Search:")
        self.search_label.grid(column=0, row=2, sticky="E")

        self.search_entry = tk.Entry(self, width=60)
        self.search_entry.grid(column=1, row=2, sticky="E")

        self.phrases_listbox_label = tk.Label(self, text="Suggestions:")
        self.phrases_listbox_label.grid(column=0, row=3,  sticky="E")

        self.phrases_listbox = tk.Listbox(self, height=5, width=60)
        self.phrases_listbox.grid(column=1, row=3, sticky="E")
        
        self.phrases_listbox_scrollbar = tk.Scrollbar(self)
        self.phrases_listbox_scrollbar.grid(column=3, row=3, sticky="ns")

        self.phrases_listbox.config(yscrollcommand=self.phrases_listbox_scrollbar.set)
        self.phrases_listbox_scrollbar.config(command=self.phrases_listbox.yview)

    # Selected phrase and row index display
                 
        self.selected_phrase_label = tk.Label(self, text="Offense Title:")
        self.selected_phrase_label.grid(column=0, row=4, sticky="E")

        self.selected_phrase_entry = tk.Entry(self, width=60)
        self.selected_phrase_entry.grid(column=1, row=4, sticky="E")
    # Code textbox and exit button
        self.code_label = tk.Label(self, text="Code")
        self.code_label.grid(row=6, column=0, sticky = "w")

        self.code_textbox = tk.Entry(self, width = 20)
        self.code_textbox.grid (row=6, column=1 ,sticky="w")

        self.statute_label = tk.Label(self, text = "Statute")
        self.statute_label.grid(row=7, column=0, sticky = "w")
        
        self.statute_textbox = tk.Entry(self, width = 20)
        self.statute_textbox.grid (row=7, column=1, sticky="w") 
        
        self.citation_label = tk.Label(self, text = "Citation")
        self.citation_label.grid(row=8, column=0, sticky = "w")
        
        self.citation_textbox = tk.Entry(self, width=20)
        self.citation_textbox.grid (row=8, column=1, sticky="w")

        level_degree_label = tk.Label(self, text = "Level/Degree")
        level_degree_label.grid(row=9, column=0, sticky = "w")


        self.level_degree_textbox = tk.Entry(self,width = 20)
        self.level_degree_textbox.grid (row=9, column=1, sticky="w")
        
        self.process_button = tk.Button(self, text=">>Read It<<", command=self.process_information)
        self.process_button.grid(row=6, column=1)       

    # Check if files exist and bind functions to events
        self.check_files()
        self.search_entry.bind("<KeyRelease>", self.populate_listbox)
        self.phrases_listbox.bind("<<ListboxSelect>>", self.select_phrase)
    def about_me (self):
        # create a new window to display the hashes
        about_window = tk.Toplevel(self)
        about_window.title("About Ra0013")

    
    def open_link(self):
        url =('https://github.com/ra0013/TexasOffenses')
        webbrowser.open_new(url)      

    def hash_file(self):
        file_path = "appendixk.xls"
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        hashed_value = hashlib.sha1(file_bytes).hexdigest()
        hash_md5 = hashlib.md5(file_bytes).hexdigest()  # calculate the MD5 hash

        # create a new window to display the hashes
        hash_window = tk.Toplevel(self)
        hash_window.title("Appendix K Hash Values")

        # create a Text widget to display the hashes
        hash_text = tk.Text(hash_window, height=2, width=50)
        hash_text.pack()

        #  insert the hashed values into the Text widget
        hash_text.insert(tk.END, f"SHA-1: {hashed_value}\nMD5: {hash_md5}")
    def update_appendixK(self):
        #url="https://www.dps.texas.gov/administration/crime_records/docs/cjis/v18offenseCodes.xls"
        url="https://www.dps.texas.gov/administration/crime_records/docs/cjis/v19offensecodes.xls"
        filename="appendixk.xls" 
        urllib.request.urlretrieve(url,filename)
        
    def check_files(self):
        appendixk_file = "appendixk.xls"
        if os.path.exists(appendixk_file):
            with open(appendixk_file, 'rb') as f:
                hasher = hashlib.sha1()
                hasher2 = hashlib.md5()
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    hasher.update(chunk)
                    hasher2.update(chunk)
            sha1_hash = hasher.hexdigest()
            md5_hash = hasher2.hexdigest()

    def populate_listbox(self, event):
        
        appendixk_file = "appendixk.xls"
        if os.path.exists(appendixk_file):
            workbook = xlrd.open_workbook(appendixk_file)
            worksheet = workbook.sheet_by_index(0)
        phrases = [worksheet.cell_value(row, 1) for row in range(2,worksheet.nrows)] #skipping the first two rows
        filter_text = self.search_entry.get().lower()
        filtered_phrases = [phrase.strip() for phrase in phrases if filter_text in phrase.lower()]
        self.phrases_listbox.delete(0, tk.END)
        for phrase in filtered_phrases:
            self.phrases_listbox.insert(tk.END, phrase)
        

    def select_phrase(self, event):
        selection = self.phrases_listbox.curselection()
        if selection:
            index = int(selection[0])
            phrase = self.phrases_listbox.get(index)
            self.selected_phrase_entry.delete(0, tk.END)
            self.selected_phrase_entry.insert(0, phrase)
            appendixk_file = "appendixk.xls"
            if os.path.exists(appendixk_file):
                workbook = xlrd.open_workbook(appendixk_file)
                worksheet = workbook.sheet_by_index(0)
                for row_idx in range(1, worksheet.nrows):
                    if worksheet.cell_value(row_idx, 1) == phrase:
                        row_values = worksheet.row_values(row_idx)
                        code = row_values[0]
                        citation = row_values[2]
                        statute = row_values[3]
                        level_degree = row_values[4]

                        self.code_textbox.delete(0, tk.END)
                        self.code_textbox.insert(0, code)
                         
                        self.statute_textbox.delete(0,tk.END)
                        self.statute_textbox.insert(0,statute)

                        self.citation_textbox.delete(0,tk.END)
                        self.citation_textbox.insert(0,citation)
                        self.level_degree_textbox.delete(0,tk.END)
                        self.level_degree_textbox.insert(0,level_degree)
                        break
 
    def process_information(self):
        # Process your previously obtained information here
        code = self.code_textbox
        OffenseTitle = self.phrases_listbox.curselection()
        Citation = self.citation_textbox.get()
        Statute = self.statute_textbox.get()
        Level_degree = self.level_degree_textbox
        # Citation
        modcitation = Citation  # copies citation including subsections
       # finds the length of citation
        citationlength = len(modcitation) - 1
        whereisit = modcitation.find("(")  # finds the first occurance of paranthesis
        #modcitation = citation_entry.get() 
        if (whereisit > 0):
            modcitation = modcitation[:whereisit]  # takes just the chapter
            #  (removes numbers in parenthesis)
        else: # this block takes into account citations with no trailing subsections (ie: 22.01 (a)(1) -> 22.01 )
            whereisit = citationlength
        modcitation = modcitation[:whereisit]
       # copy modified citation(modcitation) into modcitation2 to continue manip
       # copies citation to remove the citation's decimal values
        modcitation2 = modcitation
        whereisit2 = modcitation2.find(".")  # finds the decimal point in modcitation2
       # copies modication only up to the decimal point
        modcitation2 = modcitation2[:whereisit2+1]
        match Statute:  # converts human readable to legislature website coded Statute
            case "PC":
                Statute = "PE"
            case "TRC":
                Statute = "TN"
            case "LGC":
                Statute     = "LG"
            case "PRC":
                Statute = "PR"
            case "PWC":
                Statute = "PW"
            case "FC":
                Statute = "FA"
            case "EC":
                Statute = "EL"
            case "HSC":
                Statute = "HS"
            case "FNC":
                Statute = "FI"
            case "NRC":
                Statute = "NR"
            case "OC":
                Statute = "OC"
            case "TRC":
                Statute = "TN"
            case "GC":
                Statute = "GV"
            case "AGC":
                Statute  = "AG"
            case "BCC":
                Statute = "BC"
            case "IC":
                Statute = "IN"
            case "HRC":
                Statute = "HR"
            case "EDC":
                Statute = "ED"
            case "ABC":
                Statute = "AL"
            case "VCS":
                Statute = "CV"
            case "TUC":
                Statute = "UT"
            case "BOC":
                Statute = "BO"
            case "LC":
                Statute = "LA"
            case "CCP":
                Statute = "CR"
            case "WC":
                Statute = "WA"

# webaddress block puts the address together after all manipulations in the legislature's chosen format
        webaddress = "http://www.statutes.legis.state.tx.us/docs/"
        
        webaddress += Statute
        webaddress += "/htm/"
        webaddress += Statute
        webaddress += "."
        webaddress += modcitation2
        webaddress += "htm"
        webaddress += "#"
        webaddress += modcitation
        webbrowser.open(webaddress)  
                     
if __name__ == "__main__":
    app = App()
    app.mainloop()
