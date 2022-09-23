#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import uuid
from time import sleep


# Bearer token from your developer portal
BEARER_TOKEN = '<<<YOUR_BEARER_TOKEN_HERE>>>'
# tweets search query string
QUERY_STRING = '<<<YOUR_QUERY_HERE>>>'

# URL of twitter api v2 endpoint
SEARCH_URL = 'https://api.twitter.com/2/tweets/search/recent'

# Twitter GET request query parameters
query_params = {
    'query': QUERY_STRING,
    'max_results': 100,
    'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
    'expansions': 'attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id',
    'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
    'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
}

def create_headers(bearer_token):
    headers = {'Authorization': 'Bearer {0}'.format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params):
    response = requests.request('GET', url, headers=headers,
                                params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def print_batch(old_id, new_id, delta, batch):
    print('------------ Batch {0} ------------\nOldest ID: {1}\nNewest ID: {2}\nTweets count: {3}'.format(batch, old_id, new_id, delta))

def get_tweets():
    
    start_time = time.time()
    headers = create_headers(BEARER_TOKEN)
    json_response = connect_to_endpoint(SEARCH_URL, headers, query_params)

    file_name = '{0}.json'.format(str(uuid.uuid4().hex))
    
    json_file = open(file_name, mode='w')
    json_file.write('[')
    json_file.writelines(json.dumps(json_response['data'])[1:-1])
    
    batch_num = 1
    tweets_counter = 0
    
    tweets_counter += json_response['meta']['result_count']
    print_batch(json_response['meta']['oldest_id'], json_response['meta']['newest_id'], tweets_counter, batch_num)

    try:
        while json_response['meta']["next_token"]:
            sleep(2)
            query_params['next_token'] = json_response['meta']["next_token"]
            json_response = connect_to_endpoint(SEARCH_URL, headers, query_params)
            
            json_file.writelines("," + json.dumps(json_response['data'])[1:-1])
    
            batch_num += 1
            tweets_counter += json_response['meta']["result_count"]
            print_batch(json_response['meta']["oldest_id"], json_response['meta']['newest_id'], tweets_counter, batch_num)
            
            if 'next_token' not in json_response['meta']:
                break;
    except KeyError:
        print('No nex_token in json response.')

    json_file.writelines("]")
    json_file.close()
    
    print('---------------------------------\n *** End of search. Execution time is {0:.3f}s.\nFile saved as {1} ***'.format((time.time() - start_time), file_name))

if __name__ == "__main__":
    get_tweets()