/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "extract_bins_impl.h"

namespace gr {
  namespace monitor {

    extract_bins::sptr
    extract_bins::make(size_t vlen_in, std::vector<size_t> indices, std::vector<float> weights)
    {
      return gnuradio::get_initial_sptr
        (new extract_bins_impl(vlen_in, indices, weights));
    }

    /*
     * The private constructor
     */
    extract_bins_impl::extract_bins_impl(size_t vlen_in, std::vector<size_t> indices, std::vector<float> weights)
      : gr::sync_block("extract_bins",
              gr::io_signature::make(1, -1, sizeof(float)*vlen_in),
              gr::io_signature::make(1, -1, sizeof(float)*indices.size())),
      d_vlen_in(vlen_in),
      d_indices(indices),
      d_weights(weights),
      d_offset(size_t(weights.size()/2))
    {}

    /*
     * Our virtual destructor.
     */
    extract_bins_impl::~extract_bins_impl()
    {
    }

    int
    extract_bins_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for(size_t i = 0 ; i < noutput_items ; i++){
          for(size_t j = 0 ; j < d_indices.size() ; j++){
            float sum = 0;
            for(size_t k = 0 ; k < d_weights.size() ; k++){
                int idx = d_indices.at(j) + k - d_offset;
                if(idx >= 0 && idx < d_vlen_in){
                    sum += in[idx]*d_weights[k];
                }
            }
            out[j] = sum;
          }
          in += d_vlen_in;
          out += d_indices.size();
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace monitor */
} /* namespace gr */

