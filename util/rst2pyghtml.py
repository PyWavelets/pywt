#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Filip Wasilewski
# Date: $Date$

import rstdirective

def publish():
    import docutils.core
    docutils.core.publish_cmdline(writer_name='html')

if __name__ == "__main__":
    publish()
