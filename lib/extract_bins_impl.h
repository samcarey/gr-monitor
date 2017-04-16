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

#ifndef INCLUDED_MONITOR_EXTRACT_BINS_IMPL_H
#define INCLUDED_MONITOR_EXTRACT_BINS_IMPL_H

#include <monitor/extract_bins.h>

namespace gr {
  namespace monitor {

    class extract_bins_impl : public extract_bins
    {
     private:
         size_t d_vlen_in;
         std::vector<size_t> d_indices;
         std::vector<float> d_weights;
         size_t d_offset;

     public:
      extract_bins_impl(size_t vlen_in, std::vector<size_t> indices, std::vector<float> weights);
      ~extract_bins_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace monitor
} // namespace gr

#endif /* INCLUDED_MONITOR_EXTRACT_BINS_IMPL_H */

