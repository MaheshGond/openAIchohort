# import openai
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
#
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is recursion?"}
#     ]
# )
# print(response.choices[0].message.content)


from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()  # Make sure this runs first

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

print("Loaded Account SID:", account_sid)  # For debugging, remove later

client = Client(account_sid, auth_token)
