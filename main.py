import pyttsx3
import urllib.request
import requests
import docx
import webbrowser
from urllib.request import Request
from tkinter import filedialog, messagebox
from tkinter import *
from PyPDF2 import PdfFileReader
from bs4 import BeautifulSoup
from urllib.error import HTTPError

SPEED=150
VOLUME=0.5
VOICE=0
UNUSAVABLE_CHARECTORS = ['#', '%', '$', '<', '>', '+', '!', '`', '{', '}', '?', '"', '=', '/', '\\', ':', '@']

# Example color palettes can be found here
# https://colorhunt.co/palette/f2debaffefd60e5e6f3a8891
# Enter the RGB as a tuple in the variables below


#---------------------------- Dark Theme ---------------------------- 
# #Background Color
# BACK_GROUND_COLOR = (86, 91, 102)
# ENTRY_BACKGROUND_COLOR = (0, 0, 0)

# #Font Color
# LABEL_FONT_COLOR = (190, 190, 190)
# ENTRY_FONT_COLOR = (190, 190, 190)
# BUTTON_FONT_COLOR = (0, 0, 0)

# #Slider Color
# SLIDER_COLOR = (0, 0, 0)

# # Button Row 1
# OUTPUT_BUTTON_COLOR = (115, 95, 50)
# FILE_BUTTON_COLOR = (115, 95, 50)

# #Button Row 2
# CONVERT_WEBSITE_BUTTON_COLOR = (198, 151, 73)
# COVERT_FILE_BUTTON_COLOR = (198, 151, 73)
# TEST_VOICE_BUTTON_COLOR = (198, 151, 73)


#---------------------------- Light Theme ---------------------------- 
# Background Color
BACK_GROUND_COLOR = (242, 222, 186)
ENTRY_BACKGROUND_COLOR = (242, 222, 186)

#Font Color
LABEL_FONT_COLOR = (0, 0, 0)
ENTRY_FONT_COLOR = (0, 0, 0)
BUTTON_FONT_COLOR = (255, 255, 255)

#Slider Color
SLIDER_COLOR = (242, 222, 186)

# Button Row 1
OUTPUT_BUTTON_COLOR = (14, 94, 111)
FILE_BUTTON_COLOR = (14, 94, 111)

#Button Row 2
CONVERT_WEBSITE_BUTTON_COLOR = (58, 136, 145)
COVERT_FILE_BUTTON_COLOR = (58, 136, 145)
TEST_VOICE_BUTTON_COLOR = (58, 136, 145)


#---------------------------- Custom Theme ---------------------------- 
# # Background Color
# BACK_GROUND_COLOR = 
# ENTRY_BACKGROUND_COLOR = 
# #Font Color
# LABEL_FONT_COLOR = 
# ENTRY_FONT_COLOR = 
# BUTTON_FONT_COLOR = 

# #Slider Color
# SLIDER_COLOR = 

# # Button Row 1
# OUTPUT_BUTTON_COLOR = 
# FILE_BUTTON_COLOR = 

# #Button Row 2
# CONVERT_WEBSITE_BUTTON_COLOR = 
# COVERT_FILE_BUTTON_COLOR = 
# TEST_VOICE_BUTTON_COLOR = 

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb 


speak = pyttsx3.init()
voices = speak.getProperty('voices')

window = Tk()
window.title("PDF to MP3 Converter")
window.config(padx=50, pady=25, bg=_from_rgb(BACK_GROUND_COLOR))


canvas = Canvas(width=256, height=256, highlightthickness=0)
canvas.create_image(128, 128)


def pdf_to_text():
    input_file_path = file_input.get()

    with open(input_file_path,'rb') as f:
        pdf_read = PdfFileReader(f)
        page_content = ''
        for x in range(pdf_read.getNumPages()):
            page = pdf_read.getPage(x)
            page_content += page.extractText()
            
        return page_content

def docx_to_text():
    docx_file = file_input.get()
    doc = docx.Document(docx_file)
    completed_text = ""
    for paragraph in doc.paragraphs:
        completed_text+=paragraph.text
        
    return completed_text

