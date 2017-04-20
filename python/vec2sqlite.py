#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import sqlite3

class vec2sqlite(gr.sync_block):
    """
    docstring for block vec2sqlite
    """
    def __init__(self, data_type, vlen, filename, table_name, column_names, max_rows):
        gr.sync_block.__init__(self, name="vec2sqlite", in_sig=[(np.float32,vlen)], out_sig=None)
            
        self.vlen = vlen
        cols = '(' + ', '.join(column_names) + ')'
        question_marks = '(' + ', '.join(['?']*len(column_names)) + ')'
        self.insert_cmd = 'INSERT INTO ' + table_name + ' ' + cols + ' VALUES ' + question_marks
        self.limit_cmd = 'DELETE FROM ' + table_name + ' WHERE ROWID IN (SELECT ROWID FROM ' + table_name + ' ORDER BY ROWID DESC LIMIT -1 OFFSET ' + str(max_rows) + ')'

        # Establish database connection
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.conn.cursor()
        self.conn.text_factory = str
        self.c.execute('PRAGMA journal_mode=WAL')
        
        # Create table if we haven't already
        self.c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' ' + cols)
        self.conn.commit()

    def insert_vec_into_table(self, vals):
            self.c.execute(self.insert_cmd, vals.tolist())
            self.c.execute(self.limit_cmd)
            self.conn.commit()

    def work(self, input_items, output_items):
	in0 = input_items[0]
	for i in range(np.shape(in0)[0]):
		self.insert_vec_into_table(in0[i][:].reshape(self.vlen))
        return len(input_items[0])
