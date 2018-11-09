# The MIT License (MIT)
#
# Copyright (c) 2018 Piotr Rogulski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging

import alexa_skill
import falcon
import requests

from alexa_skill.intents import BaseIntents
from alexa_skill.intents import BuildInIntents


buildin_intents = BuildInIntents(
    help_message='Say to Alexa: "tell me a joke"',
    not_handled_message="Sorry, I don't understand you. Could you repeat?",
    stop_message='stop',
    cancel_message='cancel',
)


class JokeIntents(BaseIntents):
    @property
    def mapper(self):
        return {'random_joke': self.random_joke}

    def random_joke(self):
        joke_response = requests.get('http://api.icndb.com/jokes/random')
        if joke_response.status_code != 200:
            return self.response('Sorry, I did not find any joke. Please try again'), False

        return self.response(joke_response.json()['value']['joke']), True


class Fulfiller(object):
    def on_post(self, req, resp):
        get_response = alexa_skill.Processor(
            req.media,
            buildin_intents,
            'Welcome to joke teller. Would you like to hear a joke?',
            'Good bye',
            JokeIntents(),  # Add implemented intent
        )
        json_response, handled = get_response()
        logging.info('Response was handled by system: {}'.format(handled))
        resp.media = json_response


app = falcon.API(media_type=falcon.MEDIA_JSON)
app.add_route('/v1/alexa/fulfiller', Fulfiller())
