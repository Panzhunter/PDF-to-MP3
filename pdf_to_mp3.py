import pyttsx3
from tkinter import filedialog, messagebox
from tkinter import *
from PyPDF2 import PdfFileReader


#Creating a new window and configurations
speak = pyttsx3.init()

window = Tk()
window.title("PDF to MP3 Converter")
window.config(padx=50, pady=25)


canvas = Canvas(width=256, height=256, highlightthickness=0)
head_phone_image = PhotoImage(file="./MISC/24001-2703046815.png")
canvas.create_image(128, 128, image=head_phone_image)
canvas.grid(row=0, column=0, columnspan=3)

#Labels
input_label = Label(text="PDF Folder")
input_label.grid(row=1, column=0)

output_label = Label(text="Output Folder")
output_label.grid(row=2, column=0)


#Entries
input = Entry(width=30)
input.insert(END, string="Enter the path to your pdf")
input.grid(row=1, column=1)

output = Entry(width=30)
output.insert(END, string="Enter the output folder")
output.grid(row=2, column=1)


#Buttons
def convert_to_mp3():
    
    input_path = input.get()
    mp3_output_path = output.get()
    mp3_name = input_path.split("/")[-1].split(".")[0]
    output_path = mp3_output_path+"/"+mp3_name+".mp3"
    
    try:
        with open(input_path,'rb') as f:
            pdf_read = PdfFileReader(f)
            page_content = ''
            for x in range(pdf_read.getNumPages()):
                page = pdf_read.getPage(x)
                page_content += page.extractText()
            speak.save_to_file(page_content.replace("\n", " "), output_path)
            speak.runAndWait()
            speak.stop()
        messagebox.showinfo(title="Confirmation", message=f"{mp3_name}.mp3 was Saved in the Target Location")
    except Exception as e:
        messagebox.showerror(title="Error", message="Please double check all fields and files")
        # print(e)
        

#dialog box in button
def find_file():
    window.filename = filedialog.askopenfilename(initialdir= r"C:\Users\Panzhunter\Documents\Projects\pdf to mp3", title="Select a File", filetypes=(("PDF Files", "*.pdf"),("Word Documents", "*.docx"))) #"C:/"
    input.delete(0,END)
    input.insert(0, string=window.filename)
    
def find_output_location():
    window.filename = filedialog.askdirectory()
    output.delete(0,END)
    output.insert(0, string=window.filename)
    
#calls action() when pressed
find_input = Button(text="Open File Location", command=find_file, width=30)
find_input.grid(row=1, column=2)

find_output = Button(text="Open Output Location", command=find_output_location, width=30)
find_output.grid(row=2, column=2)

convert_button = Button(text="Convert", command=convert_to_mp3, width=30)
convert_button.grid(row=3, column=0, columnspan=3)


window.mainloop()