import requests
import json



def offensive_classifier(image_url):  
    describe = {'url': image_url, 'models': 'nudity, offensive, gore', 'api_user': '133743064', 'api_secret': 'xA9h9Ny3DBzeLPSyKAFL'}
    r = requests.get('https://api.sightengine.com/1.0/check.json', params=describe)
    output = json.loads(r.text)

    probs = {'gore': '', 'offensive': '', 'safe_prob': ''}
    probs['gore'] = output['gore']['prob']
    probs['offensive'] = output['offensive']['prob']
    probs['safe_prob'] = output['nudity']['safe']

    return probs
