from bottle import route, run, template
import requests
import time


class Stopwatch:
    def __init__(self):
        self.start_time = 0
        self.lap_time = 0
        self.start_to_lap = 0
        self.lap_to_stop = 0

    def start(self):
        self.start_time = time.time()
        self.lap_time = self.start_time

    def lap(self):
        self.lap_time = time.time()

    def stop(self):
        stop_time = time.time()
        self.start_to_lap = self.lap_time - self.start_time
        self.lap_to_stop = stop_time - self.lap_time


IFTTT_KEY = '*********************'
IFTTT_EVENT = 'stopwatch'
IFTTT_URL = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'.format(
    event=IFTTT_EVENT, key=IFTTT_KEY)


def make_web_request(start_to_lap, lap_to_stop):
    data = {}
    data['value1'] = start_to_lap
    data['value2'] = lap_to_stop

    try:
        response = requests.post(IFTTT_URL, data=data)
        print('{0.status_code}: {0.text}'.format(response))
    except:
        print('Failed to make a web request')


sw = Stopwatch()


@route('/stopwatch/<command>')
def stopwatch(command):
    if command == 'start':
        sw.start()
        return template('{{command}} requested', command=command)
    elif command == 'lap':
        sw.lap()
        return template('{{command}} requested', command=command)
    elif command == 'stop':
        sw.stop()
        make_web_request(round(sw.start_to_lap, 1), round(sw.lap_to_stop, 1))
        message = 'start to lap was {0} sec., lap to stop was {1} sec.'.format(
            round(sw.start_to_lap, 1),
            round(sw.lap_to_stop, 1))
        return template('{{message}}', message=message)

    return template('{{command}} is an unknown command', command=command)


run(host='localhost', port=8080)
