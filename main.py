import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


home_body = """
<style>
    div {{ display: flex; flex-direction: column; align-items: center; }}

    p {{
        color: #333;
        max-width: 400px;
        text-align: center;
    }}

    a {{
        text-decoration: none;
        color: #00aaee;
        max-width: 400px;
        text-align: center;
    }}

    a:hover {{ text-decoration: underline; }}
</style>
<div>
    <h3>Original Fact:</h3>
    <p>{fact}</p>
    <h3>Latinized Fact:</h3>
    <a href='{latin_fact_url}'>{latin_fact}</a>
</div>
"""


def get_fact():
    """ Returns a random fact retrieved using requests and BeautifulSoup. """
    url = "http://unkno.com"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    fact = soup.find_all("div", id="content")[0].getText()

    return fact


def fact_to_latin(fact):
    """
    Takes a random fact and passes it to pig latinizer returning the pig
    latinized fact as a string.
    """

    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    form_data = {"input_text": fact}

    r = requests.post(url, data=form_data)
    latin_fact_url = r.url
    soup = BeautifulSoup(r.content, 'html.parser')

    # print(soup)
    latin_fact = soup.find("h2").next_element.next_element.strip()

    return latin_fact_url, latin_fact


@app.route('/')
def home():
    # return "FILL ME!"
    fact = get_fact()
    latin_fact_url, latin_fact = fact_to_latin(fact)

    # print(fact)

    return home_body.format(fact=fact, latin_fact_url=latin_fact_url, latin_fact=latin_fact)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port, debug=True)

