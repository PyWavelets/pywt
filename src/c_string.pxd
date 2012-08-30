# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

cdef extern from "string.h":
	ctypedef long size_t
	void *memcpy(void *dst,void *src,size_t len)
	void *memmove(void *dst,void *src,size_t len)
	char *strdup(char *)
