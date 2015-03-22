import sys
import struct
import socket
import pprint
import optparse 

# in the github repo, cbapi is not in the example directory
sys.path.append('../src/cbapi')

import cbapi 

def build_cli_parser():
    parser = optparse.OptionParser(usage="%prog [options]", description="Dump sensor list")

    # for each supported output type, add an option
    #
    parser.add_option("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_option("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_option("-n", "--no-ssl-verify", action="store_false", default=True, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_option("-f", "--format", action="store", default='plain', dest="format",
                      help="Output in pipe-delimited ('pipe'), plaintext ('plain') format or csv ('csv'); plain by default")
    parser.add_option("-g", "--group", action="store", default=None, dest="groupid",
                      help="Limit sensor listing to just those specified by the sensor group id provided")
    return parser

def main(argv):
    parser = build_cli_parser()
    opts, args = parser.parse_args(argv)
    if not opts.url or not opts.token:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    if not opts.format == 'plain' and not opts.format == 'pipe' and not opts.format == 'csv':
        print "Format must be one of [plain|pipe|csv]"
        sys.exit(-1)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=opts.ssl_verify)

    # set up filters
    #
    filters = {}
    if opts.groupid is not None:
        filters['groupid'] = opts.groupid

    # enumerate sensors 
    #
    sensors = cb.sensors(filters)

    # output column headings as appropriate
    #
    if opts.format == 'pipe':
        print "%s|%s|%s|%s|%s" % ("sensor id", "group id", "computer name", "OS", "last checkin time")
    if opts.format == 'csv':
        print "%s,%s,%s,%s,%s" % ("sensor id", "group id", "computer name", "OS", "last checkin time")

    # output each sensor in turn
    #
    for sensor in sensors:
       if opts.format == 'plain': 
           print "%-20s : %s" % ("computer name", sensor['computer_name'])
           print "----------------------------------------------"
           print "%-20s : %s" % ("sensor_group_id", sensor['group_id'])
           print "%-20s : %s" % ("sensor id", sensor['id'])
           print "%-20s : %s" % ("os", sensor['os_environment_display_string'])
           print "%-20s : %s" % ("last checkin time", sensor['last_checkin_time'])
           print
       elif opts.format == 'pipe':
           print "%s|%s|%s|%s|%s" % (sensor['id'], sensor['group_id'], sensor['computer_name'], sensor['os_environment_display_string'], sensor['last_checkin_time'])
       elif opts.format == 'csv':
           print '"%s","%s","%s","%s","%s"' % (sensor['id'], sensor['group_id'], sensor['computer_name'], sensor['os_environment_display_string'], sensor['last_checkin_time'])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
