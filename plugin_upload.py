#!/usr/bin/env python
# coding=utf-8
"""This script uploads a plugin package to the plugin repository.
        Authors: A. Pasotti, V. Picavet
        git sha              : $TemplateVCSFormat
"""

import sys
import getpass
import xmlrpc.client
from optparse import OptionParser
from future import standard_library
import os
import zipfile

standard_library.install_aliases()

# Configuration
PROTOCOL = 'https'
SERVER = 'plugins.qgis.org'
PORT = '443'
ENDPOINT = '/plugins/RPC2/'
VERBOSE = False

ZIP_FILE_NAME = 'plugin.zip'


def zip_dir():
    """Zip plugin source code and place it inside a 'Transition-QGIS' folder"""
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(".", topdown=True):
            # Exclude certain directories from being zipped
            dirs[:] = [d for d in dirs if d not in [".git", ".idea", "__pycache__"]]
            for file in files:
                if file != ZIP_FILE_NAME:
                    # Calculate the relative path of the file to the root directory
                    relative_path = os.path.relpath(os.path.join(root, file), start=".")
                    # Construct the new path inside the 'Transition-QGIS' folder
                    new_path = os.path.join("Transition-QGIS", relative_path)
                    # Write the file to the zip with the new path
                    zipf.write(os.path.join(root, file), arcname=new_path)


def delete_zip():
    """Deletes the created zip file"""
    if os.path.exists(ZIP_FILE_NAME):
        os.remove(ZIP_FILE_NAME)
        print(f"{ZIP_FILE_NAME} has been deleted.")
    else:
        print(f"{ZIP_FILE_NAME} does not exist.")
            

def main(parameters):
    """Uploads plugin to

    :param parameters: Command line parameters.
    :param arguments: Command line arguments.
    """
    address = "{protocol}://{username}:{password}@{server}:{port}{endpoint}".format(
        protocol=PROTOCOL,
        username=parameters.username,
        password=parameters.password,
        server=parameters.server,
        port=parameters.port,
        endpoint=ENDPOINT)
    print("Connecting to: %s" % hide_password(address))

    server = xmlrpc.client.ServerProxy(address, verbose=VERBOSE)
    
    # Zip plugin source code
    zip_dir()

    try:
        # Upload plugin to QGIS
        with open(ZIP_FILE_NAME, 'rb') as handle:
            plugin_id, version_id = server.plugin.upload(
                xmlrpc.client.Binary(handle.read()))
        print("Plugin ID: %s" % plugin_id)
        print("Version ID: %s" % version_id)
    except xmlrpc.client.ProtocolError as err:
        print("A protocol error occurred")
        print("URL: %s" % hide_password(err.url, 0))
        print("HTTP/HTTPS headers: %s" % err.headers)
        print("Error code: %d" % err.errcode)
        print("Error message: %s" % err.errmsg)
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)

    # Delete zip file
    delete_zip()


def hide_password(url, start=6):
    """Returns the http url with password part replaced with '*'.

    :param url: URL to upload the plugin to.
    :type url: str

    :param start: Position of start of password.
    :type start: int
    """
    start_position = url.find(':', start) + 1
    end_position = url.find('@')
    return "%s%s%s" % (
        url[:start_position],
        '*' * (end_position - start_position),
        url[end_position:])


if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options]")
    parser.add_option(
        "-w", "--password", dest="password",
        help="Password for plugin site", metavar="******")
    parser.add_option(
        "-u", "--username", dest="username",
        help="Username of plugin site", metavar="user")
    parser.add_option(
        "-p", "--port", dest="port",
        help="Server port to connect to", metavar="80")
    parser.add_option(
        "-s", "--server", dest="server",
        help="Specify server name", metavar="plugins.qgis.org")
    options, args = parser.parse_args()

    if not options.server:
        options.server = SERVER
    if not options.port:
        options.port = PORT
    if not options.username:
        # interactive mode
        username = getpass.getuser()
        print("Please enter user name [%s] :" % username, end=' ')

        res = input()
        if res != "":
            options.username = res
        else:
            options.username = username
    if not options.password:
        # interactive mode
        options.password = getpass.getpass()
    main(options)
