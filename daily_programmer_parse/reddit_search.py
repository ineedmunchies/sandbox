import requests 
import time 
import pickle

url = 'http://www.reddit.com/r/dailyprogrammer/search.json'
payload = {'q':'dailyprogrammer', 'sort':'new', 'limit':'100'}
reddit_data = []

def run_request(url, payload):
    r = requests.get(url, params=payload)
    return r.json()


def parse_request(data):
    if len(data['data']['children']) == 0:
        return False
    else:
        for item in data['data']['children']:
            name = item['data']['name']
            reddit_data.append(item['data'])
    # Set the 'after' parameter so the next search returns results after the
    # last post found.
        payload['after'] = name
        return True

def main():
    while parse_request(run_request(url, payload)):
        time.sleep(3)
    outputfile = open("reddit.pickle", 'w')
    pickle.dump(reddit_data, outputfile)
    outputfile.close()

if __name__ == '__main__':
    main()
