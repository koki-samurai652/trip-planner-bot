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

        # Load system content
        system_content_file = open(SYSTEM_CONTENT_PATH, "r", encoding="UTF-8")
        system_content = system_content_file.read()

        # Load suggestion
        suggestion_format_file = open(SUGGESTION_FORMAT_PATH, "r", encoding="UTF-8")
        self.suggestion_format = suggestion_format_file.read()

        # Load API key
        openai.api_key = config["api_key"]["chatgpt"]

        # Init messages
        self.messages = [
                {"role": "system", "content": system_content}
            ]
    

    def get_res(self, user_messages = None, is_suggestion = False) -> str:

        # Insert messages
        if user_messages != None:
            self.messages = user_messages

        # Insert suggestion message
        if is_suggestion:
            if self.suggestion_format not in self.messages[0]["content"]:
                self.messages[-1]["content"] += self.suggestion_format
    
        # Get response
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            messages = self.messages
        )

        # Return res
        return f"ChatGPT: {response['choices'][0]['message']['content']}"
    

    def add_user_message(self, user_res, user_messages = None):

        if user_messages != None:
            self.messages = user_messages

        self.messages.append({"role": "user", "content": user_res})
        return self.messages
    

    def add_planner_message(self, planner_res, user_messages = None):
        
        if user_messages != None:
            self.messages = user_messages
                
        self.messages.append({"role": "assistant", "content": planner_res})
        return self.messages


def main() -> None:
    
    is_suggestion = False
    trip_planner = TripPlannerBot()
    messages = trip_planner.messages

    # Start message 
    print("プランナーと話して、旅行計画を立て見ましょう。q または quit で終了します。")
    print("*"*100)
    
    # Bot
    while True:
        
        # User
        user_res = input("<You>\n")
        if user_res == "q" or user_res == "quit":
            break
        if len(messages) >= 5:
            is_suggestion = True
        messages = trip_planner.add_user_message(user_res=user_res, user_messages=messages)

        # Planner
        planner_res = trip_planner.get_res(user_messages=messages, is_suggestion=is_suggestion)
        print("<TripPlanner>")
        print(planner_res)
        messages = trip_planner.add_planner_message(planner_res=planner_res, user_messages=messages)
        

if __name__ in "__main__":
    main()