def txt_to_text():
    input_file_path = file_input.get()
    with open(input_file_path, "r", encoding="utf-8") as f:
        page_content = ''
        for line in f.readlines():
            page_content += line
            
        return page_content
        
def text_to_mp3(text, mp3_name):
    mp3_output_path = output.get()
    output_path = mp3_output_path+"/"+mp3_name+".mp3"
   
    speak.setProperty('rate', SPEED)
    speak.setProperty('volume', VOLUME)
    speak.setProperty('voice', voices[VOICE].id)
    speak.save_to_file(text.replace("\n", " "), output_path)
    speak.runAndWait()
    speak.stop()

def website_to_text(url):
    try:
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        my_request = urllib.request.urlopen(req)
    
    except requests.exceptions.Timeout: 
        messagebox.showerror(title="Error", message="Website timed out. Please try again later")

    except requests.exceptions.HTTPError:
        messagebox.showerror(title="Error", message="There is an error with the website url or this website isn't currently supported")

    except requests.exceptions.InvalidSchema:
        messagebox.showerror(title="Error", message="There is an error with your link. Please check it and try again.")
        
    except HTTPError:
        messagebox.showerror(title="Error", message="This website is currently unsupported")
        
    else:
        my_HTML = my_request.read().decode("utf8")
        soup = BeautifulSoup(my_HTML, features='html.parser')
        #TODO Pull in Paragraph Headings
        p_tags = soup.find_all('p')
        website_text = ""
        for tag in p_tags:
            website_text+=(' '+tag.get_text())
        
        print(website_text)
        return website_text

def start_file_conversion():
    file = file_input.get()   
    print(file)
    file_type = file.split(".")[-1]
    print(file_type)
    mp3_name = file.split("/")[-1].split(".")[0]
    if UNUSAVABLE_CHARECTORS in mp3_name:
        mp3_name = 'untitled' 
    
    try:
        if file_type == "pdf":
            text = pdf_to_text()
        elif file_type == "docx":
            text = docx_to_text()
        elif file_type == "txt":
            text = txt_to_text()
        else:
            print("invalid file type")
            
        text_to_mp3(text=text, mp3_name=mp3_name)
            
        messagebox.showinfo(title="Confirmation", message=f"{mp3_name}.mp3 was Saved in the Target Location")
    except Exception as e:
        print(e)
        messagebox.showerror(title="Error", message="Please double check all fields and files")

def start_website_conversion():
    url = website_input.get()
    text = website_to_text(url=url)
    if url.split("/")[-1]:
        mp3_name = url.split("/")[-1]
    else:
        mp3_name = url.split("/")[-2]   
    text_to_mp3(text=text, mp3_name=mp3_name)
      
    messagebox.showinfo(title="Confirmation", message=f"{mp3_name}.mp3 was Saved in the Target Location")
      
def find_file():
    window.filename = filedialog.askopenfilename(initialdir= r".\Documents", title="Select a File", filetypes=(("PDF Files", "*.pdf"),("Word Documents", "*.docx"),("Text Documents", "*.txt")))
    file_input.delete(0,END)
    file_input.insert(0, string=window.filename)
    
def find_output_location():
    window.filename = filedialog.askdirectory()
    output.delete(0,END)
    output.insert(0, string=window.filename)
    
def test_voice():
    speak.setProperty('rate', SPEED)
    speak.setProperty('volume', VOLUME)
    speak.setProperty('voice', voices[VOICE].id)
    speak.say("This is a test of what your mp3 will sound like.")
    speak.runAndWait()
    speak.stop()

def voice_scale_used(value):
    global VOICE
    VOICE = int(value)
    
def speed_scale_used(value):
    global SPEED
    SPEED = int(value)*3

def volume_scale_used(value):
    global VOLUME
    VOLUME = int(value)/100
    
def callback(url):
   webbrowser.open_new_tab(url)

