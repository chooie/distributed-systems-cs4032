import server_client_package.server.server_core.server_core as server

from shared_lib.constants import STATIC_HOST, STATIC_PORT
from directory.directory import DirectoryHandler

server.run(STATIC_HOST, STATIC_PORT, DirectoryHandler)
