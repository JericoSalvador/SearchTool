from tkinter import filedialog
import tkinter as tk
import os
import threading
import regex as re
import webbrowser

def main(): 
    root = tk.Tk()
    root.title("File Search")
    root.geometry("400x300")
    newApp = myApp(root)
    newApp.mainloop()

class myApp(tk.Frame): 
    def __init__(self, master=None): 
        super().__init__(master)
        self.searchButton = tk.Button(self, text= "Search!", command = self.asyncSearchDirectories)
        self.changeDirectoryButton = tk.Button(self, text="Change Directory", command = self.changeDirectory)
        
        self.currentDirectory = tk.StringVar()
        self.currentDirectory.set("cwd: "+os.getcwd())
        self.label = tk.Label(self, textvariable=self.currentDirectory)   
        self.entry = tk.Entry(self, text="re")
        self.listbox = tk.Listbox(self, width = 60, selectmode = tk.SINGLE)
        self.listbox.yview()
        self.listbox.xview()
        
        self.foldersIsChecked = tk.BooleanVar(value="False")
        self.foldersOption = tk.Checkbutton(self, text="Folder Name", variable=self.foldersIsChecked, onvalue=True, offvalue=False )
        
        self.fileNamesIsChecked = tk.BooleanVar(value="True")
        self.fileNamesOption = tk.Checkbutton(self, text="File Name", variable=self.fileNamesIsChecked, onvalue=True, offvalue=False)
        
        self.insideFilesIsChecked = tk.BooleanVar(value="False")
        self.insideFilesOption = tk.Checkbutton(self, text="Inside Files",variable=self.insideFilesIsChecked, onvalue=True, offvalue=False)
        
        self.status = tk.StringVar(value="")
        self.statusLabel = tk.Label(self, textvariable=self.status)
        
        self.grid()
        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)
        self.searchButton.grid(row=1, column=1)
        self.changeDirectoryButton.grid(row=0, column=1)
        self.foldersOption.grid(row=2, column=0)
        self.fileNamesOption.grid(row=2, column=1)
        self.insideFilesOption.grid(row=2, column=2)
        self.listbox.grid(row=3,columnspan = 3)
        self.statusLabel.grid(row=4, column=2)
        
        self.listbox.bind('<Double-Button-1>', self.openSelectedFile)   
        self.listbox.bind('<<ListboxSelect>>', self.createListItemButtons)
        
        self.SearchingThread = None 
        
    def changeDirectory(self): 
        newDir = filedialog.askdirectory()
        try: 
            os.chdir(newDir)
            self.currentDirectory.set("cwd: " + os.getcwd())
        except: 
            #print("Error: Directory Not set")
            pass
        
    def searchDirectories(self): 
        text = self.entry.get()
        pattern = re.compile(text)
        
        self.listbox.delete(0,tk.END)
        self.status.set("Searching...")
        for root, dirs, files in os.walk(os.getcwd()):
            if self.foldersIsChecked.get(): 
                for directory in dirs: 
                    if re.search(pattern, directory): 
                        path = os.path.join(root, directory)
                        self.listbox.insert(tk.END, path)
            if self.fileNamesIsChecked or self.insideFilesIsChecked:
                for file in files: 
                    filePath = os.path.join(root, file)
                    if self.fileNamesIsChecked.get(): 
                        if re.search(pattern, file): 
                            self.listbox.insert(tk.END, filePath)
                    if self.insideFilesIsChecked.get():
                        if self.searchFiles(pattern, filePath):
                            self.listbox.insert(tk.END, filePath)
        self.status.set("Done!")
                    
    def searchFiles(self, pattern, filename): 
        with open(filename, 'r') as fh: 
            try: 
                content = fh.read()
                return re.search(pattern, content)
            except:
                #print("problem reading ", filename)
                pass
        
    def openSelectedFile(self, event = None): 
        itemIndex = self.listbox.curselection()
        filePath = self.listbox.get(itemIndex)
        webbrowser.open_new(filePath)
        
    def openFileLocation(self, event = None): 
        itemIndex = self.listbox.curselection()
        filePath = self.listbox.get(itemIndex)
        dirPath = os.path.dirname(filePath)
        webbrowser.open_new(dirPath)
    
    def createListItemButtons(self, event = None):
        self.openFileButton = tk.Button(self, text = "Open File", command = self.openSelectedFile)
        self.openLocationButton = tk.Button(self, text = "Open Location", command = self.openFileLocation)
        
        self.openFileButton.grid(row = 4, column = 0)
        self.openLocationButton.grid(row=4, column = 1)
        
    def asyncSearchDirectories(self): 
        self.searchingThread = threading.Thread(target=self.searchDirectories, args = ())
        self.searchingThread.start()
                

if __name__ == "__main__": 
    main()