import server_client_package.server.server_core.server_core as server

from shared_lib.constants import STATIC_HOST
from file.constants import FILE_PORT
from file.file import FileHandler


server.run(STATIC_HOST, FILE_PORT, FileHandler)
