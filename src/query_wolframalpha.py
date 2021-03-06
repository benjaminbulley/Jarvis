"""
This is our knowledge API where we send queries and receives answers
"""
import requests
import logging
import urllib.parse

import player


def wolframalpha_query(question: str):
    """
    logic for what kind of audio is played
    :param question (str)- Question received from our user, converted to text by speech to text
    :returns plaintext (string) answer form wolfram
    """
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
        return player.player_thread_local("didnt_understand")  # singleton













































