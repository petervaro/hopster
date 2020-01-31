from hopster.error import ServerError
from hopster.tasks.download import download_stream

#------------------------------------------------------------------------------#
class ProgressError(ServerError): pass
#------------------------------------------------------------------------------#
class MissingArgument(ProgressError): pass


#------------------------------------------------------------------------------#
def progress(raw_enquiry_details):
    try:
        reference = raw_enquiry_details['reference']
    except KeyError as key:
        raise MissingArgument(str(key))

    return {'is_finished': download_stream.is_finished(reference)}
