"""
Wrapper script for script generated by GNU Radio companion, in order to avoid
having to edit the autogenerated script directly.
"""

import iq_to_file
from datetime import datetime
import sys
import argparse
import rotctld_logger
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument('basename', type=str, help='Prefix for output filenames.')
parser.add_argument('--center-freq', type=float, default=146000000)
parser.add_argument('--samp-rate', type=float, default=500000)
parser.add_argument('--record-angles', type=str, metavar='HOST[:PORT]', help='Record (az,el) from rotctld server if specified.')

args = parser.parse_args()

#generate base filename
output_filename_base = args.basename + '_freq_' + str(args.center_freq) + '_rate_' + str(args.samp_rate) +'_' + datetime.now().strftime('%Y-%m-%dT%M%S')

#iq data filename
args.filename = output_filename_base + '.iq'

angle_log_thread = None
if args.record_angles is not None:
    #connect to rotctld server
    host, port = rotctld_logger.get_host_port(args.record_angles)
    rotctl = rotctld_logger.rotctld_connect(host, port)

    #logfile
    rotctl_output_file = open(output_filename_base + '_antenna_angles.dat', "w")

    angle_log_thread = multiprocessing.Process(target=rotctld_logger.print_angles_forever, args=(rotctl, rotctl_output_file))
    angle_log_thread.start()

#run grc flowgraph
iq_to_file.main(options=args)

#stop az,el logging thread
if angle_log_thread is not None:
    angle_log_thread.terminate()
