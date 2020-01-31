from shutil import rmtree
from pathlib import Path

from hopster import server


#------------------------------------------------------------------------------#
for directory in ('.locks', '.videos', '.download'):
    path = Path(directory)
    rmtree(path)
    path.mkdir(exist_ok=True)

server.run(host='0.0.0.0', port=5000, debug=__debug__)
