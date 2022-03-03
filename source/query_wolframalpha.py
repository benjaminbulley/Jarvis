import wolframalpha

question = "WHat time is it in New York?"


def query(question):
    app_id = "6QLE9Y-R347K3E3HV"
    client = wolframalpha.Client(app_id)

    response = client.query(question)
    answer = next(response.results).text
    print(answer)
    return answer


query(question)
