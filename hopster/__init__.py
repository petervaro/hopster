from json import dumps
from http import HTTPStatus

from flask import Flask, Response, jsonify, send_file

from hopster.views.schedule import schedule as schedule_
from hopster.views.progress import progress as progress_
from hopster.views.download import download as download_


#------------------------------------------------------------------------------#
server = Flask('hopster')
server.config.from_object('hopster.config')


#------------------------------------------------------------------------------#
@server.route('/')
def index():
    return jsonify(
        {'message': "Welcome to Hopster's Video Downloading Service!"})


#------------------------------------------------------------------------------#
@server.route('/schedule', methods=['POST'])
def schedule():
    response, status = schedule_()
    return Response(response=dumps(response),
                    status=status,
                    mimetype='application/json')


#------------------------------------------------------------------------------#
@server.route('/progress', methods=['GET'])
def progress():
    response, status = progress_()
    return Response(response=dumps(response),
                    status=status,
                    mimetype='application/json')


#------------------------------------------------------------------------------#
@server.route('/download', methods=['GET'])
def download():
    response, status = download_()
    if status != HTTPStatus.OK:
        return Response(response=dumps(response),
                        status=status,
                        mimetype='application/json')
    return Response(response=open(response, 'rb'),
                    status=status,
                    mimetype="video/mp4",
                    direct_passthrough=True)
