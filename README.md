# # InfiniVision
 
Text-to-Image Generator

# 1.	Introduction
InfiniVision is a text-to-image generator utilizing the OpenAI's GPT-3 and DALL-E models. Flask framework is used for web development. Users can enter to input text descriptions and receive corresponding images generated based on those descriptions as it would seem 20 years later. The app also has voice recording feature for a more user-interactive experience.

# 2.	Setup Instructions
Python 3.8 or higher and pip (Python package installer) are prerequsities for the project. Ensure you have these software installed on your system. Then, follow the instructions below:

         1.	Clone the repository
         The github repository link: https://github.com/elisturegun/InfiniVision.git
         You need to get a copy of the project repository. Open your command prompt and run the following commands:
                  git clone https://github.com/elisturegun/InfiniVision.git
                  cd InfiniVision
         Create necessary directories: Ensure that the necessary directories exist for storing generated images. Run the following command to create the static directory:
                  mkdir -p static
         In static folder, generated_image.png file will be created after an image is generated.
         
         2.	Install Dependencies
         The project has several dependencies listed in the requirements.txt file. You can install them using pip. In the terminal, run:
                  pip install -r requirements.txt
                  
         3.	Setup API Keys
         You need an API key to use openai models. Follow these steps to work with your API key:
                  a)	Get an API Key: Obtain your API key from openai website:
                           https://openai.com/index/openai-api/
                           
                  b)	Configure the API Key: Open app.py file in a text editor and replace the placeholder with your actual API key:
                           openai.api_key = 'your_openai_api_key'

         4.	Execution Instructions
         You can start the Flask application. In your terminal, make sure you are in the project directory and execute:
                  python app.py
                  
         5.	Access The Application
         Once the application is running, open your web browser and navigate to:
                  http://127.0.0.1:5000

# 3.	Explanation of Directory Structure
         static/: 
         a.	generated_image.png: This file will be created dynamically after an image is generated and removed when redirecting to index.html
         
         templates/: 
         b.	index.html: The main page where users can enter text descriptions or use voice input to describe a scene to see 20 years later.
         
         c.	loading.html: The loading page displayed while the the generate image button is clicked on index page.
         
         d.	result.html: The result page is seen when image generation is completed. The page displays the generated image with options to download or create a new image.
         
         app.py: The main application file that sets up the Flask server and defines the routes and functions for handling requests.
         
         requirements.txt: A file listing all the dependencies required for the project. This can be used to install the necessary packages using pip.
         
         README.md: The detailed documentation of the project, including setup instructions, usage instructions, and more.

# 4.	Usage Instructions
         Text Input
                  1.	Enter a text description of the scene you want to generate in the text input field.
                  2.	Click on the "Generate Image" button.
                  3.	Wait for the image to be generated and displayed on the result page.
         Voice Input
                  1.	Ensure you are in a quiet and interrupted environment.
                  2.	Click on the microphone icon to start voice recognition.
                  3.	Speak your description clearly. Your voice will be recorded until silence.
                  4.	The recognized text will be filled into the text input field automatically.
                  5.	Edit the text input field if you want to.
                  6.	Click on the "Generate Image" button to generate the image.
                  7.	Wait for the image to be generated and displayed on the result page.
# 5.	Functionality
          Main Pages and Endpoints
                  Index Page (/)
                  •	Description: The main interface where users can enter text descriptions or use voice input to describe a scene.
                  •	Features:
                           o	Text input field
                           o	Voice input button
                           o	Submit button to generate an image
                  Loading Page (/loading)
                  •	Description: Displays a loading animation while the image is being generated.
                  •	Features:
                           o	Animated loading screen
                           o	Status check for image generation
                  Result Page (/result)
                  •	Description: Displays the generated image with options to download or create a new image.
                  •	Features:
                           o	Generated image display
                           o	Download button
                           o	Create new image button
         API Endpoints
         /generate (POST)
                  •	Description: Handles the text input from the user and initiates the image generation process.
                  •	Parameters:
                  o	text: The textual description provided by the user.
                  •	Response: JSON object indicating the status of the image generation.
         /status (GET)
                  •	Description: Checks the status of the image generation process.
                  •	Response: JSON object with the status and filename of the generated image if ready.
         /clear_image (GET)
                  •	Description: Clears the generated image and resets the system to accept new inputs.
                  •	Response: Redirects to the index page.
         /start_voice_recognition (GET)
                  •	Description: Starts the voice recognition procedure to get text input.
                  •	Response: JSON object with the transcribed text or error message.

# 6.	Performance Evaluation
The Infinivision demonstrates good performance in generating high-quality images from both text and voice inputs. The system's integration of advanced large language model GPT-3 and image generation model DALL-E supports a captivating user experience. Processing speed and handling detailed descriptions may be enhanced in the future to promote user satisfaction and system performance.




