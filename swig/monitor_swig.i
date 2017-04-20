/* -*- c++ -*- */

#define MONITOR_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "monitor_swig_doc.i"

%{
#include "monitor/extract_bins.h"
%}


%include "monitor/extract_bins.h"
GR_SWIG_BLOCK_MAGIC2(monitor, extract_bins);

