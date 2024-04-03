import speech_recognition as sr
import wikipedia
import pyttsx3
import requests

# Initializes the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
  """Speaks the given text using the text-to-speech engine."""
  engine.say(text)
  engine.runAndWait()

def listen():
  """Listens for user input and returns the recognized text."""
  with sr.Microphone() as source:
    print("Listening...")
    listener = recognizer.listen(source)
  try:
    recognized_text = recognizer.recognize_google(listener)
    return recognized_text.lower()
  except sr.UnknownValueError:
    print("Could not understand audio")
    return None
  except sr.RequestError as e:
    print(f"Request failed: {e}")
    return None

def get_info_wikipedia(query):
  """Fetches information from Wikipedia based on the user query and speaks it."""
  speak(f"Searching Wikipedia for {query}")
  try:
    info = wikipedia.summary(query, sentences=3)
    speak(info)
  except wikipedia.exceptions.DisambiguationError as e:
    speak(f"Wikipedia Disambiguation: {e}")
  except wikipedia.exceptions.PageError:
    speak("The page could not be found on Wikipedia.")

def get_info_api(query, api_url):
  """Fetches information from an external API and speaks it (if available)."""
  try:
    response = requests.get(api_url)
    data = response.json()
    # Process and speak the information from the API response (example)
    if query == "states":
      speak("Here are some Indian states:")
      for state in data:
        speak(state["name"])
    else:
      speak(f"Information about {query} retrieved from API.")
  except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    speak("An error occurred while fetching information.")

def get_info(query):
  """Checks for specific topics and uses Wikipedia or external API."""
  if query == "states":
    # Check for a reliable external API for Indian states
    api_url = "https://en.wikipedia.org/wiki/States_and_union_territories_of_India"
    if requests.get(api_url).status_code == 200:  # Check if API is reachable
      get_info_api(query, api_url)
    else:
      speak("Using Wikipedia for state information.")
      get_info_wikipedia("States of India")
  else:
    get_info_wikipedia(query)

def main():

  while True:
    query = listen()
    if query is None:
      continue
    if "exit" in query:
      speak("Thank you for using the chatbot. Goodbye!")
      break
    elif "india" in query:
      # Handle specific topics about India
      if "culture" in query:
        get_info("Indian culture")
      elif "states" in query:
        get_info(query)
      else:
        get_info_wikipedia(query)  # Use Wikipedia for general information
    else:
      speak("I can provide information about Indian culture or states. How can I help you?")

if __name__ == "__main__":
  speak(" Namaste! ,Welcome to the India Information Chatbot!")
  main()

