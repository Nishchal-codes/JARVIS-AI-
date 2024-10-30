'''importing modules'''
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv 
import customtkinter as CTk
import webbrowser
import requests
import spotipy
import cohere
import os


#Loading up the credentials
load_dotenv("JARVIS\API_CREDENTIALS.env")

#asssigning variables
api_key = os.getenv("api_key")
weather_api_key=os.getenv("wapi_key")
client_id=os.getenv('client_id')
client_secret =os.getenv('client_secret')

redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read"))


invalid_command=   'open:play:'or'play:open:'or'open: play:'or'play: open:'


#HANDLEING CALLS
class ChatInterface:
    #creating chat window
    def __init__(self, root):
        self.chat_window = root
        self.chat_window.title("JARVIS")
        self.chat_window.geometry("600x600")
        
        self.chat_window.iconbitmap(r"JARVIS\jarvis_icon.ico")

        # creating Response Panel
        self.response_frame = CTk.CTkFrame(self.chat_window)
        self.response_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nsew')

        self.response_text = CTk.CTkTextbox(self.response_frame, wrap='word', state='normal')
        self.response_text.pack(padx=10, pady=10, fill='both', expand=True)

        self.query_frame = CTk.CTkFrame(self.chat_window)
        self.query_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        #creating inpu fields and managing inputs
        self.input_field = CTk.CTkEntry(
            self.query_frame, placeholder_text='MESSAGE JARVIS',
            placeholder_text_color='gray', height=7, width=400
            )
        
        self.input_field.pack(side='left', padx=10, fill='x', expand=True)

        self.input_field.bind("<Return>", self.on_enter)
        #creating and handleing submit buttons
        self.submit_button = CTk.CTkButton(self.query_frame, text="Submit", command=self.process_query)
        self.submit_button.pack(side='right', padx=10)

        self.chat_window.grid_rowconfigure(0, weight=1)
        self.chat_window.grid_rowconfigure(1, weight=0)
        self.chat_window.grid_columnconfigure(0, weight=1)

        self.status_label = CTk.CTkLabel(self.response_frame, text="")
        self.status_label.pack(padx=10, pady=(5, 10), anchor='w')

    '''CREATING LOGICS FOR CHAT INTERFACE'''

    def on_enter(self, event):
        self.process_query() # force submits the input


    def process_query(self):
        query = self.get_query_text()  

        if not query.strip():
            self.display_text_animation("Error: Query cannot be empty!", "JARVIS")
            return

        self.clear_input_field() 

        self.display_text_animation(query, "You", delay=40)

        self.chat_window.after(2000, lambda: self.animate_jarvis_response(query))

    def get_query_text(self):
      
        return self.input_field.get().strip()  

    def clear_input_field(self):
        
        self.input_field.delete(0, 'end')  


    def conversation(self, query):
        query=query.lower()      
        #handeling the task
        if 'weather' in query:
            city = 'Raipur'
            url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                return('''HAVING TROUBLE FETCHING DATA..\n  PLEASE CHECK YOUR INTERNET CONNECTION''')
            else:
                weather_result = data['current']['condition']['text']
                temperature = data['current']['temp_c']
                return(f"The weather in {city} is {weather_result} with a temperature of {temperature}  degreesCelsius\n")
        elif invalid_command in query:
            return('''Invalid command. Please try again''')
        elif "open:" in query :
            query=query.replace("open:","")
            url=query+".com"
            try:
                webbrowser.open(url)
                return "OPENING THE SITE"
            except webbrowser.Error as e:
                self.display_text_animation("","UNABLE TO OPEN SITE ,; TRY PROVIDING SOME ACTUAL LINK",delay =50)
                self.display_text_animation(e,"Jarvis:",delay =50)
                
                try:
                    query=self.get_query_text()
                    webbrowser.open(query)
                except Exception as e :
                    return("ERROR OCCURED WHILE OPENING SITE TRY RECHECKING YOUR INTERNET CONNECTION OR TRY AGAIN LATER :")
        elif 'play:' in query:
            try:
                query=query.replace('play:',"")
                results = sp.search(q=query, type='track')           
                track_url = results['tracks']['items'][0]['external_urls']['spotify']
                webbrowser.open(track_url)            
                
            except webbrowser.Error as e :
                return e
        else:
            co = cohere.Client(api_key)
            try:
                response = co.generate(
                    model='command', 
                    prompt=query,
                    return_likelihoods='GENERATION'
                )
                generated_text = response.generations[0].text.strip()  
                return generated_text
            except Exception as e:
                return f"Error: {str(e)}" 
        
    def animate_jarvis_response(self, query):
        response = self.conversation(query)
        if 'play:'not in  query:
            
            if response is not None:
                self.display_text_animation(response, "JARVIS", delay=50)
            else:
                self.display_text_animation("Sorry, I'm having trouble understanding you. Please try again.", "JARVIS", delay=50)
        else:
            None
    def display_text_animation(self, text, prefix, delay=100, callback=None):

        self.response_text.insert('end', f"{prefix}: ")
        self.response_text.see('end')

        def animate_characters(i):
            if i < len(text):
                self.response_text.insert('end', text[i])
                self.response_text.see('end')
                self.response_text.after(delay, animate_characters, i + 1)
            else:
                self.response_text.insert('end', "\n\n") 
                if callback:
                    callback()

        animate_characters(0)

'''------------\end-----------'''