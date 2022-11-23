import pyttsx3
import urllib.request
import requests
import docx
from urllib.request import Request
from tkinter import filedialog, messagebox
from tkinter import *
from PyPDF2 import PdfFileReader
from bs4 import BeautifulSoup
from urllib.error import HTTPError

#TODO JSON to save settings, Clean up UI
SPEED=150
VOLUME=0.5
VOICE=0
#Creating a new window and configurations
speak = pyttsx3.init()
voices = speak.getProperty('voices')

window = Tk()
window.title("PDF to MP3 Converter")
window.config(padx=50, pady=25)


canvas = Canvas(width=256, height=256, highlightthickness=0)
canvas.create_image(128, 128) #, image=head_phone_image


#Labels
website_input_label = Label(text="Website")
website_input_label.grid(row=1, column=0)

input_label = Label(text="File Location")
input_label.grid(row=1, column=1)


output_label = Label(text="Output Folder")
output_label.grid(row=1, column=2)

volume_label = Label(text="Volume")
volume_label.grid(row=1, column=3)

speed_label = Label(text="Speed")
speed_label.grid(row=1, column=4)

voice_label = Label(text="Voice")
voice_label.grid(row=1, column=5)


#Entries
website_input = Entry(width=30)
website_input.insert(END, string="Enter Website URL")
website_input.grid(row=2, column=0)

file_input = Entry(width=30)
file_input.insert(END, string="Enter the path to your file")
file_input.grid(row=2, column=1)

output = Entry(width=30)
output.insert(END, string="Enter the output folder")
output.grid(row=2, column=2)

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
   
    # TODO Add speed, volume, and voices
    speed= SPEED
    volume=VOLUME
    voice=VOICE
    speak.setProperty('rate', speed)
    speak.setProperty('volume', volume)
    speak.setProperty('voice', voice[VOICE].id)
    speak.save_to_file(text.replace("\n", " "), output_path)
    speak.runAndWait()
    speak.stop()
    
#Buttons
def start_file_conversion():
    
    file = file_input.get()   
    print(file)
    file_type = file.split(".")[-1]
    print(file_type)
    mp3_name = file.split("/")[-1].split(".")[0]
    
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
    text = convert_website(url=url)
    if url.split("/")[-1]:
        mp3_name = url.split("/")[-1]
    else:
        mp3_name = url.split("/")[-2]
    # mp3_name = url.split("/")[-1]   
    text_to_mp3(text=text, mp3_name=mp3_name)
        
        
    messagebox.showinfo(title="Confirmation", message=f"{mp3_name}.mp3 was Saved in the Target Location")
    # except Exception as e:
    #     print(e)
    #     messagebox.showerror(title="Error", message="Please double check website and fields")
      
def convert_website(url):
    
    try:
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # response.raise_for_status()
        my_request = urllib.request.urlopen(req)
        # print(response)
    
    
    except requests.exceptions.Timeout: 
        messagebox.showerror(title="Error", message="Website timed out. Please try again later")

    except requests.exceptions.HTTPError:
        messagebox.showerror(title="Error", message="There is an error with the website url or this website isn't currently supported")

    except requests.exceptions.InvalidSchema:
        messagebox.showerror(title="Error", message="There is an error with your link. Please check it and try again.")
        
    except HTTPError as e:
        messagebox.showerror(title="Error", message="This website is currently unsupported")
        print(e)
        
    else:
        #TODO Clean this up so it doesn't have weird pauses
        my_HTML = my_request.read().decode("utf8")
        soup = BeautifulSoup(my_HTML, features='html.parser') #lxml
        p_tags = soup.find_all('p')
        website_text = ""
        for tag in p_tags:
            website_text+=tag.get_text()

            print(tag.get_text())
        return website_text



#dialog box in button
def find_file():
    window.filename = filedialog.askopenfilename(initialdir= r"C:\Users\Panzhunter\Documents\Projects\pdf to mp3", title="Select a File", filetypes=(("PDF Files", "*.pdf"),("Word Documents", "*.docx"),("Text Documents", "*.txt"))) #"C:/"
    file_input.delete(0,END)
    file_input.insert(0, string=window.filename)
    
def find_output_location():
    window.filename = filedialog.askdirectory()
    output.delete(0,END)
    output.insert(0, string=window.filename)
    
def test_voice():
    # speed=SPEED
    # volume=VOLUME
    # voice=VOICE
    speak.setProperty('rate', SPEED)
    speak.setProperty('volume', VOLUME)
    speak.setProperty('voice', voices[VOICE].id)
    speak.say("This is a test of what your mp3 will sound like.")
    speak.runAndWait()
    speak.stop()


#calls action() when pressed
find_input = Button(text="Open File Location", command=find_file, width=20)
find_input.grid(row=3, column=1)

find_output = Button(text="Open Output Location", command=find_output_location, width=20)
find_output.grid(row=3, column=2)

convert_file_button = Button(text="Convert File", command=start_file_conversion, width=50, bg='green')
convert_file_button.grid(row=4, column=1, columnspan=2)

convert_website_button = Button(text="Convert Website", command=start_website_conversion, width=20, bg='deep sky blue')
convert_website_button.grid(row=4, column=0, columnspan=1)

test_voice_button = Button(text="Test Voice", command=test_voice, width=20)
test_voice_button.grid(row=4, column=3, columnspan=3)


#Scale
#Called with current scale value.
def volume_scale_used(value):
    global VOLUME
    VOLUME = int(value)/100
volume_scale = Scale(from_=100, to=0, command=volume_scale_used)
volume_scale.set(VOLUME*100)
volume_scale.grid(row=2, column=3, rowspan=2)

def speed_scale_used(value):
    global SPEED
    SPEED = int(value)*3
speed_scale = Scale(from_=100, to=0, command=speed_scale_used)
speed_scale.set(SPEED/3)
speed_scale.grid(row=2, column=4, rowspan=2)

def voice_scale_used(value):
    global VOICE
    VOICE = int(value)
voice_scale = Scale(from_=1, to=0, command=voice_scale_used)
voice_scale.set(VOICE)
voice_scale.grid(row=2, column=5, rowspan=2)

window.mainloop()