# UI Row 1
input_label = Label(text="File Location", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
input_label.grid(row=1, column=0)

output_label = Label(text="Output Folder", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
output_label.grid(row=1, column=1)

website_input_label = Label(text="Website", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
website_input_label.grid(row=1, column=2)

volume_label = Label(text="Volume", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
volume_label.grid(row=1, column=3)

speed_label = Label(text="Speed", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
speed_label.grid(row=1, column=4)

voice_label = Label(text="Voice", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR))
voice_label.grid(row=1, column=5)


# UI Row 2
file_input = Entry(width=30)
file_input.insert(END, string="File Path")
file_input.config(background=_from_rgb(ENTRY_BACKGROUND_COLOR), foreground=_from_rgb(ENTRY_FONT_COLOR))
file_input.grid(row=2, column=0)

output = Entry(width=30)
output.insert(END, string="Output Folder")
output.config(background=_from_rgb(ENTRY_BACKGROUND_COLOR), foreground=_from_rgb(ENTRY_FONT_COLOR))
output.grid(row=2, column=1)

website_input = Entry(width=30)
website_input.insert(END, string="Paste Website URL")
website_input.config(background=_from_rgb(ENTRY_BACKGROUND_COLOR), foreground=_from_rgb(ENTRY_FONT_COLOR))
website_input.grid(row=2, column=2)

volume_scale = Scale(from_=100, to=0, command=volume_scale_used, foreground=_from_rgb(LABEL_FONT_COLOR), highlightthickness=0, background=_from_rgb(BACK_GROUND_COLOR), troughcolor=_from_rgb(SLIDER_COLOR)) #, troughcolor=SLIDER_COLOR
volume_scale.set(VOLUME*100)
volume_scale.grid(row=2, column=3, rowspan=2)

speed_scale = Scale(from_=100, to=0, command=speed_scale_used, foreground=_from_rgb(LABEL_FONT_COLOR), highlightthickness=0, background=_from_rgb(BACK_GROUND_COLOR), troughcolor=_from_rgb(SLIDER_COLOR))
speed_scale.set(SPEED/3)
speed_scale.grid(row=2, column=4, rowspan=2)

voice_scale = Scale(from_=1, to=0, command=voice_scale_used, foreground=_from_rgb(LABEL_FONT_COLOR), highlightthickness=0, background=_from_rgb(BACK_GROUND_COLOR), troughcolor=_from_rgb(SLIDER_COLOR))
voice_scale.set(VOICE)
voice_scale.grid(row=2, column=5, rowspan=2)


# UI ROW 3
find_input = Button(text="Open File Location", command=find_file, width=25, fg=_from_rgb(BUTTON_FONT_COLOR), bg=_from_rgb(FILE_BUTTON_COLOR))
find_input.grid(row=3, column=0)

find_output = Button(text="Open Output Location", command=find_output_location, width=51, fg=_from_rgb(BUTTON_FONT_COLOR), background=_from_rgb(OUTPUT_BUTTON_COLOR))
find_output.grid(row=3, column=1, columnspan=2)


# UI Row 4
convert_file_button = Button(text="Convert File", command=start_file_conversion, width=51, fg=_from_rgb(BUTTON_FONT_COLOR), bg=_from_rgb(COVERT_FILE_BUTTON_COLOR))
convert_file_button.grid(row=4, column=0, columnspan=2)

convert_website_button = Button(text="Convert Website", command=start_website_conversion, width=25, fg=_from_rgb(BUTTON_FONT_COLOR), bg=_from_rgb(CONVERT_WEBSITE_BUTTON_COLOR))
convert_website_button.grid(row=4, column=2, columnspan=1)

test_voice_button = Button(text="Test Voice", command=test_voice, width=15, fg=_from_rgb(BUTTON_FONT_COLOR), bg=_from_rgb(TEST_VOICE_BUTTON_COLOR))
test_voice_button.grid(row=4, column=3, columnspan=3)


# UI Row 5
author_info = Label(text="Made by Panzhunter", fg=_from_rgb(LABEL_FONT_COLOR), bg=_from_rgb(BACK_GROUND_COLOR), cursor="hand2")
author_info.grid(row=5, column=3, columnspan=3)
author_info.bind("<Button-1>", lambda e:
    callback("github.com/Panzhunter"))

window.mainloop()