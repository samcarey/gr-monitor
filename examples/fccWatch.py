#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fccwatch
# Generated: Wed Apr 19 17:39:55 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import monitor
import numpy as np
import sip
import spr
import sys
import time
from gnuradio import qtgui


class fccWatch(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fccwatch")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fccwatch")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fccWatch")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.spec_samp_rate_pre = spec_samp_rate_pre = 40
        self.spec_samp_rate_post = spec_samp_rate_post = 1
        self.fccFreqs = fccFreqs = 1e6*np.array([461.025,461.075,461.1,462.155,462.375,462.4,464.5,464.55,464.6,464.625,464.65,464.725,464.75])
        self.samp_rate = samp_rate = 4e6
        self.fft_len = fft_len = 1024
        self.decimation_post = decimation_post = int(np.round(spec_samp_rate_pre/spec_samp_rate_post))
        self.center_freq = center_freq = (np.max(fccFreqs)+np.min(fccFreqs))/2
        self.waterfall_min = waterfall_min = -93
        self.waterfall_max = waterfall_max = -82
        self.indices = indices = np.round((fccFreqs - center_freq)*fft_len/samp_rate+fft_len/2).astype(int)
        self.fccFreqNames = fccFreqNames = [('_' + s + 'M').replace('.','_') for s in map(str,(fccFreqs*1e-6))]
        self.decimation_pre = decimation_pre = int(np.round(samp_rate/fft_len/spec_samp_rate_pre))
        self.bw = bw = np.max(fccFreqs)-np.min(fccFreqs)
        self.alpha = alpha = 1/float(decimation_post)

        ##################################################
        # Blocks
        ##################################################
        self._waterfall_min_range = Range(-140, 30, 1, -93, 200)
        self._waterfall_min_win = RangeWidget(self._waterfall_min_range, self.set_waterfall_min, "waterfall_min", "counter_slider", float)
        self.top_layout.addWidget(self._waterfall_min_win)
        self._waterfall_max_range = Range(-140, 30, 1, -82, 200)
        self._waterfall_max_win = RangeWidget(self._waterfall_max_range, self.set_waterfall_max, "waterfall_max", "counter_slider", float)
        self.top_layout.addWidget(self._waterfall_max_win)
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
        self.spr_vec_iir_0 = spr.vec_iir(len(indices), alpha)
        (self.spr_vec_iir_0).set_max_output_buffer(8)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	fft_len, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	center_freq, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(waterfall_min, waterfall_max)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            len(indices),
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-55, -20)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.monitor_vec2sqlite_0 = monitor.vec2sqlite(float, len(indices), '/home/samcarey/rfnoc/src/gr-monitor/examples/fccFreqs0.db', 'table1', fccFreqNames, 300)
        self.monitor_extract_bins_0 = monitor.extract_bins(fft_len, (indices), ([0.3, 0.3, 0.3]))
        (self.monitor_extract_bins_0).set_max_output_buffer(8)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (window.blackmanharris(1024)), True, 1)
        (self.fft_vxx_0).set_max_output_buffer(10)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, len(indices), 0)
        (self.blocks_nlog10_ff_0).set_max_output_buffer(64)
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
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.monitor_extract_bins_0, 0), (self.spr_vec_iir_0, 0))
        self.connect((self.spr_vec_iir_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fccWatch")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

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
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_waterfall_min(self):
        return self.waterfall_min

    def set_waterfall_min(self, waterfall_min):
        self.waterfall_min = waterfall_min
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.waterfall_min, self.waterfall_max)

    def get_waterfall_max(self):
        return self.waterfall_max

    def set_waterfall_max(self, waterfall_max):
        self.waterfall_max = waterfall_max
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.waterfall_min, self.waterfall_max)

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

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
