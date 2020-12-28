import slack
import json
import requests

class SlackService:
    def __init__(self):
        pass

    def post_to_slack(self, message) -> None:
        webhook_url = 'https://hooks.slack.com/services/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'
        slack_data = '{"text": "' + message + '"}'
        response = requests.post(
            webhook_url, 
            data=slack_data.encode('utf-8'),
            headers={'Content-type': 'application/json'}
        )
        if response.status_code != 200:
            print(response.__dict__)
            print(slack_data)
            print('ERROR!')

if __name__ == '__main__':
    post_to_slack('hi')


