import json
import openai

class TripPlannerBot():

    def __init__(self) -> None:

        # const
        CONFIG_PATH = "./config/config.json"
        SYSTEM_CONTENT_PATH = "./system_content.txt"

        # Load config
        json_file = open(CONFIG_PATH, "r")
        config = json.load(json_file)

        # Load system content
        system_content_file = open(SYSTEM_CONTENT_PATH, "r", encoding="UTF-8")
        system_content = system_content_file.read()

        # Load API key
        openai.api_key = config["api_key"]["chatgpt"]

        # Init messages
        self.messages = [
                {"role": "system", "content": system_content}
            ]
    

    def get_res(self, user_messages = None) -> str:

        # Insert messages
        if user_messages != None:
            self.messages = user_messages

        # Get responsea
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            messages = self.messages
        )

        # Return res
        return f"ChatGPT: {response['choices'][0]['message']['content']}"
    

    def add_user_message(self, user_res):

        self.messages.append({"role": "user", "content": user_res})
        return self.messages
    

    def add_planner_message(self, planner_res):
        
        self.messages.append({"role": "assistant", "content": planner_res})
        return self.messages


def main() -> None:
    
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
        messages = trip_planner.add_user_message(user_res=user_res)

        # Planner
        planner_res = trip_planner.get_res()
        print("<TripPlanner>")
        print(planner_res)
        messages = trip_planner.add_planner_message(planner_res=planner_res)
        

if __name__ in "__main__":
    main()