import json
import openai

class TripPlannerBot():

    def __init__(self) -> None:

        # const
        CONFIG_PATH = "./config/config.json"
        SYSTEM_CONTENT_PATH = "./system_content.txt"
        SUGGESTION_FORMAT_PATH = "./suggestion_format.txt"

        # Load config
        json_file = open(CONFIG_PATH, "r")
        config = json.load(json_file)

        system_content_PATH = open(SYSTEM_CONTENT_PATH, "r", encoding="UTF-8")
        system_content = system_content_PATH.read()

        suggestion_format_file = open(SUGGESTION_FORMAT_PATH, "r", encoding="UTF-8")
        self.suggestion_format = suggestion_format_file.read()

        # Load API key
        openai.api_key = config["api_key"]["chatgpt"]

        # Init messages
        self.tokens = 0
        self.messages = [
                {"role": "system", "content": system_content}
            ]
    
    def get_res(self) -> str:

        # Get response
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            messages = self.messages
        )
        self.tokens += response['usage']['total_tokens']
        print(self.tokens)

        # Return res
        return f"ChatGPT: {response['choices'][0]['message']['content']}"
    
    def trip_planner(self, user_message):
        
        # Bot
        if len(self.messages) > 4:
            print("here")
            user_message += self.suggestion_format
        self.messages.append({"role": "user", "content": user_message})

        # Get res
        planner_res = self.get_res()
        print("<TripPlanner>")
        print(planner_res)
        
        self.messages.append({"role": "assistant", "content": planner_res})

        return planner_res

if __name__ in "__main__":
    TripPlannerBot().trip_planner("こんにちは、京都に行きたいです。")