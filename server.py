#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reference: https://github.com/go2starr/py-flask-video-stream
'''

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


import os
import re
import json

import mimetypes
from flask import Response, render_template
from flask import Flask
from flask import request

app = Flask(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


VIDEOS = json.load(open('./videos/data.json'))


def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range',
        'bytes {0}-{1}/{2}'.format(start, end, file_size,),
    )
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def parse_range(request):
    range = request.headers.get('Range')
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None

@app.route('/')
def home():
    response = render_template('index.html',
                               videos=sorted(VIDEOS.keys()))
    return response


@app.route('/play/<video_name>')
def play(video_name):
    response = render_template('player.html',
                               video_name=video_name)
    return response


@app.route('/video/<video_name>')
def video(video_name):
    video_path = VIDEOS[video_name]

    start, end = parse_range(request)
    return partial_response(video_path, start, end)


if __name__ == '__main__':
    HOST = '0.0.0.0'

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8080)
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt as e:
        'Exit.'

    #  app.run(host=HOST, port=8080, debug=True)
