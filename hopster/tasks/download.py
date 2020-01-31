from hopster.dummy.task import Task
from hopster.dummy.bucket import Bucket


#------------------------------------------------------------------------------#
@Task
def download_stream(stream, destination):
    file_path = stream.download(destination)
    Bucket().upload(file_path)
