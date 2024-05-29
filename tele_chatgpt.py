import openai

# Set your API key directly
API_KEY = "**************************************"
openai.api_key = API_KEY

output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content":
               "clearly explain with example and convert the following text into the Bilingual telugu" + "text" }]
)

#explain the concept the following text and elaborate it with the example if possible.

# Print out the whole output dictionary
#print(output)

# Get the output text only
print(output['choices'][0]['message']['content'])
