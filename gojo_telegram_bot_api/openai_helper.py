import openai
import json
import function_definitions as func
import os
from dotenv import load_dotenv
import helper_functions as helper

load_dotenv()

openai.api_key = os.getenv('OPENAI_TOKEN')

system_file = open("system_message.txt", "r")
system_message = system_file.read()

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "Don’t justify your answers. Don’t give information not mentioned in the CONTEXT INFORMATION."},
    {"role": "assistant", "content": "Sure! I will stick to all the information given in the system context. I won’t answer any question that is outside the context of information. I won’t even attempt to give answers that are outside of context. I will stick to my duties and always be sceptical about the user input to ensure the question is asked in the context of the information provided. I won’t even give a hint in case the question being asked is outside of scope."}
]

functions = func.function_definitions

available_functions = {"get_listings": helper.get_listivo_listings, "add_listing": helper.add_listing_to_sheet }

def get_reply(telegram_messages):
    temp_messages = messages + telegram_messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = temp_messages,
        functions = functions,
        function_call = 'auto'
    )

    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(function_args)
        temp_messages.append(response_message)
        temp_messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response
        })

        second_response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0613",
            messages = temp_messages
        )

        return second_response["choices"][0]["message"].get("content")
    return response_message.get("content")