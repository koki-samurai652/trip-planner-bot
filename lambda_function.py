import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

from TripPlannerBot import TripPlannerBot

# const
CONFIG_PATH = "./config/config.json"

# Load config
json_file = open(CONFIG_PATH, "r")
config = json.load(json_file)

# Load channel access token
channel_access_token = config["channel_access_token"]

# set channel access token
line_bot_api = LineBotApi(channel_access_token=channel_access_token)

# Main
def lambda_handler(event, context):

    # Init TripPlannerBot
    bot = TripPlannerBot()

    # Get res
    line_body = json.loads(event['body'])
    
    for linereq in line_body['events']:

        print(json.dumps(linereq))

        reply_token = linereq['replyToken']
        response_message = ''

        if 'text' in linereq['message']:

            message = linereq['message']['text']

            # Make response
            # response_message = str(type(message))
            response_message = bot.trip_planner(message)
            # print(messages)

            if response_message == '':
                response_message = 'メッセージが分かりませんでした。'
            
            # Return response
            print(response_message)
            try:
                line_bot_api.reply_message(reply_token, TextSendMessage(text=response_message))
            except LineBotApiError as e:
                print(e.error)

    return {
        'statusCode': 200
    }
