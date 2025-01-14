# Instalação dos pacotes necessários
!pip install SpeechRecognition
!pip install gTTS
!pip install playsound
!pip install wikipedia
!pip install geocoder
!pip install folium
!pip install python-dotenv
!pip install PyAudio
  
#Importação das Bibliotecas
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import webbrowser
import wikipedia
import geocoder
import datetime
import json
from threading import Thread
import time
  
#Implementação do Assistente Virtual
class VirtualAssistant:
    def __init__(self, name="Assistente"):
        self.name = name
        self.recognizer = sr.Recognizer()
        wikipedia.set_lang("pt")
        
    def text_to_speech(self, text, lang='pt'):
        """Converte texto em fala"""
        try:
            tts = gTTS(text=text, lang=lang)
            filename = 'voice.mp3'
            tts.save(filename)
            playsound.playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"Erro na conversão texto-fala: {str(e)}")

    def speech_to_text(self):
        """Captura áudio e converte para texto"""
        with sr.Microphone() as source:
            print("Ouvindo...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse")
            return ""
        except sr.RequestError:
            print("Erro na requisição ao serviço de reconhecimento")
            return ""

    def process_command(self, command):
        """Processa os comandos de voz"""
        if "pesquisar" in command:
            search_term = command.replace("pesquisar", "").strip()
            try:
                result = wikipedia.summary(search_term, sentences=2)
                self.text_to_speech(result)
            except:
                self.text_to_speech("Não encontrei informações sobre isso")

        elif "youtube" in command:
            self.text_to_speech("Abrindo YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "farmácia" in command:
            self.find_nearest_pharmacy()

        elif "horas" in command:
            current_time = datetime.datetime.now().strftime('%H:%M')
            self.text_to_speech(f"Agora são {current_time}")

    def find_nearest_pharmacy(self):
        """Encontra a farmácia mais próxima"""
        try:
            g = geocoder.ip('me')
            if g.ok:
                lat, lng = g.latlng
                self.text_to_speech(
                    f"Suas coordenadas são: latitude {lat:.2f}, longitude {lng:.2f}")
                webbrowser.open(
                    f"https://www.google.com/maps/search/farmacia/@{lat},{lng},15z")
            else:
                self.text_to_speech("Não foi possível determinar sua localização")
        except Exception as e:
            self.text_to_speech("Erro ao buscar localização")

    def run(self):
        """Executa o assistente virtual"""
        self.text_to_speech(f"Olá, eu sou {self.name}. Como posso ajudar?")
        
        while True:
            command = self.speech_to_text()
            
            if "sair" in command:
                self.text_to_speech("Até logo!")
                break
                
            if command:
                self.process_command(command)
  
#Exemplo de Uso
# Inicializa e executa o assistente virtual
if __name__ == "__main__":
    assistant = VirtualAssistant("Alice")
    assistant.run()
  
