from shutil import rmtree
from pathlib import Path

from hopster import server


#------------------------------------------------------------------------------#
for directory in ('.locks', '.bucket', '.videos', '.download'):
    path = Path(directory)
    rmtree(path, ignore_errors=True)
    path.mkdir(exist_ok=True)

server.run(host='0.0.0.0', port=5000, debug=__debug__)
