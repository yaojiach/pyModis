#!/usr/bin/env python
# script to download massive MODIS data from ftp
#
#  (c) Copyright Luca Delucchi 2010
#  Authors: Luca Delucchi
#  Email: luca dot delucchi at iasma dot it
#
##################################################################
#
#  This MODIS Python script is licensed under the terms of GNU GPL 2.
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
##################################################################

import sys
#import modis library
from pymodis import downmodis, optparse_gui, optparse_required


def main():
    """Main function"""
    #usage
    usage = "usage: %prog [options] destination_folder"
    if 1 == len(sys.argv):
        option_parser_class = optparse_gui.OptionParser
    else:
        option_parser_class = optparse_required.OptionParser
    parser = option_parser_class(usage=usage, description='modis_download')
    #password
    parser.add_option("-P", "--password", dest="password", default="None",
                      help="password to connect to ftp server [default=" \
                           "%default]")
    #username
    parser.add_option("-U", "--username", dest="user", default="anonymous",
                      help="username to connect to ftp server [default=%default]")
    #url
    parser.add_option("-u", "--url", default="http://e4ftl01.cr.usgs.gov",
                      help="ftp server url [default=%default]", dest="url")
    #tiles
    parser.add_option("-t", "--tiles", dest="tiles", default="None",
                      help="string of tiles separated from comma " \
                      + "[default=%default for all tiles]")
    #path to add the path in the server
    parser.add_option("-s", "--source", dest="path", default="MOLT",
                      help="directory on the ftp [default=%default]")
    #path to add the url
    parser.add_option("-p", "--product", dest="prod", default="MOD11A1.005",
                      help="directory on the ftp [default=%default]")
    #delta
    parser.add_option("-D", "--delta", dest="delta", default=10,
                      help="delta of day from the first day " \
                      + "[default=%default]")
    #first day
    parser.add_option("-f", "--firstday", dest="today", default=None,
                      metavar="LAST_DAY", help="the day to start download " \
                      + "[default=%default is for today]; if you want change" \
                      " data you must use this format YYYY-MM-DD")
    #first day
    parser.add_option("-e", "--endday", dest="enday", default=None,
                      metavar="FIRST_DAY", help="the day to start download " \
                      + "[default=%default]; if you want change" \
                      " data you must use this format YYYY-MM-DD")
    #debug
    parser.add_option("-x", action="store_true", dest="debug", default=False,
                      help="this is useful for debugging the " \
                      "download [default=%default]")
    #jpg
    parser.add_option("-j", action="store_true", dest="jpg", default=False,
                      help="download also the jpeg files [default=%default]")
    #only one day
    parser.add_option("-O", dest="oneday", action="store_true", default=False,
                      help="download only one day, it set " \
                      "delta=1 [default=%default]")
    #all days
    parser.add_option("-A", dest="alldays", action="store_true", default=False,
                      help="download all days, it usefull for first download "\
                      "of a product. It overwrite the 'firstday' and 'endday'"\
                      " options [default=%default]")
    #remove file with size = 0
    parser.add_option("-r", dest="empty", action="store_true", default=False,
                      help="remove files with size ugual to zero from " \
                      "'destination_folder'  [default=%default]")
    #parser.add_option("-A", dest="alldays", action="store_true", default=True,
                      #help="download all days from the first")

    #set false several options
    parser.set_defaults(oneday=False)
    parser.set_defaults(debug=False)
    parser.set_defaults(jpg=False)

    #return options and argument
    (options, args) = parser.parse_args()
    #test if args[0] it is set
    if len(args) == 0:
        parser.error("You have to pass the destination folder for HDF file")
    #check if oneday option it is set
    if options.oneday:
        options.delta = 1
    #set modis object
    modisOgg = downmodis.downModis(url=options.url, user=options.user,
               password=options.password, destinationFolder=args[0],
               tiles=options.tiles, path=options.path, product=options.prod, 
               today=options.today, enddate=options.enday, jpg=options.jpg,
               delta=int(options.delta), debug=options.debug)
    #connect to ftp
    modisOgg.connect()
    if modisOgg.nconnection <= 20:
        #download data
        modisOgg.downloadsAllDay(clean=options.empty, allDays=options.alldays)
    else:
        parser.error("Some problem with connection occur")

#add options
if __name__ == "__main__":
    main()