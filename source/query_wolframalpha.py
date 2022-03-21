import wolframalpha


def query(question: str):
    app_id = "6QLE9Y-R347K3E3HV"
    client = wolframalpha.Client(app_id)

    response = client.query(question)
    answer = next(response.results).text
    print(answer)
    return answer

