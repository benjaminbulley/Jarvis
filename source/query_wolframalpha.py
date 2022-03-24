import requests
import logging
import urllib.parse

from player_logic import player_thread


def wolfram_query(question: str):
    formatted = urllib.parse.quote_plus(question)
    logging.debug("Formatted question: ", formatted)
    app_id = "6QLE9Y-R347K3E3HV"
    query_url = f"http://api.wolframalpha.com/v1/query?" \
             f"appid={app_id}" \
             f"&input={formatted}" \
             f"&format=plaintext" \
             f"&output=json"
    try:
        r = requests.get(query_url).json()
        data = r["queryresult"]["pods"][1]["subpods"][0]
        plaintext = data["plaintext"]

        logging.info("Wolfram said: ", data)
        print(plaintext)
        return plaintext
    except KeyError as k:
        logging.error("Wolfram did not understand")
        return player_thread("didnt_understand")
