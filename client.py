from time import sleep
from shutil import copyfileobj
from http import HTTPStatus
from sys import exit, stderr

from requests import get, post
from exitstatus import ExitStatus


#------------------------------------------------------------------------------#
SERVER = 'http://0.0.0.0:5000'
VIDEO_ID = 'k3YmNzaTE6XAeocyVuctpmcXe4g_iNWh'
START = '00:00:03'
STOP = '00:00:06'


#------------------------------------------------------------------------------#
def check_status_code(response):
    if response.status_code != HTTPStatus.OK:
        error = response.json()['error']
        print(f'Oups, something went wrong:',
              f'Response HTTP status code: {response.status_code}',
              f'Error message: {error["message"]}',
              f'Error code: {error["code"]}',
              sep='\n',
              file=stderr)
        exit(ExitStatus.failure)


#------------------------------------------------------------------------------#
# Schedule a new video download
print('Scheduling a task on the server to download a video...')
response = post(f'{SERVER}/schedule',
                json={'video_id': VIDEO_ID, 'start': START, 'stop': STOP})
check_status_code(response)
video_file = response.json()['video_file']
print('Task scheduled on the server successfully')

# Wait until its finished
while True:
    response = get(f'{SERVER}/progress?reference={video_file}')
    check_status_code(response)
    if response.json()['is_finished']:
        print("Video downloaded to the server successfully")
        break
    print('Downloading on the server is in progress...')
    sleep(1)

# Download the video
print('Downloading the video to the client...')
with get(f'{SERVER}/download?video_file={video_file}', stream=True) as response:
    check_status_code(response)
    response.raise_for_status()
    with open(video_file, 'wb') as file:
        copyfileobj(response.raw, file)
print('Video on the clinet downloaded successfully')
