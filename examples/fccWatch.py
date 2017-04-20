#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fccwatch
# Generated: Thu Apr 20 19:03:56 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import monitor
import numpy as np
import time


class fccWatch(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Fccwatch")

        ##################################################
        # Variables
        ##################################################
        self.spec_samp_rate_pre = spec_samp_rate_pre = 4
        self.spec_samp_rate_post = spec_samp_rate_post = 1
        self.fccFreqs = fccFreqs = 1e6*np.array([461.025,461.075,461.1,462.155,462.375,462.4,464.5,464.55,464.6,464.625,464.65,464.725,464.75])
        self.samp_rate = samp_rate = 4e6
        self.fft_len = fft_len = 1024
        self.decimation_post = decimation_post = int(np.round(spec_samp_rate_pre/spec_samp_rate_post))
        self.center_freq = center_freq = (np.max(fccFreqs)+np.min(fccFreqs))/2
        self.indices = indices = np.round((fccFreqs - center_freq)*fft_len/samp_rate+fft_len/2).astype(int)
        self.fccFreqNames = fccFreqNames = [('_' + s + 'M').replace('.','_') for s in map(str,(fccFreqs*1e-6))]
        self.decimation_pre = decimation_pre = int(np.round(samp_rate/fft_len/spec_samp_rate_pre))
        self.bw = bw = np.max(fccFreqs)-np.min(fccFreqs)
        self.alpha = alpha = 1/float(decimation_post)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("type=b200", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(31.5, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.monitor_vec2sqlite_0 = monitor.vec2sqlite(float, len(indices), '/home/pi/sdr/pybombs_default/src/gr-monitor/examples/fccFreqs0.db', 'table1', fccFreqNames, 300)
        self.monitor_extract_bins_0 = monitor.extract_bins(fft_len, (indices), ([0.3, 0.3, 0.3]))
        (self.monitor_extract_bins_0).set_max_output_buffer(8)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (window.blackmanharris(1024)), True, 1)
        (self.fft_vxx_0).set_max_output_buffer(10)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, len(indices), 0)
        (self.blocks_nlog10_ff_0).set_max_output_buffer(1024)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*fft_len, decimation_pre)
        (self.blocks_keep_one_in_n_0_0).set_max_output_buffer(8)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_len)
        (self.blocks_complex_to_mag_squared_0).set_max_output_buffer(8)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.monitor_extract_bins_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.monitor_vec2sqlite_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.monitor_extract_bins_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))

    def get_spec_samp_rate_pre(self):
        return self.spec_samp_rate_pre

    def set_spec_samp_rate_pre(self, spec_samp_rate_pre):
        self.spec_samp_rate_pre = spec_samp_rate_pre
        self.set_decimation_pre(int(np.round(self.samp_rate/self.fft_len/self.spec_samp_rate_pre)))
        self.set_decimation_post(int(np.round(self.spec_samp_rate_pre/self.spec_samp_rate_post)))

    def get_spec_samp_rate_post(self):
        return self.spec_samp_rate_post

    def set_spec_samp_rate_post(self, spec_samp_rate_post):
        self.spec_samp_rate_post = spec_samp_rate_post
        self.set_decimation_post(int(np.round(self.spec_samp_rate_pre/self.spec_samp_rate_post)))

    def get_fccFreqs(self):
        return self.fccFreqs

    def set_fccFreqs(self, fccFreqs):
        self.fccFreqs = fccFreqs
        self.set_indices(np.round((self.fccFreqs - self.center_freq)*self.fft_len/self.samp_rate+self.fft_len/2).astype(int))
        self.set_fccFreqNames([('_' + s + 'M').replace('.','_') for s in map(str,(self.fccFreqs*1e-6))])
        self.set_center_freq((np.max(self.fccFreqs)+np.min(self.fccFreqs))/2)
        self.set_bw(np.max(self.fccFreqs)-np.min(self.fccFreqs))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_indices(np.round((self.fccFreqs - self.center_freq)*self.fft_len/self.samp_rate+self.fft_len/2).astype(int))
        self.set_decimation_pre(int(np.round(self.samp_rate/self.fft_len/self.spec_samp_rate_pre)))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_indices(np.round((self.fccFreqs - self.center_freq)*self.fft_len/self.samp_rate+self.fft_len/2).astype(int))
        self.set_decimation_pre(int(np.round(self.samp_rate/self.fft_len/self.spec_samp_rate_pre)))

    def get_decimation_post(self):
        return self.decimation_post

    def set_decimation_post(self, decimation_post):
        self.decimation_post = decimation_post
        self.set_alpha(1/float(self.decimation_post))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_indices(np.round((self.fccFreqs - self.center_freq)*self.fft_len/self.samp_rate+self.fft_len/2).astype(int))
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_indices(self):
        return self.indices

    def set_indices(self, indices):
        self.indices = indices

    def get_fccFreqNames(self):
        return self.fccFreqNames

    def set_fccFreqNames(self, fccFreqNames):
        self.fccFreqNames = fccFreqNames

    def get_decimation_pre(self):
        return self.decimation_pre

    def set_decimation_pre(self, decimation_pre):
        self.decimation_pre = decimation_pre
        self.blocks_keep_one_in_n_0_0.set_n(self.decimation_pre)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha


def main(top_block_cls=fccWatch, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
