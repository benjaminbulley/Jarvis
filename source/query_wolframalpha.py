import wolframalpha


def query(q: str):
    app_id = "6QLE9Y-R347K3E3HV"
    client = wolframalpha.Client(app_id)

    response = client.query(question)
    answer = next(response.results).text
    print(answer)
    return answer


# query("lifespan of a mosquito")

# import logging
# from pprint import pprint
# import requests
# import os
# import urllib.parse
# import sys
#
# logger = logging.getLogger(__name__)
#
#
# def query_wolfram(q: str):
#     app_id = os.getenv("WA_APPID", "VURUPU-UR8UKWRVE8")
#     print(app_id)
#
#     query = urllib.parse.quote_plus(q)
#
#     print(query)
#
#     query_url = f"http://api.wolframalpha.com/v2/query?" \
#                 f"appid={app_id}" \
#                 f"&input={query}" \
#                 f"&format=plaintext" \
#                 f"&output=json"
#
#     print("query url", query_url)
#     try:
#         r = requests.get(query_url).json()
#         print("r", r)
#     except KeyError as ex:
#         logging.error(ex)
#         sys.exit('Invalid AppID')
#
#     if r["queryresult"]["numpods"] == 0:
#         error = r["queryresult"]["error"]
#         logging.error(error)
#     else:
#         data = r["queryresult"]["pods"][0]["subpods"][0]
#         datasource = ", ".join(data["datasources"]["datasource"])
#         microsource = data["microsources"]["microsource"]
#         plaintext = data["plaintext"]
#         print(f"Result: '{plaintext}' from {datasource} ({microsource}).")


question = "lifespan of a mosquito"
query_wolfram(question)
