cdef extern from "string.h":
	ctypedef long size_t
	void *memcpy(void *dst,void *src,size_t len)
	void *memmove(void *dst,void *src,size_t len)
	char *strdup(char *)
