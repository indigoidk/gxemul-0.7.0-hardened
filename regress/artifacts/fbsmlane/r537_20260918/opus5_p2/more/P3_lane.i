
typedef long unsigned int size_t;
typedef __builtin_va_list __gnuc_va_list;
typedef unsigned char __u_char;
typedef unsigned short int __u_short;
typedef unsigned int __u_int;
typedef unsigned long int __u_long;
typedef signed char __int8_t;
typedef unsigned char __uint8_t;
typedef signed short int __int16_t;
typedef unsigned short int __uint16_t;
typedef signed int __int32_t;
typedef unsigned int __uint32_t;
typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;
typedef __int8_t __int_least8_t;
typedef __uint8_t __uint_least8_t;
typedef __int16_t __int_least16_t;
typedef __uint16_t __uint_least16_t;
typedef __int32_t __int_least32_t;
typedef __uint32_t __uint_least32_t;
typedef __int64_t __int_least64_t;
typedef __uint64_t __uint_least64_t;
typedef long int __quad_t;
typedef unsigned long int __u_quad_t;
typedef long int __intmax_t;
typedef unsigned long int __uintmax_t;
typedef unsigned long int __dev_t;
typedef unsigned int __uid_t;
typedef unsigned int __gid_t;
typedef unsigned long int __ino_t;
typedef unsigned long int __ino64_t;
typedef unsigned int __mode_t;
typedef unsigned long int __nlink_t;
typedef long int __off_t;
typedef long int __off64_t;
typedef int __pid_t;
typedef struct { int __val[2]; } __fsid_t;
typedef long int __clock_t;
typedef unsigned long int __rlim_t;
typedef unsigned long int __rlim64_t;
typedef unsigned int __id_t;
typedef long int __time_t;
typedef unsigned int __useconds_t;
typedef long int __suseconds_t;
typedef long int __suseconds64_t;
typedef int __daddr_t;
typedef int __key_t;
typedef int __clockid_t;
typedef void * __timer_t;
typedef long int __blksize_t;
typedef long int __blkcnt_t;
typedef long int __blkcnt64_t;
typedef unsigned long int __fsblkcnt_t;
typedef unsigned long int __fsblkcnt64_t;
typedef unsigned long int __fsfilcnt_t;
typedef unsigned long int __fsfilcnt64_t;
typedef long int __fsword_t;
typedef long int __ssize_t;
typedef long int __syscall_slong_t;
typedef unsigned long int __syscall_ulong_t;
typedef __off64_t __loff_t;
typedef char *__caddr_t;
typedef long int __intptr_t;
typedef unsigned int __socklen_t;
typedef int __sig_atomic_t;
typedef struct
{
  int __count;
  union
  {
    unsigned int __wch;
    char __wchb[4];
  } __value;
} __mbstate_t;
typedef struct _G_fpos_t
{
  __off_t __pos;
  __mbstate_t __state;
} __fpos_t;
typedef struct _G_fpos64_t
{
  __off64_t __pos;
  __mbstate_t __state;
} __fpos64_t;
struct _IO_FILE;
typedef struct _IO_FILE __FILE;
struct _IO_FILE;
typedef struct _IO_FILE FILE;
struct _IO_FILE;
struct _IO_marker;
struct _IO_codecvt;
struct _IO_wide_data;
typedef void _IO_lock_t;
struct _IO_FILE
{
  int _flags;
  char *_IO_read_ptr;
  char *_IO_read_end;
  char *_IO_read_base;
  char *_IO_write_base;
  char *_IO_write_ptr;
  char *_IO_write_end;
  char *_IO_buf_base;
  char *_IO_buf_end;
  char *_IO_save_base;
  char *_IO_backup_base;
  char *_IO_save_end;
  struct _IO_marker *_markers;
  struct _IO_FILE *_chain;
  int _fileno;
  int _flags2:24;
  char _short_backupbuf[1];
  __off_t _old_offset;
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];
  _IO_lock_t *_lock;
  __off64_t _offset;
  struct _IO_codecvt *_codecvt;
  struct _IO_wide_data *_wide_data;
  struct _IO_FILE *_freeres_list;
  void *_freeres_buf;
  struct _IO_FILE **_prevchain;
  int _mode;
  int _unused3;
  __uint64_t _total_written;
  char _unused2[12 * sizeof (int) - 5 * sizeof (void *)];
};
typedef __ssize_t cookie_read_function_t (void *__cookie, char *__buf,
                                          size_t __nbytes);
typedef __ssize_t cookie_write_function_t (void *__cookie, const char *__buf,
                                           size_t __nbytes);
typedef int cookie_seek_function_t (void *__cookie, __off64_t *__pos, int __w);
typedef int cookie_close_function_t (void *__cookie);
typedef struct _IO_cookie_io_functions_t
{
  cookie_read_function_t *read;
  cookie_write_function_t *write;
  cookie_seek_function_t *seek;
  cookie_close_function_t *close;
} cookie_io_functions_t;
typedef __gnuc_va_list va_list;
typedef __off_t off_t;
typedef __ssize_t ssize_t;
typedef __fpos_t fpos_t;
extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;
extern int remove (const char *__filename) __attribute__ ((__nothrow__ , __leaf__));
extern int rename (const char *__old, const char *__new) __attribute__ ((__nothrow__ , __leaf__));
extern int renameat (int __oldfd, const char *__old, int __newfd,
       const char *__new) __attribute__ ((__nothrow__ , __leaf__));
extern int fclose (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern FILE *tmpfile (void)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern char *tmpnam (char[20]) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern char *tmpnam_r (char __s[20]) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern char *tempnam (const char *__dir, const char *__pfx)
   __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__malloc__ (__builtin_free, 1)));
extern int fflush (FILE *__stream);
extern int fflush_unlocked (FILE *__stream);
extern FILE *fopen (const char *__restrict __filename,
      const char *__restrict __modes)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern FILE *freopen (const char *__restrict __filename,
        const char *__restrict __modes,
        FILE *__restrict __stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (3)));
extern FILE *fdopen (int __fd, const char *__modes) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern FILE *fopencookie (void *__restrict __magic_cookie,
     const char *__restrict __modes,
     cookie_io_functions_t __io_funcs) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern FILE *fmemopen (void *__s, size_t __len, const char *__modes)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern FILE *open_memstream (char **__bufloc, size_t *__sizeloc) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) __attribute__ ((__warn_unused_result__));
extern void setbuf (FILE *__restrict __stream, char *__restrict __buf) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__nonnull__ (1)));
extern int setvbuf (FILE *__restrict __stream, char *__restrict __buf,
      int __modes, size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern void setbuffer (FILE *__restrict __stream, char *__restrict __buf,
         size_t __size) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern void setlinebuf (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int fprintf (FILE *__restrict __stream,
      const char *__restrict __format, ...) __attribute__ ((__nonnull__ (1)));
extern int printf (const char *__restrict __format, ...);
extern int sprintf (char *__restrict __s,
      const char *__restrict __format, ...) __attribute__ ((__nothrow__));
extern int vfprintf (FILE *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg) __attribute__ ((__nonnull__ (1)));
extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);
extern int vsprintf (char *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg) __attribute__ ((__nothrow__));
extern int snprintf (char *__restrict __s, size_t __maxlen,
       const char *__restrict __format, ...)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 4)));
extern int vsnprintf (char *__restrict __s, size_t __maxlen,
        const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 0)));
extern int vasprintf (char **__restrict __ptr, const char *__restrict __f,
        __gnuc_va_list __arg)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 2, 0))) __attribute__ ((__warn_unused_result__));
extern int __asprintf (char **__restrict __ptr,
         const char *__restrict __fmt, ...)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 2, 3))) __attribute__ ((__warn_unused_result__));
extern int asprintf (char **__restrict __ptr,
       const char *__restrict __fmt, ...)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 2, 3))) __attribute__ ((__warn_unused_result__));
extern int vdprintf (int __fd, const char *__restrict __fmt,
       __gnuc_va_list __arg)
     __attribute__ ((__format__ (__printf__, 2, 0)));
extern int dprintf (int __fd, const char *__restrict __fmt, ...)
     __attribute__ ((__format__ (__printf__, 2, 3)));
extern int fscanf (FILE *__restrict __stream,
     const char *__restrict __format, ...) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int scanf (const char *__restrict __format, ...) __attribute__ ((__warn_unused_result__));
extern int sscanf (const char *__restrict __s,
     const char *__restrict __format, ...) __attribute__ ((__nothrow__ , __leaf__));
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf") __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int scanf (const char *__restrict __format, ...) __asm__ ("" "__isoc99_scanf") __attribute__ ((__warn_unused_result__));
extern int sscanf (const char *__restrict __s, const char *__restrict __format, ...) __asm__ ("" "__isoc99_sscanf") __attribute__ ((__nothrow__ , __leaf__));
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format,
      __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 2, 0))) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 1, 0))) __attribute__ ((__warn_unused_result__));
extern int vsscanf (const char *__restrict __s,
      const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__format__ (__scanf__, 2, 0)));
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vfscanf")
     __attribute__ ((__format__ (__scanf__, 2, 0))) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vscanf")
     __attribute__ ((__format__ (__scanf__, 1, 0))) __attribute__ ((__warn_unused_result__));
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__ ((__format__ (__scanf__, 2, 0)));
extern int fgetc (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int getc (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int getchar (void);
extern int getc_unlocked (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int getchar_unlocked (void);
extern int fgetc_unlocked (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int fputc (int __c, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern int putc (int __c, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern int putchar (int __c);
extern int fputc_unlocked (int __c, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern int putc_unlocked (int __c, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern int putchar_unlocked (int __c);
extern int getw (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int putw (int __w, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
     __attribute__ ((__warn_unused_result__)) __attribute__ ((__access__ (__write_only__, 1, 2))) __attribute__ ((__nonnull__ (3)));
extern char *gets (char *__s) __attribute__ ((__warn_unused_result__)) __attribute__ ((__deprecated__));
extern __ssize_t __getdelim (char **__restrict __lineptr,
                             size_t *__restrict __n, int __delimiter,
                             FILE *__restrict __stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (4)));
extern __ssize_t getdelim (char **__restrict __lineptr,
                           size_t *__restrict __n, int __delimiter,
                           FILE *__restrict __stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (4)));
extern __ssize_t getline (char **__restrict __lineptr,
                          size_t *__restrict __n,
                          FILE *__restrict __stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (3)));
extern int fputs (const char *__restrict __s, FILE *__restrict __stream)
  __attribute__ ((__nonnull__ (2)));
extern int puts (const char *__s);
extern int ungetc (int __c, FILE *__stream) __attribute__ ((__nonnull__ (2)));
extern size_t fread (void *__restrict __ptr, size_t __size,
       size_t __n, FILE *__restrict __stream) __attribute__ ((__warn_unused_result__))
  __attribute__ ((__nonnull__ (4)));
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
        size_t __n, FILE *__restrict __s) __attribute__ ((__nonnull__ (4)));
extern size_t fread_unlocked (void *__restrict __ptr, size_t __size,
         size_t __n, FILE *__restrict __stream) __attribute__ ((__warn_unused_result__))
  __attribute__ ((__nonnull__ (4)));
extern size_t fwrite_unlocked (const void *__restrict __ptr, size_t __size,
          size_t __n, FILE *__restrict __stream)
  __attribute__ ((__nonnull__ (4)));
extern int fseek (FILE *__stream, long int __off, int __whence)
  __attribute__ ((__nonnull__ (1)));
extern long int ftell (FILE *__stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern void rewind (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern int fseeko (FILE *__stream, __off_t __off, int __whence)
  __attribute__ ((__nonnull__ (1)));
extern __off_t ftello (FILE *__stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int fgetpos (FILE *__restrict __stream, fpos_t *__restrict __pos)
  __attribute__ ((__nonnull__ (1)));
extern int fsetpos (FILE *__stream, const fpos_t *__pos) __attribute__ ((__nonnull__ (1)));
extern void clearerr (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int feof (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int ferror (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern void clearerr_unlocked (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int feof_unlocked (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int ferror_unlocked (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern void perror (const char *__s) __attribute__ ((__cold__));
extern int fileno (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int fileno_unlocked (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern int pclose (FILE *__stream) __attribute__ ((__nonnull__ (1)));
extern FILE *popen (const char *__command, const char *__modes)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (pclose, 1))) __attribute__ ((__warn_unused_result__));
extern char *ctermid (char *__s) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__access__ (__write_only__, 1)));
extern void flockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int ftrylockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (1)));
extern void funlockfile (FILE *__stream) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int __uflow (FILE *);
extern int __overflow (FILE *, int);
extern int __sprintf_chk (char *__restrict __s, int __flag, size_t __slen,
     const char *__restrict __format, ...) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 3)));
extern int __vsprintf_chk (char *__restrict __s, int __flag, size_t __slen,
      const char *__restrict __format,
      __gnuc_va_list __ap) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 3)));
extern int __snprintf_chk (char *__restrict __s, size_t __n, int __flag,
      size_t __slen, const char *__restrict __format,
      ...) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 2)));
extern int __vsnprintf_chk (char *__restrict __s, size_t __n, int __flag,
       size_t __slen, const char *__restrict __format,
       __gnuc_va_list __ap) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 2)));
extern int __fprintf_chk (FILE *__restrict __stream, int __flag,
     const char *__restrict __format, ...)
    __attribute__ ((__nonnull__ (1)));
extern int __printf_chk (int __flag, const char *__restrict __format, ...);
extern int __vfprintf_chk (FILE *__restrict __stream, int __flag,
      const char *__restrict __format,
      __gnuc_va_list __ap) __attribute__ ((__nonnull__ (1)));
extern int __vprintf_chk (int __flag, const char *__restrict __format,
     __gnuc_va_list __ap);
extern int __dprintf_chk (int __fd, int __flag, const char *__restrict __fmt,
     ...) __attribute__ ((__format__ (__printf__, 3, 4)));
extern int __vdprintf_chk (int __fd, int __flag,
      const char *__restrict __fmt, __gnuc_va_list __arg)
     __attribute__ ((__format__ (__printf__, 3, 0)));
extern char *__gets_warn (char *__str) __asm__ ("" "gets")
     __attribute__ ((__warn_unused_result__)) __attribute__((__warning__ ("please use fgets or getline instead, gets can't " "specify buffer size")));
extern char *__gets_chk (char *__str, size_t) __attribute__ ((__warn_unused_result__));
extern char *__fgets_alias (char *__restrict __s, int __n, FILE *__restrict __stream) __asm__ ("" "fgets")
    __attribute__ ((__warn_unused_result__)) __attribute__ ((__access__ (__write_only__, 1, 2)));
extern char *__fgets_chk_warn (char *__restrict __s, size_t __size, int __n, FILE *__restrict __stream) __asm__ ("" "__fgets_chk")
     __attribute__ ((__warn_unused_result__)) __attribute__((__warning__ ("fgets called with bigger size than length " "of destination buffer")));
extern char *__fgets_chk (char *__restrict __s, size_t __size, int __n,
     FILE *__restrict __stream)
    __attribute__ ((__warn_unused_result__)) __attribute__ ((__access__ (__write_only__, 1, 3))) __attribute__ ((__nonnull__ (4)));
extern size_t __fread_alias (void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __stream) __asm__ ("" "fread") __attribute__ ((__warn_unused_result__));
extern size_t __fread_chk_warn (void *__restrict __ptr, size_t __ptrlen, size_t __size, size_t __n, FILE *__restrict __stream) __asm__ ("" "__fread_chk")
     __attribute__ ((__warn_unused_result__)) __attribute__((__warning__ ("fread called with bigger size * nmemb than length " "of destination buffer")));
extern size_t __fread_chk (void *__restrict __ptr, size_t __ptrlen,
      size_t __size, size_t __n,
      FILE *__restrict __stream) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (5)));
extern size_t __fread_unlocked_alias (void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __stream) __asm__ ("" "fread_unlocked") __attribute__ ((__warn_unused_result__));
extern size_t __fread_unlocked_chk_warn (void *__restrict __ptr, size_t __ptrlen, size_t __size, size_t __n, FILE *__restrict __stream) __asm__ ("" "__fread_unlocked_chk")
     __attribute__ ((__warn_unused_result__)) __attribute__((__warning__ ("fread_unlocked called with bigger size * nmemb than " "length of destination buffer")));
extern size_t __fread_unlocked_chk (void *__restrict __ptr, size_t __ptrlen,
        size_t __size, size_t __n,
        FILE *__restrict __stream)
    __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (5)));
extern __inline __attribute__ ((__gnu_inline__)) int
getchar (void)
{
  return getc (stdin);
}
extern __inline __attribute__ ((__gnu_inline__)) int
fgetc_unlocked (FILE *__fp)
{
  return (__builtin_expect (((__fp)->_IO_read_ptr >= (__fp)->_IO_read_end), 0) ? __uflow (__fp) : *(unsigned char *) (__fp)->_IO_read_ptr++);
}
extern __inline __attribute__ ((__gnu_inline__)) int
getc_unlocked (FILE *__fp)
{
  return (__builtin_expect (((__fp)->_IO_read_ptr >= (__fp)->_IO_read_end), 0) ? __uflow (__fp) : *(unsigned char *) (__fp)->_IO_read_ptr++);
}
extern __inline __attribute__ ((__gnu_inline__)) int
getchar_unlocked (void)
{
  return (__builtin_expect (((stdin)->_IO_read_ptr >= (stdin)->_IO_read_end), 0) ? __uflow (stdin) : *(unsigned char *) (stdin)->_IO_read_ptr++);
}
extern __inline __attribute__ ((__gnu_inline__)) int
putchar (int __c)
{
  return putc (__c, stdout);
}
extern __inline __attribute__ ((__gnu_inline__)) int
fputc_unlocked (int __c, FILE *__stream)
{
  return (__builtin_expect (((__stream)->_IO_write_ptr >= (__stream)->_IO_write_end), 0) ? __overflow (__stream, (unsigned char) (__c)) : (unsigned char) (*(__stream)->_IO_write_ptr++ = (__c)));
}
extern __inline __attribute__ ((__gnu_inline__)) int
putc_unlocked (int __c, FILE *__stream)
{
  return (__builtin_expect (((__stream)->_IO_write_ptr >= (__stream)->_IO_write_end), 0) ? __overflow (__stream, (unsigned char) (__c)) : (unsigned char) (*(__stream)->_IO_write_ptr++ = (__c)));
}
extern __inline __attribute__ ((__gnu_inline__)) int
putchar_unlocked (int __c)
{
  return (__builtin_expect (((stdout)->_IO_write_ptr >= (stdout)->_IO_write_end), 0) ? __overflow (stdout, (unsigned char) (__c)) : (unsigned char) (*(stdout)->_IO_write_ptr++ = (__c)));
}
extern __inline __attribute__ ((__gnu_inline__)) int
__attribute__ ((__nothrow__ , __leaf__)) feof_unlocked (FILE *__stream)
{
  return (((__stream)->_flags & 0x0010) != 0);
}
extern __inline __attribute__ ((__gnu_inline__)) int
__attribute__ ((__nothrow__ , __leaf__)) ferror_unlocked (FILE *__stream)
{
  return (((__stream)->_flags & 0x0020) != 0);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
__attribute__ ((__nothrow__ , __leaf__)) sprintf (char *__restrict __s, const char *__restrict __fmt, ...)
{
  return __builtin___sprintf_chk (__s, 2 - 1,
      __builtin_object_size (__s, 2 > 1), __fmt,
      __builtin_va_arg_pack ());
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
__attribute__ ((__nothrow__ , __leaf__)) vsprintf (char * __restrict __s, const char *__restrict __fmt, __gnuc_va_list __ap)
{
  return __builtin___vsprintf_chk (__s, 2 - 1,
       __builtin_object_size (__s, 2 > 1), __fmt, __ap);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
__attribute__ ((__nothrow__ , __leaf__)) snprintf (char *__restrict __s, size_t __n, const char *__restrict __fmt, ...)
{
  return __builtin___snprintf_chk (__s, __n, 2 - 1,
       __builtin_object_size (__s, 2 > 1), __fmt,
       __builtin_va_arg_pack ());
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
__attribute__ ((__nothrow__ , __leaf__)) vsnprintf (char * __restrict __s, size_t __n, const char *__restrict __fmt, __gnuc_va_list __ap)
    
{
  return __builtin___vsnprintf_chk (__s, __n, 2 - 1,
        __builtin_object_size (__s, 2 > 1), __fmt, __ap);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__nonnull__ (1))) int
fprintf (FILE *__restrict __stream, const char *__restrict __fmt, ...)
{
  return __fprintf_chk (__stream, 2 - 1, __fmt,
   __builtin_va_arg_pack ());
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
printf (const char *__restrict __fmt, ...)
{
  return __printf_chk (2 - 1, __fmt, __builtin_va_arg_pack ());
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
vprintf (const char * __restrict __fmt,
  __gnuc_va_list __ap)
{
  return __vfprintf_chk (stdout, 2 - 1, __fmt, __ap);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__nonnull__ (1))) int
vfprintf (FILE *__restrict __stream,
   const char *__restrict __fmt, __gnuc_va_list __ap)
{
  return __vfprintf_chk (__stream, 2 - 1, __fmt, __ap);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
dprintf (int __fd, const char *__restrict __fmt, ...)
{
  return __dprintf_chk (__fd, 2 - 1, __fmt,
   __builtin_va_arg_pack ());
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
vdprintf (int __fd, const char *__restrict __fmt, __gnuc_va_list __ap)
{
  return __vdprintf_chk (__fd, 2 - 1, __fmt, __ap);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) char *
gets (char * __str)
    
{
  if (__builtin_object_size (__str, 2 > 1) != (size_t) -1)
    return __gets_chk (__str, __builtin_object_size (__str, 2 > 1));
  return __gets_warn (__str);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__access__ (__write_only__, 1, 2)))
__attribute__ ((__nonnull__ (3))) char *
fgets (char * __restrict __s, int __n,
       FILE *__restrict __stream)
    
{
  size_t __sz = __builtin_object_size (__s, 2 > 1);
  if (((__builtin_constant_p (__sz) && (__sz) == (long unsigned int) -1) || (((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= ((__sz)) / ((sizeof (char))))) && (((long unsigned int) (__n)) <= ((__sz)) / ((sizeof (char)))))))
    return __fgets_alias (__s, __n, __stream);
  if ((((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= (__sz) / (sizeof (char)))) && !(((long unsigned int) (__n)) <= (__sz) / (sizeof (char)))))
    return __fgets_chk_warn (__s, __sz, __n, __stream);
  return __fgets_chk (__s, __sz, __n, __stream);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (4))) size_t
fread (void * __restrict __ptr,
       size_t __size, size_t __n, FILE *__restrict __stream)
    
{
  size_t __sz = __builtin_object_size (__ptr, 0);
  if (((__builtin_constant_p (__sz) && (__sz) == (long unsigned int) -1) || (((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= ((__sz)) / ((__size)))) && (((long unsigned int) (__n)) <= ((__sz)) / ((__size))))))
    return __fread_alias (__ptr, __size, __n, __stream);
  if ((((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= (__sz) / (__size))) && !(((long unsigned int) (__n)) <= (__sz) / (__size))))
    return __fread_chk_warn (__ptr, __sz, __size, __n, __stream);
  return __fread_chk (__ptr, __sz, __size, __n, __stream);
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__nonnull__ (4))) size_t
fread_unlocked (void * __restrict __ptr,
  size_t __size, size_t __n, FILE *__restrict __stream)
    
{
  size_t __sz = __builtin_object_size (__ptr, 0);
  if (((__builtin_constant_p (__sz) && (__sz) == (long unsigned int) -1) || (((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= ((__sz)) / ((__size)))) && (((long unsigned int) (__n)) <= ((__sz)) / ((__size))))))
    {
      if (__builtin_constant_p (__size)
   && __builtin_constant_p (__n)
   && (__size | __n) < (((size_t) 1) << (8 * sizeof (size_t) / 2))
   && __size * __n <= 8)
 {
   size_t __cnt = __size * __n;
   char *__cptr = (char *) __ptr;
   if (__cnt == 0)
     return 0;
   for (; __cnt > 0; --__cnt)
     {
       int __c = getc_unlocked (__stream);
       if (__c == (-1))
  break;
       *__cptr++ = __c;
     }
   return (__cptr - (char *) __ptr) / __size;
 }
      return __fread_unlocked_alias (__ptr, __size, __n, __stream);
    }
  if ((((__typeof (__n)) 0 < (__typeof (__n)) -1 || (__builtin_constant_p (__n) && (__n) > 0)) && __builtin_constant_p ((((long unsigned int) (__n)) <= (__sz) / (__size))) && !(((long unsigned int) (__n)) <= (__sz) / (__size))))
    return __fread_unlocked_chk_warn (__ptr, __sz, __size, __n, __stream);
  return __fread_unlocked_chk (__ptr, __sz, __size, __n, __stream);
}

typedef int wchar_t;

typedef struct
  {
    int quot;
    int rem;
  } div_t;
typedef struct
  {
    long int quot;
    long int rem;
  } ldiv_t;
__extension__ typedef struct
  {
    long long int quot;
    long long int rem;
  } lldiv_t;
extern size_t __ctype_get_mb_cur_max (void) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern double atof (const char *__nptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern int atoi (const char *__nptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern long int atol (const char *__nptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
__extension__ extern long long int atoll (const char *__nptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern double strtod (const char *__restrict __nptr,
        char **__restrict __endptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern float strtof (const char *__restrict __nptr,
       char **__restrict __endptr) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern long double strtold (const char *__restrict __nptr,
       char **__restrict __endptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern long int strtol (const char *__restrict __nptr,
   char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern unsigned long int strtoul (const char *__restrict __nptr,
      char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
__extension__
extern long long int strtoq (const char *__restrict __nptr,
        char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
__extension__
extern unsigned long long int strtouq (const char *__restrict __nptr,
           char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
__extension__
extern long long int strtoll (const char *__restrict __nptr,
         char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
__extension__
extern unsigned long long int strtoull (const char *__restrict __nptr,
     char **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern __inline __attribute__ ((__gnu_inline__)) int
__attribute__ ((__nothrow__ , __leaf__)) atoi (const char *__nptr)
{
  return (int) strtol (__nptr, (char **) ((void *)0), 10);
}
extern __inline __attribute__ ((__gnu_inline__)) long int
__attribute__ ((__nothrow__ , __leaf__)) atol (const char *__nptr)
{
  return strtol (__nptr, (char **) ((void *)0), 10);
}
__extension__ extern __inline __attribute__ ((__gnu_inline__)) long long int
__attribute__ ((__nothrow__ , __leaf__)) atoll (const char *__nptr)
{
  return strtoll (__nptr, (char **) ((void *)0), 10);
}
extern char *l64a (long int __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern long int a64l (const char *__s)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));

typedef __u_char u_char;
typedef __u_short u_short;
typedef __u_int u_int;
typedef __u_long u_long;
typedef __quad_t quad_t;
typedef __u_quad_t u_quad_t;
typedef __fsid_t fsid_t;
typedef __loff_t loff_t;
typedef __ino_t ino_t;
typedef __dev_t dev_t;
typedef __gid_t gid_t;
typedef __mode_t mode_t;
typedef __nlink_t nlink_t;
typedef __uid_t uid_t;
typedef __pid_t pid_t;
typedef __id_t id_t;
typedef __daddr_t daddr_t;
typedef __caddr_t caddr_t;
typedef __key_t key_t;
typedef __clock_t clock_t;
typedef __clockid_t clockid_t;
typedef __time_t time_t;
typedef __timer_t timer_t;
typedef unsigned long int ulong;
typedef unsigned short int ushort;
typedef unsigned int uint;
typedef __int8_t int8_t;
typedef __int16_t int16_t;
typedef __int32_t int32_t;
typedef __int64_t int64_t;
typedef __uint8_t u_int8_t;
typedef __uint16_t u_int16_t;
typedef __uint32_t u_int32_t;
typedef __uint64_t u_int64_t;
typedef int register_t __attribute__ ((__mode__ (__word__)));
static __inline __uint16_t
__bswap_16 (__uint16_t __bsx)
{
  return __builtin_bswap16 (__bsx);
}
static __inline __uint32_t
__bswap_32 (__uint32_t __bsx)
{
  return __builtin_bswap32 (__bsx);
}
__extension__ static __inline __uint64_t
__bswap_64 (__uint64_t __bsx)
{
  return __builtin_bswap64 (__bsx);
}
static __inline __uint16_t
__uint16_identity (__uint16_t __x)
{
  return __x;
}
static __inline __uint32_t
__uint32_identity (__uint32_t __x)
{
  return __x;
}
static __inline __uint64_t
__uint64_identity (__uint64_t __x)
{
  return __x;
}
typedef struct
{
  unsigned long int __val[(1024 / (8 * sizeof (unsigned long int)))];
} __sigset_t;
typedef __sigset_t sigset_t;
struct timeval
{
  __time_t tv_sec;
  __suseconds_t tv_usec;
};
struct timespec
{
  __time_t tv_sec;
  __syscall_slong_t tv_nsec;
};
typedef __suseconds_t suseconds_t;
typedef long int __fd_mask;
typedef struct
  {
    __fd_mask __fds_bits[1024 / (8 * (int) sizeof (__fd_mask))];
  } fd_set;
typedef __fd_mask fd_mask;

extern int select (int __nfds, fd_set *__restrict __readfds,
     fd_set *__restrict __writefds,
     fd_set *__restrict __exceptfds,
     struct timeval *__restrict __timeout);
extern int pselect (int __nfds, fd_set *__restrict __readfds,
      fd_set *__restrict __writefds,
      fd_set *__restrict __exceptfds,
      const struct timespec *__restrict __timeout,
      const __sigset_t *__restrict __sigmask);
extern long int __fdelt_chk (long int __d);
extern long int __fdelt_warn (long int __d)
  __attribute__((__warning__ ("bit outside of fd_set selected")));

typedef __blksize_t blksize_t;
typedef __blkcnt_t blkcnt_t;
typedef __fsblkcnt_t fsblkcnt_t;
typedef __fsfilcnt_t fsfilcnt_t;
typedef union
{
  __extension__ unsigned long long int __value64;
  struct
  {
    unsigned int __low;
    unsigned int __high;
  } __value32;
} __atomic_wide_counter;
typedef struct __pthread_internal_list
{
  struct __pthread_internal_list *__prev;
  struct __pthread_internal_list *__next;
} __pthread_list_t;
typedef struct __pthread_internal_slist
{
  struct __pthread_internal_slist *__next;
} __pthread_slist_t;
struct __pthread_mutex_s
{
  int __lock;
  unsigned int __count;
  int __owner;
  unsigned int __nusers;
  int __kind;
  short __spins;
  short __elision;
  __pthread_list_t __list;
};
struct __pthread_rwlock_arch_t
{
  unsigned int __readers;
  unsigned int __writers;
  unsigned int __wrphase_futex;
  unsigned int __writers_futex;
  unsigned int __pad3;
  unsigned int __pad4;
  int __cur_writer;
  int __shared;
  signed char __rwelision;
  unsigned char __pad1[7];
  unsigned long int __pad2;
  unsigned int __flags;
};
struct __pthread_cond_s
{
  __atomic_wide_counter __wseq;
  __atomic_wide_counter __g1_start;
  unsigned int __g_size[2] ;
  unsigned int __g1_orig_size;
  unsigned int __wrefs;
  unsigned int __g_signals[2];
  unsigned int __unused_initialized_1;
  unsigned int __unused_initialized_2;
};
typedef unsigned int __tss_t;
typedef unsigned long int __thrd_t;
typedef struct
{
  int __data ;
} __once_flag;
typedef unsigned long int pthread_t;
typedef union
{
  char __size[4];
  int __align;
} pthread_mutexattr_t;
typedef union
{
  char __size[4];
  int __align;
} pthread_condattr_t;
typedef unsigned int pthread_key_t;
typedef int pthread_once_t;
union pthread_attr_t
{
  char __size[56];
  long int __align;
};
typedef union pthread_attr_t pthread_attr_t;
typedef union
{
  struct __pthread_mutex_s __data;
  char __size[40];
  long int __align;
} pthread_mutex_t;
typedef union
{
  struct __pthread_cond_s __data;
  char __size[48];
  __extension__ long long int __align;
} pthread_cond_t;
typedef union
{
  struct __pthread_rwlock_arch_t __data;
  char __size[56];
  long int __align;
} pthread_rwlock_t;
typedef union
{
  char __size[8];
  long int __align;
} pthread_rwlockattr_t;
typedef volatile int pthread_spinlock_t;
typedef union
{
  char __size[32];
  long int __align;
} pthread_barrier_t;
typedef union
{
  char __size[4];
  int __align;
} pthread_barrierattr_t;

extern long int random (void) __attribute__ ((__nothrow__ , __leaf__));
extern void srandom (unsigned int __seed) __attribute__ ((__nothrow__ , __leaf__));
extern char *initstate (unsigned int __seed, char *__statebuf,
   size_t __statelen) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)));
extern char *setstate (char *__statebuf) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
struct random_data
  {
    int32_t *fptr;
    int32_t *rptr;
    int32_t *state;
    int rand_type;
    int rand_deg;
    int rand_sep;
    int32_t *end_ptr;
  };
extern int random_r (struct random_data *__restrict __buf,
       int32_t *__restrict __result) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int srandom_r (unsigned int __seed, struct random_data *__buf)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)));
extern int initstate_r (unsigned int __seed, char *__restrict __statebuf,
   size_t __statelen,
   struct random_data *__restrict __buf)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2, 4)));
extern int setstate_r (char *__restrict __statebuf,
         struct random_data *__restrict __buf)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int rand (void) __attribute__ ((__nothrow__ , __leaf__));
extern void srand (unsigned int __seed) __attribute__ ((__nothrow__ , __leaf__));
extern int rand_r (unsigned int *__seed) __attribute__ ((__nothrow__ , __leaf__));
extern double drand48 (void) __attribute__ ((__nothrow__ , __leaf__));
extern double erand48 (unsigned short int __xsubi[3]) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern long int lrand48 (void) __attribute__ ((__nothrow__ , __leaf__));
extern long int nrand48 (unsigned short int __xsubi[3])
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern long int mrand48 (void) __attribute__ ((__nothrow__ , __leaf__));
extern long int jrand48 (unsigned short int __xsubi[3])
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern void srand48 (long int __seedval) __attribute__ ((__nothrow__ , __leaf__));
extern unsigned short int *seed48 (unsigned short int __seed16v[3])
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern void lcong48 (unsigned short int __param[7]) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
struct drand48_data
  {
    unsigned short int __x[3];
    unsigned short int __old_x[3];
    unsigned short int __c;
    unsigned short int __init;
    __extension__ unsigned long long int __a;
  };
extern int drand48_r (struct drand48_data *__restrict __buffer,
        double *__restrict __result) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int erand48_r (unsigned short int __xsubi[3],
        struct drand48_data *__restrict __buffer,
        double *__restrict __result) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int lrand48_r (struct drand48_data *__restrict __buffer,
        long int *__restrict __result)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int nrand48_r (unsigned short int __xsubi[3],
        struct drand48_data *__restrict __buffer,
        long int *__restrict __result)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int mrand48_r (struct drand48_data *__restrict __buffer,
        long int *__restrict __result)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int jrand48_r (unsigned short int __xsubi[3],
        struct drand48_data *__restrict __buffer,
        long int *__restrict __result)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int srand48_r (long int __seedval, struct drand48_data *__buffer)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)));
extern int seed48_r (unsigned short int __seed16v[3],
       struct drand48_data *__buffer) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int lcong48_r (unsigned short int __param[7],
        struct drand48_data *__buffer)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern __uint32_t arc4random (void)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern void arc4random_buf (void *__buf, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern __uint32_t arc4random_uniform (__uint32_t __upper_bound)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern void *malloc (size_t __size) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__))
     __attribute__ ((__alloc_size__ (1))) __attribute__ ((__warn_unused_result__));
extern void *calloc (size_t __nmemb, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__)) __attribute__ ((__alloc_size__ (1, 2))) __attribute__ ((__warn_unused_result__));
extern void *realloc (void *__ptr, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__)) __attribute__ ((__alloc_size__ (2)));
extern void free (void *__ptr) __attribute__ ((__nothrow__ , __leaf__));
extern void *reallocarray (void *__ptr, size_t __nmemb, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__))
     __attribute__ ((__alloc_size__ (2, 3)))
    __attribute__ ((__malloc__ (__builtin_free, 1)));
extern void *reallocarray (void *__ptr, size_t __nmemb, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__ (reallocarray, 1)));

extern void *alloca (size_t __size) __attribute__ ((__nothrow__ , __leaf__));

extern void *valloc (size_t __size) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__))
     __attribute__ ((__alloc_size__ (1))) __attribute__ ((__warn_unused_result__));
extern int posix_memalign (void **__memptr, size_t __alignment, size_t __size)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern void abort (void) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__)) __attribute__ ((__cold__));
extern int atexit (void (*__func) (void)) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int on_exit (void (*__func) (int __status, void *__arg), void *__arg)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern void exit (int __status) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));
extern void _Exit (int __status) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__noreturn__));
extern char *getenv (const char *__name) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern int putenv (char *__string) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int setenv (const char *__name, const char *__value, int __replace)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)));
extern int unsetenv (const char *__name) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int clearenv (void) __attribute__ ((__nothrow__ , __leaf__));
extern char *mktemp (char *__template) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int mkstemp (char *__template) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern int mkstemps (char *__template, int __suffixlen) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern char *mkdtemp (char *__template) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern int system (const char *__command) __attribute__ ((__warn_unused_result__));
extern char *realpath (const char *__restrict __name,
         char *__restrict __resolved) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
typedef int (*__compar_fn_t) (const void *, const void *);
extern void *bsearch (const void *__key, const void *__base,
        size_t __nmemb, size_t __size, __compar_fn_t __compar)
     __attribute__ ((__nonnull__ (1, 2, 5))) __attribute__ ((__warn_unused_result__));
extern __inline __attribute__ ((__gnu_inline__)) void *
bsearch (const void *__key, const void *__base, size_t __nmemb, size_t __size,
  __compar_fn_t __compar)
{
  const void *__p;
  int __comparison;
  while (__nmemb)
    {
      __p = (const void *) (((const char *) __base) + ((__nmemb >> 1) * __size));
      __comparison = (*__compar) (__key, __p);
      if (__comparison == 0)
 {
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wcast-qual"
   return (void *) __p;
#pragma GCC diagnostic pop
 }
      if (__comparison > 0)
 {
   __base = ((const char *) __p) + __size;
   --__nmemb;
 }
      __nmemb >>= 1;
    }
  return ((void *)0);
}
extern void qsort (void *__base, size_t __nmemb, size_t __size,
     __compar_fn_t __compar) __attribute__ ((__nonnull__ (1, 4)));
extern int abs (int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
extern long int labs (long int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
__extension__ extern long long int llabs (long long int __x)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
extern div_t div (int __numer, int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
extern ldiv_t ldiv (long int __numer, long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
__extension__ extern lldiv_t lldiv (long long int __numer,
        long long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) __attribute__ ((__warn_unused_result__));
extern char *ecvt (double __value, int __ndigit, int *__restrict __decpt,
     int *__restrict __sign) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4))) __attribute__ ((__warn_unused_result__));
extern char *fcvt (double __value, int __ndigit, int *__restrict __decpt,
     int *__restrict __sign) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4))) __attribute__ ((__warn_unused_result__));
extern char *gcvt (double __value, int __ndigit, char *__buf)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3))) __attribute__ ((__warn_unused_result__));
extern char *qecvt (long double __value, int __ndigit,
      int *__restrict __decpt, int *__restrict __sign)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4))) __attribute__ ((__warn_unused_result__));
extern char *qfcvt (long double __value, int __ndigit,
      int *__restrict __decpt, int *__restrict __sign)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4))) __attribute__ ((__warn_unused_result__));
extern char *qgcvt (long double __value, int __ndigit, char *__buf)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3))) __attribute__ ((__warn_unused_result__));
extern int ecvt_r (double __value, int __ndigit, int *__restrict __decpt,
     int *__restrict __sign, char *__restrict __buf,
     size_t __len) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4, 5)));
extern int fcvt_r (double __value, int __ndigit, int *__restrict __decpt,
     int *__restrict __sign, char *__restrict __buf,
     size_t __len) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4, 5)));
extern int qecvt_r (long double __value, int __ndigit,
      int *__restrict __decpt, int *__restrict __sign,
      char *__restrict __buf, size_t __len)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4, 5)));
extern int qfcvt_r (long double __value, int __ndigit,
      int *__restrict __decpt, int *__restrict __sign,
      char *__restrict __buf, size_t __len)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (3, 4, 5)));
extern int mblen (const char *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int mbtowc (wchar_t *__restrict __pwc,
     const char *__restrict __s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int wctomb (char *__s, wchar_t __wchar) __attribute__ ((__nothrow__ , __leaf__));
extern size_t mbstowcs (wchar_t *__restrict __pwcs,
   const char *__restrict __s, size_t __n) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__read_only__, 2)));
extern size_t wcstombs (char *__restrict __s,
   const wchar_t *__restrict __pwcs, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__access__ (__write_only__, 1, 3)))
  __attribute__ ((__access__ (__read_only__, 2)));
extern int rpmatch (const char *__response) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__warn_unused_result__));
extern int getsubopt (char **__restrict __optionp,
        char *const *__restrict __tokens,
        char **__restrict __valuep)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2, 3))) __attribute__ ((__warn_unused_result__));
extern int getloadavg (double __loadavg[], int __nelem)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern __inline __attribute__ ((__gnu_inline__)) double
__attribute__ ((__nothrow__ , __leaf__)) atof (const char *__nptr)
{
  return strtod (__nptr, (char **) ((void *)0));
}
extern char *__realpath_chk (const char *__restrict __name,
        char *__restrict __resolved,
        size_t __resolvedlen) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern char *__realpath_alias (const char *__restrict __name, char *__restrict __resolved) __asm__ ("" "realpath") __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern char *__realpath_chk_warn (const char *__restrict __name, char *__restrict __resolved, size_t __resolvedlen) __asm__ ("" "__realpath_chk") __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__))
     __attribute__((__warning__ ("second argument of realpath must be either NULL or at " "least PATH_MAX bytes long buffer")));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) char *
__attribute__ ((__nothrow__ , __leaf__)) realpath (const char *__restrict __name, char * __restrict __resolved)
{
  size_t __sz = __builtin_object_size (__resolved, 2 > 1);
  if (__sz == (size_t) -1)
    return __realpath_alias (__name, __resolved);
  return __realpath_chk (__name, __resolved, __sz);
}
extern int __ptsname_r_chk (int __fd, char *__buf, size_t __buflen,
       size_t __nreal) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)))
    __attribute__ ((__access__ (__write_only__, 2, 3)));
extern int __ptsname_r_alias (int __fd, char *__buf, size_t __buflen) __asm__ ("" "ptsname_r") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__ ((__nonnull__ (2))) __attribute__ ((__access__ (__write_only__, 2, 3)));
extern int __ptsname_r_chk_warn (int __fd, char *__buf, size_t __buflen, size_t __nreal) __asm__ ("" "__ptsname_r_chk") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__ ((__nonnull__ (2))) __attribute__((__warning__ ("ptsname_r called with buflen bigger than " "size of buf")));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) int
__attribute__ ((__nothrow__ , __leaf__)) ptsname_r (int __fd, char * __buf, size_t __buflen)
    
{
  return (((__builtin_constant_p (__builtin_object_size (__buf, 2 > 1)) && (__builtin_object_size (__buf, 2 > 1)) == (long unsigned int) -1) || (((__typeof (__buflen)) 0 < (__typeof (__buflen)) -1 || (__builtin_constant_p (__buflen) && (__buflen) > 0)) && __builtin_constant_p ((((long unsigned int) (__buflen)) <= ((__builtin_object_size (__buf, 2 > 1))) / ((sizeof (char))))) && (((long unsigned int) (__buflen)) <= ((__builtin_object_size (__buf, 2 > 1))) / ((sizeof (char)))))) ? __ptsname_r_alias (__fd, __buf, __buflen) : ((((__typeof (__buflen)) 0 < (__typeof (__buflen)) -1 || (__builtin_constant_p (__buflen) && (__buflen) > 0)) && __builtin_constant_p ((((long unsigned int) (__buflen)) <= (__builtin_object_size (__buf, 2 > 1)) / (sizeof (char)))) && !(((long unsigned int) (__buflen)) <= (__builtin_object_size (__buf, 2 > 1)) / (sizeof (char)))) ? __ptsname_r_chk_warn (__fd, __buf, __buflen, __builtin_object_size (__buf, 2 > 1)) : __ptsname_r_chk (__fd, __buf, __buflen, __builtin_object_size (__buf, 2 > 1))));
}
extern int __wctomb_chk (char *__s, wchar_t __wchar, size_t __buflen)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern int __wctomb_alias (char *__s, wchar_t __wchar) __asm__ ("" "wctomb") __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__warn_unused_result__));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) __attribute__ ((__warn_unused_result__)) int
__attribute__ ((__nothrow__ , __leaf__)) wctomb (char * __s, wchar_t __wchar)
{
  if (__builtin_object_size (__s, 2 > 1) != (size_t) -1
      && 16 > __builtin_object_size (__s, 2 > 1))
    return __wctomb_chk (__s, __wchar, __builtin_object_size (__s, 2 > 1));
  return __wctomb_alias (__s, __wchar);
}
extern size_t __mbstowcs_chk (wchar_t *__restrict __dst,
         const char *__restrict __src,
         size_t __len, size_t __dstlen) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 3))) __attribute__ ((__access__ (__read_only__, 2)));
extern size_t __mbstowcs_nulldst (wchar_t *__restrict __dst, const char *__restrict __src, size_t __len) __asm__ ("" "mbstowcs") __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__read_only__, 2)));
extern size_t __mbstowcs_alias (wchar_t *__restrict __dst, const char *__restrict __src, size_t __len) __asm__ ("" "mbstowcs") __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__write_only__, 1, 3))) __attribute__ ((__access__ (__read_only__, 2)));
extern size_t __mbstowcs_chk_warn (wchar_t *__restrict __dst, const char *__restrict __src, size_t __len, size_t __dstlen) __asm__ ("" "__mbstowcs_chk") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__((__warning__ ("mbstowcs called with dst buffer smaller than len " "* sizeof (wchar_t)")));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) size_t
__attribute__ ((__nothrow__ , __leaf__)) mbstowcs (wchar_t * __restrict __dst, const char *__restrict __src, size_t __len)
    
{
  if (__builtin_constant_p (__dst == ((void *)0)) && __dst == ((void *)0))
    return __mbstowcs_nulldst (__dst, __src, __len);
  else
    return (((__builtin_constant_p (__builtin_object_size (__dst, 2 > 1)) && (__builtin_object_size (__dst, 2 > 1)) == (long unsigned int) -1) || (((__typeof (__len)) 0 < (__typeof (__len)) -1 || (__builtin_constant_p (__len) && (__len) > 0)) && __builtin_constant_p ((((long unsigned int) (__len)) <= ((__builtin_object_size (__dst, 2 > 1))) / ((sizeof (wchar_t))))) && (((long unsigned int) (__len)) <= ((__builtin_object_size (__dst, 2 > 1))) / ((sizeof (wchar_t)))))) ? __mbstowcs_alias (__dst, __src, __len) : ((((__typeof (__len)) 0 < (__typeof (__len)) -1 || (__builtin_constant_p (__len) && (__len) > 0)) && __builtin_constant_p ((((long unsigned int) (__len)) <= (__builtin_object_size (__dst, 2 > 1)) / (sizeof (wchar_t)))) && !(((long unsigned int) (__len)) <= (__builtin_object_size (__dst, 2 > 1)) / (sizeof (wchar_t)))) ? __mbstowcs_chk_warn (__dst, __src, __len, (__builtin_object_size (__dst, 2 > 1)) / (sizeof (wchar_t))) : __mbstowcs_chk (__dst, __src, __len, (__builtin_object_size (__dst, 2 > 1)) / (sizeof (wchar_t)))));
}
extern size_t __wcstombs_chk (char *__restrict __dst,
         const wchar_t *__restrict __src,
         size_t __len, size_t __dstlen) __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__access__ (__write_only__, 1, 3))) __attribute__ ((__access__ (__read_only__, 2)));
extern size_t __wcstombs_alias (char *__restrict __dst, const wchar_t *__restrict __src, size_t __len) __asm__ ("" "wcstombs") __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__access__ (__write_only__, 1, 3))) __attribute__ ((__access__ (__read_only__, 2)));
extern size_t __wcstombs_chk_warn (char *__restrict __dst, const wchar_t *__restrict __src, size_t __len, size_t __dstlen) __asm__ ("" "__wcstombs_chk") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__((__warning__ ("wcstombs called with dst buffer smaller than len")));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) size_t
__attribute__ ((__nothrow__ , __leaf__)) wcstombs (char * __restrict __dst, const wchar_t *__restrict __src, size_t __len)
{
  return (((__builtin_constant_p (__builtin_object_size (__dst, 2 > 1)) && (__builtin_object_size (__dst, 2 > 1)) == (long unsigned int) -1) || (((__typeof (__len)) 0 < (__typeof (__len)) -1 || (__builtin_constant_p (__len) && (__len) > 0)) && __builtin_constant_p ((((long unsigned int) (__len)) <= ((__builtin_object_size (__dst, 2 > 1))) / ((sizeof (char))))) && (((long unsigned int) (__len)) <= ((__builtin_object_size (__dst, 2 > 1))) / ((sizeof (char)))))) ? __wcstombs_alias (__dst, __src, __len) : ((((__typeof (__len)) 0 < (__typeof (__len)) -1 || (__builtin_constant_p (__len) && (__len) > 0)) && __builtin_constant_p ((((long unsigned int) (__len)) <= (__builtin_object_size (__dst, 2 > 1)) / (sizeof (char)))) && !(((long unsigned int) (__len)) <= (__builtin_object_size (__dst, 2 > 1)) / (sizeof (char)))) ? __wcstombs_chk_warn (__dst, __src, __len, __builtin_object_size (__dst, 2 > 1)) : __wcstombs_chk (__dst, __src, __len, __builtin_object_size (__dst, 2 > 1))));
}


extern void *memcpy (void *__restrict __dest, const void *__restrict __src,
       size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern void *memmove (void *__dest, const void *__src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern void *memccpy (void *__restrict __dest, const void *__restrict __src,
        int __c, size_t __n)
    __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2))) __attribute__ ((__access__ (__write_only__, 1, 4)));
extern void *memset (void *__s, int __c, size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int memcmp (const void *__s1, const void *__s2, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern int __memcmpeq (const void *__s1, const void *__s2, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern void *memchr (const void *__s, int __c, size_t __n)
      __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern char *strcpy (char *__restrict __dest, const char *__restrict __src)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strncpy (char *__restrict __dest,
        const char *__restrict __src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strcat (char *__restrict __dest, const char *__restrict __src)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strncat (char *__restrict __dest, const char *__restrict __src,
        size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern int strcmp (const char *__s1, const char *__s2)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern int strncmp (const char *__s1, const char *__s2, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern int strcoll (const char *__s1, const char *__s2)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern size_t strxfrm (char *__restrict __dest,
         const char *__restrict __src, size_t __n)
    __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2))) __attribute__ ((__access__ (__write_only__, 1, 3)));
struct __locale_struct
{
  struct __locale_data *__locales[13];
  const unsigned short int *__ctype_b;
  const int *__ctype_tolower;
  const int *__ctype_toupper;
  const char *__names[13];
};
typedef struct __locale_struct *__locale_t;
typedef __locale_t locale_t;
extern int strcoll_l (const char *__s1, const char *__s2, locale_t __l)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2, 3)));
extern size_t strxfrm_l (char *__dest, const char *__src, size_t __n,
    locale_t __l) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2, 4)))
     __attribute__ ((__access__ (__write_only__, 1, 3)));
extern char *strdup (const char *__s)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__)) __attribute__ ((__nonnull__ (1)));
extern char *strndup (const char *__string, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__malloc__)) __attribute__ ((__nonnull__ (1)));
extern char *strchr (const char *__s, int __c)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern char *strrchr (const char *__s, int __c)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern char *strchrnul (const char *__s, int __c)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern size_t strcspn (const char *__s, const char *__reject)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern size_t strspn (const char *__s, const char *__accept)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strpbrk (const char *__s, const char *__accept)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strstr (const char *__haystack, const char *__needle)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strtok (char *__restrict __s, const char *__restrict __delim)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)));
extern char *__strtok_r (char *__restrict __s,
    const char *__restrict __delim,
    char **__restrict __save_ptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2, 3)));
extern char *strtok_r (char *__restrict __s, const char *__restrict __delim,
         char **__restrict __save_ptr)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2, 3)));
extern char *strcasestr (const char *__haystack, const char *__needle)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern void *memmem (const void *__haystack, size_t __haystacklen,
       const void *__needle, size_t __needlelen)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 3)))
    __attribute__ ((__access__ (__read_only__, 1, 2)))
    __attribute__ ((__access__ (__read_only__, 3, 4)));
extern void *__mempcpy (void *__restrict __dest,
   const void *__restrict __src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern void *mempcpy (void *__restrict __dest,
        const void *__restrict __src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern size_t strlen (const char *__s)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern size_t strnlen (const char *__string, size_t __maxlen)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern char *strerror (int __errnum) __attribute__ ((__nothrow__ , __leaf__));
extern int strerror_r (int __errnum, char *__buf, size_t __buflen) __asm__ ("" "__xpg_strerror_r") __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (2)))
    __attribute__ ((__access__ (__write_only__, 2, 3)));
extern char *strerror_l (int __errnum, locale_t __l) __attribute__ ((__nothrow__ , __leaf__));

extern int bcmp (const void *__s1, const void *__s2, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern void bcopy (const void *__src, void *__dest, size_t __n)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern void bzero (void *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern char *index (const char *__s, int __c)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern char *rindex (const char *__s, int __c)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1)));
extern int ffs (int __i) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__));
extern int ffsl (long int __l) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__));
__extension__ extern int ffsll (long long int __ll)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__));
extern int strcasecmp (const char *__s1, const char *__s2)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern int strncasecmp (const char *__s1, const char *__s2, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2)));
extern int strcasecmp_l (const char *__s1, const char *__s2, locale_t __loc)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2, 3)));
extern int strncasecmp_l (const char *__s1, const char *__s2,
     size_t __n, locale_t __loc)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__pure__)) __attribute__ ((__nonnull__ (1, 2, 4)));

extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void
__attribute__ ((__nothrow__ , __leaf__)) bcopy (const void *__src, void *__dest, size_t __len)
{
  (void) __builtin___memmove_chk (__dest, __src, __len,
      __builtin_object_size (__dest, 0));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void
__attribute__ ((__nothrow__ , __leaf__)) bzero (void *__dest, size_t __len)
{
  (void) __builtin___memset_chk (__dest, '\0', __len,
     __builtin_object_size (__dest, 0));
}
extern void explicit_bzero (void *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)))
    __attribute__ ((__access__ (__write_only__, 1, 2)));
extern char *strsep (char **__restrict __stringp,
       const char *__restrict __delim)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *strsignal (int __sig) __attribute__ ((__nothrow__ , __leaf__));
extern char *__stpcpy (char *__restrict __dest, const char *__restrict __src)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *stpcpy (char *__restrict __dest, const char *__restrict __src)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *__stpncpy (char *__restrict __dest,
   const char *__restrict __src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern char *stpncpy (char *__restrict __dest,
        const char *__restrict __src, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2)));
extern size_t strlcpy (char *__restrict __dest,
         const char *__restrict __src, size_t __n)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2))) __attribute__ ((__access__ (__write_only__, 1, 3)));
extern size_t strlcat (char *__restrict __dest,
         const char *__restrict __src, size_t __n)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1, 2))) __attribute__ ((__access__ (__read_write__, 1, 3)));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void *
__attribute__ ((__nothrow__ , __leaf__)) memcpy (void *__restrict __dest, const void *__restrict __src, size_t __len)
{
  return __builtin___memcpy_chk (__dest, __src, __len,
     __builtin_object_size (__dest, 0));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void *
__attribute__ ((__nothrow__ , __leaf__)) memmove (void *__dest, const void *__src, size_t __len)
{
  return __builtin___memmove_chk (__dest, __src, __len,
      __builtin_object_size (__dest, 0));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void *
__attribute__ ((__nothrow__ , __leaf__)) memset (void *__dest, int __ch, size_t __len)
{
  return __builtin___memset_chk (__dest, __ch, __len,
     __builtin_object_size (__dest, 0));
}
void __explicit_bzero_chk (void *__dest, size_t __len, size_t __destlen)
  __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1))) __attribute__ ((__access__ (__write_only__, 1, 2)));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) void
__attribute__ ((__nothrow__ , __leaf__)) explicit_bzero (void *__dest, size_t __len)
{
  __explicit_bzero_chk (__dest, __len, __builtin_object_size (__dest, 0));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) strcpy (char * __restrict __dest, const char *__restrict __src)
    
{
  return __builtin___strcpy_chk (__dest, __src, __builtin_object_size (__dest, 2 > 1));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) stpcpy (char * __restrict __dest, const char *__restrict __src)
    
{
  return __builtin___stpcpy_chk (__dest, __src, __builtin_object_size (__dest, 2 > 1));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) strncpy (char * __restrict __dest, const char *__restrict __src, size_t __len)
    
{
  return __builtin___strncpy_chk (__dest, __src, __len,
      __builtin_object_size (__dest, 2 > 1));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) stpncpy (char * __dest, const char *__src, size_t __n)
    
{
  return __builtin___stpncpy_chk (__dest, __src, __n,
      __builtin_object_size (__dest, 2 > 1));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) strcat (char * __restrict __dest, const char *__restrict __src)
    
{
  return __builtin___strcat_chk (__dest, __src, __builtin_object_size (__dest, 2 > 1));
}
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) char *
__attribute__ ((__nothrow__ , __leaf__)) strncat (char * __restrict __dest, const char *__restrict __src, size_t __len)
    
{
  return __builtin___strncat_chk (__dest, __src, __len,
      __builtin_object_size (__dest, 2 > 1));
}
extern size_t __strlcpy_chk (char *__dest, const char *__src, size_t __n,
        size_t __destlen) __attribute__ ((__nothrow__ , __leaf__));
extern size_t __strlcpy_alias (char *__dest, const char *__src, size_t __n) __asm__ ("" "strlcpy") __attribute__ ((__nothrow__ , __leaf__));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) size_t
__attribute__ ((__nothrow__ , __leaf__)) strlcpy (char * __restrict __dest, const char *__restrict __src, size_t __n)
    
{
  if (__builtin_object_size (__dest, 2 > 1) != (size_t) -1
      && (!__builtin_constant_p (__n > __builtin_object_size (__dest, 2 > 1))
   || __n > __builtin_object_size (__dest, 2 > 1)))
    return __strlcpy_chk (__dest, __src, __n, __builtin_object_size (__dest, 2 > 1));
  return __strlcpy_alias (__dest, __src, __n);
}
extern size_t __strlcat_chk (char *__dest, const char *__src, size_t __n,
        size_t __destlen) __attribute__ ((__nothrow__ , __leaf__));
extern size_t __strlcat_alias (char *__dest, const char *__src, size_t __n) __asm__ ("" "strlcat") __attribute__ ((__nothrow__ , __leaf__));
extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) __attribute__ ((__artificial__)) size_t
__attribute__ ((__nothrow__ , __leaf__)) strlcat (char * __restrict __dest, const char *__restrict __src, size_t __n)
{
  if (__builtin_object_size (__dest, 2 > 1) != (size_t) -1
      && (!__builtin_constant_p (__n > __builtin_object_size (__dest, 2 > 1))
   || __n > __builtin_object_size (__dest, 2 > 1)))
    return __strlcat_chk (__dest, __src, __n, __builtin_object_size (__dest, 2 > 1));
  return __strlcat_alias (__dest, __src, __n);
}

 
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpedantic"
typedef __uint8_t uint8_t;
typedef __uint16_t uint16_t;
typedef __uint32_t uint32_t;
typedef __uint64_t uint64_t;
typedef __int_least8_t int_least8_t;
typedef __int_least16_t int_least16_t;
typedef __int_least32_t int_least32_t;
typedef __int_least64_t int_least64_t;
typedef __uint_least8_t uint_least8_t;
typedef __uint_least16_t uint_least16_t;
typedef __uint_least32_t uint_least32_t;
typedef __uint_least64_t uint_least64_t;
typedef signed char int_fast8_t;
typedef long int int_fast16_t;
typedef long int int_fast32_t;
typedef long int int_fast64_t;
typedef unsigned char uint_fast8_t;
typedef unsigned long int uint_fast16_t;
typedef unsigned long int uint_fast32_t;
typedef unsigned long int uint_fast64_t;
typedef long int intptr_t;
typedef unsigned long int uintptr_t;
typedef __intmax_t intmax_t;
typedef __uintmax_t uintmax_t;
#pragma GCC diagnostic pop
typedef int __gwchar_t;

typedef struct
  {
    long int quot;
    long int rem;
  } imaxdiv_t;
extern intmax_t imaxabs (intmax_t __n) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__));
extern imaxdiv_t imaxdiv (intmax_t __numer, intmax_t __denom)
      __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__));
extern intmax_t strtoimax (const char *__restrict __nptr,
      char **__restrict __endptr, int __base) __attribute__ ((__nothrow__ , __leaf__));
extern uintmax_t strtoumax (const char *__restrict __nptr,
       char ** __restrict __endptr, int __base) __attribute__ ((__nothrow__ , __leaf__));
extern intmax_t wcstoimax (const __gwchar_t *__restrict __nptr,
      __gwchar_t **__restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__));
extern uintmax_t wcstoumax (const __gwchar_t *__restrict __nptr,
       __gwchar_t ** __restrict __endptr, int __base)
     __attribute__ ((__nothrow__ , __leaf__));

struct cpu;
struct emul;
struct machine;
struct memory;
enum Endianness
{
 BigEndian = 0,
 LittleEndian
};
int load_bootblock(struct machine *m, struct cpu *cpu,
 int *n_loadp, char ***load_namesp);
int apple_load_bootblock(struct machine *m, struct cpu *cpu,
 int disk_id, int disk_type, int *n_loadp, char ***load_namesp);
int iso_load_bootblock(struct machine *m, struct cpu *cpu,
 int disk_id, int disk_type, int iso_type, unsigned char *buf,
 int *n_loadp, char ***load_namesp);
int decstation_prom_emul(struct cpu *cpu);
extern int *debugmsg_current_verbosity;
extern int debugmsg_break_on_error;
void debug_indentation(int diff);
void debug(const char *fmt, ...);
void fatal(const char *fmt, ...);
void debugmsg_init();
int debugmsg_register_subsystem(const char* name);
void debugmsg_change_settings(char *subsystem_name, char *n);
void debugmsg_print_settings(const char *subsystem_name);
void debugmsg_add_verbosity_level(int subsystem, int verbosity_delta);
void debugmsg_set_verbosity_level(int subsystem, int verbosity);
void debugmsg(int subsystem, const char *name, int verbosity_required, const char *fmt, ...);
void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name, int verbosity_required, const char *fmt, ...);
int debugmsg_set_breakpoint(const char *subsystem_name, int level);
void debugmsg_print_breakpoints(void);
void dreamcast_machine_setup(struct machine *);
void dreamcast_emul(struct cpu *cpu);
void dreamcast_descramble(char *from, char *to);
int file_n_executables_loaded(void);
void file_load(struct machine *machine, struct memory *mem,
 char *filename, uint64_t *entrypointp,
 int arch, uint64_t *gpp, int *byte_order, uint64_t *tocp);
void luna88kprom_init(struct machine *machine);
int luna88kprom_emul(struct cpu *cpu);
void color_prompt();
void color_normal();
void color_error(_Bool bold);
void color_debugmsg_subsystem();
void color_debugmsg_name();
void color_banner();
void color_pc_indicator();
const char* color_symbol_ptr();
const char* color_normal_ptr();
unsigned long long mystrtoull(const char *s, char **endp, int base);
int mymkstemp(char *templ);
void print_separator_line(void);
uint64_t size_to_mask(uint64_t size);
void mvmeprom_init(struct machine *machine);
int mvmeprom_emul(struct cpu *cpu);
int playstation2_sifbios_emul(struct cpu *cpu);
void sh_ipl_g_emul_init(struct machine *machine);
int sh_ipl_g_emul(struct cpu *);
void yamon_machine_setup(struct machine *machine, uint64_t env);
int yamon_emul(struct cpu *);
typedef u_int16_t pci_vendor_id_t;
typedef u_int16_t pci_product_id_t;
typedef u_int8_t pci_class_t;
typedef u_int8_t pci_subclass_t;
typedef u_int8_t pci_interface_t;
typedef u_int8_t pci_revision_t;
typedef u_int8_t pci_intr_latency_t;
typedef u_int8_t pci_intr_grant_t;
typedef u_int8_t pci_intr_pin_t;
typedef u_int8_t pci_intr_line_t;
struct pci_vpd_smallres {
 uint8_t vpdres_byte0;
} __attribute__((__packed__));
struct pci_vpd_largeres {
 uint8_t vpdres_byte0;
 uint8_t vpdres_len_lsb;
 uint8_t vpdres_len_msb;
} __attribute__((__packed__));
struct pci_vpd {
 uint8_t vpd_key0;
 uint8_t vpd_key1;
 uint8_t vpd_len;
} __attribute__((__packed__));
struct machine;
struct memory;
struct pci_device;
struct pci_data;
void bus_pci_decompose_1(uint32_t t, int *bus, int *dev, int *func, int *reg);
void bus_pci_setaddr(struct cpu *cpu, struct pci_data *pci_data,
 int bus, int device, int function, int reg);
void bus_pci_data_access(struct cpu *cpu, struct pci_data *pci_data,
 uint64_t *data, int len, int writeflag);
struct pci_data *bus_pci_init(struct machine *machine, const char *irq_path,
 uint64_t pci_actual_io_offset, uint64_t pci_actual_mem_offset,
 uint64_t pci_portbase, uint64_t pci_membase, const char *pci_irqbase,
 uint64_t isa_portbase, uint64_t isa_membase, const char *isa_irqbase);
void bus_pci_add(struct machine *machine, struct pci_data *pci_data,
 struct memory *mem, int bus, int device, int function,
 const char *name);
struct emul;
void console_deinit_main(void);
void console_sigcont(int x);
void console_makeavail(int handle, char ch);
int console_charavail(int handle);
_Bool console_any_input_available(struct emul *emul);
int console_readchar(int handle);
void console_putchar(int handle, int ch);
void console_flush(void);
void console_mouse_coordinate_update(int dx, int dy, int fb_nr);
void console_mouse_button(int, int);
void console_getmouse(int *dx, int *dy, int *buttons, int *fb_nr);
void console_slave(const char *arg);
int console_are_slaves_allowed(void);
int console_warn_if_slaves_are_needed(int init);
int console_start_slave(struct machine *, const char *consolename, int use_for_input);
int console_start_slave_inputonly(struct machine *, const char *consolename,
 int use_for_input);
int console_change_inputability(int handle, int inputability);
void console_init_main(struct emul *);
void console_debug_dump(struct machine *);
void console_allow_slaves(int);
void console_init(void);
void console_deinit(void);

struct timezone
  {
    int tz_minuteswest;
    int tz_dsttime;
  };
extern int gettimeofday (struct timeval *__restrict __tv,
    void *__restrict __tz) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int settimeofday (const struct timeval *__tv,
    const struct timezone *__tz)
     __attribute__ ((__nothrow__ , __leaf__));
extern int adjtime (const struct timeval *__delta,
      struct timeval *__olddelta) __attribute__ ((__nothrow__ , __leaf__));
enum __itimer_which
  {
    ITIMER_REAL = 0,
    ITIMER_VIRTUAL = 1,
    ITIMER_PROF = 2
  };
struct itimerval
  {
    struct timeval it_interval;
    struct timeval it_value;
  };
typedef int __itimer_which_t;
extern int getitimer (__itimer_which_t __which,
        struct itimerval *__value) __attribute__ ((__nothrow__ , __leaf__));
extern int setitimer (__itimer_which_t __which,
        const struct itimerval *__restrict __new,
        struct itimerval *__restrict __old) __attribute__ ((__nothrow__ , __leaf__));
extern int utimes (const char *__file, const struct timeval __tvp[2])
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int lutimes (const char *__file, const struct timeval __tvp[2])
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__nonnull__ (1)));
extern int futimes (int __fd, const struct timeval __tvp[2]) __attribute__ ((__nothrow__ , __leaf__));

struct timer;
struct timer *timer_add(double freq, void (*timer_tick)(struct timer *timer,
 void *extra), void *extra);
void timer_remove(struct timer *t);
void timer_update_frequency(struct timer *t, double new_freq);
void timer_start(void);
void timer_stop(void);
void timer_init(void);
struct physpage_ranges {
 uint32_t next_ofs;
 uint32_t n_entries_used;
 uint16_t base[20];
 uint16_t length[20];
 uint16_t count[20];
};
struct alpha_pcb {
 uint64_t apcb_ksp;
 uint64_t apcb_usp;
 uint64_t apcb_ptbr;
 uint32_t apcb_cpc;
 uint32_t apcb_asn;
 uint64_t apcb_unique;
 uint64_t apcb_flags;
 uint64_t apcb_decrsv0;
 uint64_t apcb_decrsv1;
};
struct alpha_logout_area {
 uint32_t la_frame_size;
 uint32_t la_flags;
 uint32_t la_cpu_offset;
 uint32_t la_system_offset;
};
typedef unsigned long alpha_pt_entry_t;
struct alpha_cpu_type_def {
 const char *name;
 uint64_t pcs_type;
 int features;
 int implver;
 int icache_shift;
 int ilinesize;
 int iway;
 int dcache_shift;
 int dlinesize;
 int dway;
 int l2cache_shift;
 int l2linesize;
 int l2way;
};
struct cpu_family;
struct alpha_instr_call { void (*f)(struct cpu *, struct alpha_instr_call *); uintptr_t arg[3]; }; struct alpha_tc_physpage { struct alpha_instr_call ics[(1 << 11)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint64_t physaddr; }; struct alpha_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint64_t vaddr_page; uint64_t paddr_page; unsigned char *host_page; };
struct alpha_l3_64_table { unsigned char *host_load[1 << 17]; unsigned char *host_store[1 << 17]; uint64_t phys_addr[1 << 17]; uint8_t vaddr_to_tlbindex[1 << 17]; struct alpha_tc_physpage *phys_page[1 << 17]; struct alpha_l3_64_table *next; int refcount; }; struct alpha_l2_64_table { struct alpha_l3_64_table *l3[1 << 17]; struct alpha_l2_64_table *next; int refcount; };
struct alpha_cpu {
 struct alpha_cpu_type_def cpu_type;
 uint64_t r[32];
 uint64_t f[32];
 uint64_t fpcr;
 uint64_t pcc;
 uint64_t load_linked_addr;
 int ll_flag;
 int irq_asserted;
 uint64_t ps;
 uint64_t vptptr;
 uint64_t sysvalue;
 uint64_t mces;
 uint64_t kgp;
 uint64_t kentry[6];
 uint64_t ctx;
 struct alpha_pcb pcb;
 struct alpha_tc_physpage *cur_physpage; struct alpha_instr_call *cur_ic_page; struct alpha_instr_call *next_ic; struct alpha_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct alpha_instr_call *, int low_addr);
 struct alpha_vpg_tlb_entry vph_tlb_entry[128];
 struct alpha_l3_64_table *l3_64_dummy; struct alpha_l3_64_table *next_free_l3; struct alpha_l2_64_table *l2_64_dummy; struct alpha_l2_64_table *next_free_l2; struct alpha_l2_64_table *l1_64[1 << 17];
};
void alpha_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void alpha_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void alpha_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void alpha_init_64bit_dummy_tables(struct cpu *cpu);
int alpha_run_instr(struct cpu *cpu);
int alpha_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void alpha_cpu_family_init(struct cpu_family *);
void alpha_palcode_name(uint32_t palcode, char *buf, size_t buflen);
void alpha_palcode(struct cpu *cpu, uint32_t palcode);
int alpha_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct interrupt {
 void (*interrupt_assert)(struct interrupt *);
 void (*interrupt_deassert)(struct interrupt *);
 uint32_t line;
 void *extra;
 char *name;
};
void interrupt_handler_register(struct interrupt *templ);
void interrupt_handler_remove(const char *name);
int interrupt_handler_lookup(const char *name, struct interrupt *templ);
void interrupt_connect(struct interrupt *i, int exclusive);
void interrupt_disconnect(struct interrupt *i, int exclusive);
struct cpu_family;
struct arm_cpu_type_def {
 const char *name;
 uint32_t cpu_id;
 int flags;
 int icache_shift;
 int iway;
 int dcache_shift;
 int dway;
};
struct arm_instr_call { void (*f)(struct cpu *, struct arm_instr_call *); uintptr_t arg[3]; }; struct arm_tc_physpage { struct arm_instr_call ics[(1 << 10)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint32_t physaddr; }; struct arm_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint32_t vaddr_page; uint32_t paddr_page; unsigned char *host_page; };
struct arm_cpu {
 struct arm_cpu_type_def cpu_type;
 uint32_t of_emul_addr;
 void (*coproc[16])(struct cpu *, int opcode1,
        int opcode2, int l_bit, int crn, int crm,
        int rd);
 uint32_t r[16];
 uint32_t default_r8_r14[7];
 uint32_t fiq_r8_r14[7];
 uint32_t irq_r13_r14[2];
 uint32_t svc_r13_r14[2];
 uint32_t abt_r13_r14[2];
 uint32_t und_r13_r14[2];
 uint32_t tmp_pc;
 uint32_t tmp_pc_data[2];
 uint32_t tmp_branch;
 size_t flags;
 uint32_t cpsr;
 uint32_t spsr_svc;
 uint32_t spsr_abt;
 uint32_t spsr_und;
 uint32_t spsr_irq;
 uint32_t spsr_fiq;
 uint32_t cachetype;
 uint32_t control;
 uint32_t auxctrl;
 uint32_t ttb;
 uint32_t dacr;
 uint32_t fsr;
 uint32_t far;
 uint32_t pid;
 uint32_t cpar;
 uint32_t i80321_inten;
 uint32_t i80321_isteer;
 uint32_t i80321_isrc;
 uint32_t tmr0;
 uint32_t tmr1;
 struct interrupt tmr0_irq;
 struct interrupt tmr1_irq;
 uint32_t tcr0;
 uint32_t tcr1;
 uint32_t trr0;
 uint32_t trr1;
 uint32_t tisr;
 uint32_t wdtcr;
 uint32_t xsc1_pmnc;
 uint32_t xsc1_ccnt;
 uint32_t xsc1_pmn0;
 uint32_t xsc1_pmn1;
 uint32_t xsc2_pmnc;
 uint32_t xsc2_ccnt;
 uint32_t xsc2_inten;
 uint32_t xsc2_flag;
 uint32_t xsc2_evtsel;
 uint32_t xsc2_pmn0;
 uint32_t xsc2_pmn1;
 uint32_t xsc2_pmn2;
 uint32_t xsc2_pmn3;
 unsigned char *translation_table;
 uint32_t last_ttb;
 int irq_asserted;
 int rmw;
 uint32_t rmw_len;
 uint32_t rmw_addr;
 struct arm_tc_physpage *cur_physpage; struct arm_instr_call *cur_ic_page; struct arm_instr_call *next_ic; struct arm_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct arm_instr_call *, int low_addr);
 struct arm_vpg_tlb_entry vph_tlb_entry[384];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct arm_tc_physpage *phys_page[1048576]; uint16_t vaddr_to_tlbindex[1048576];
 uint32_t is_userpage[1048576/32];
 uint64_t ls_general;
};
void arm_setup_initial_translation_table(struct cpu *cpu, uint32_t ttb_addr);
void arm_translation_table_set_l1(struct cpu *cpu, uint32_t vaddr,
 uint32_t paddr);
void arm_translation_table_set_l1_b(struct cpu *cpu, uint32_t vaddr,
 uint32_t paddr);
void arm_exception(struct cpu *, int);
int arm_cpu_interpret_thumb_SLOW(struct cpu*);
int arm_run_instr(struct cpu *cpu);
void arm_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void arm_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void arm_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void arm_load_register_bank(struct cpu *cpu);
void arm_save_register_bank(struct cpu *cpu);
int arm_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void arm_cpu_family_init(struct cpu_family *);
void arm_coproc_15(struct cpu *cpu, int opcode1, int opcode2, int l_bit,
 int crn, int crm, int rd);
void arm_coproc_i80321_6(struct cpu *cpu, int opcode1, int opcode2, int l_bit,
 int crn, int crm, int rd);
void arm_coproc_xscale_14(struct cpu *cpu, int opcode1, int opcode2, int l_bit,
 int crn, int crm, int rd);
void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs);
void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw);
int arm_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
int arm_translate_v2p_mmu(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu_family;
struct i960_instr_call { void (*f)(struct cpu *, struct i960_instr_call *); uintptr_t arg[3]; }; struct i960_tc_physpage { struct i960_instr_call ics[(1 << 10)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint32_t physaddr; }; struct i960_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint32_t vaddr_page; uint32_t paddr_page; unsigned char *host_page; };
struct i960_cpu {
 uint32_t ac;
 uint32_t i960_pc;
 uint32_t tc;
 uint32_t r[32];
 int nr_of_valid_sfrs;
 uint32_t sfr[32];
 int irq_asserted;
 struct i960_tc_physpage *cur_physpage; struct i960_instr_call *cur_ic_page; struct i960_instr_call *next_ic; struct i960_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct i960_instr_call *, int low_addr);
 struct i960_vpg_tlb_entry vph_tlb_entry[128];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct i960_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
};
int i960_cpu_instruction_has_delayslot(struct cpu *cpu, unsigned char *ib);
int i960_run_instr(struct cpu *cpu);
void i960_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void i960_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void i960_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
int i960_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void i960_cpu_family_init(struct cpu_family *);
void i960_exception(struct cpu *cpu, int vector, int is_trap);
int i960_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu_family;
struct m88k_cpu_type_def {
 const char *name;
 int type;
 uint32_t pid;
};
struct m88k_instr_call { void (*f)(struct cpu *, struct m88k_instr_call *); uintptr_t arg[3]; }; struct m88k_tc_physpage { struct m88k_instr_call ics[(1 << 10)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint32_t physaddr; }; struct m88k_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint32_t vaddr_page; uint32_t paddr_page; unsigned char *host_page; };
struct m8820x_cmmu {
 uint32_t reg[0x1000 / sizeof(uint32_t)];
 uint32_t batc[10];
 uint32_t patc_v_and_control[56];
 uint32_t patc_p_and_supervisorbit[56];
 int patc_update_index;
};
struct m88k_cpu {
 struct m88k_cpu_type_def cpu_type;
 uint32_t r[32 +1];
 uint32_t zero_scratch;
 uint32_t cr[64];
 uint32_t fcr[64];
 int irq_asserted;
 struct m8820x_cmmu *cmmu[8];
 uint32_t dmt[2];
 uint32_t dmd[2];
 uint32_t dma[2];
 uint32_t delay_target;
 uint64_t idle_fold_installs[3];
 uint64_t idle_fold_n_taken_plain;
 uint64_t idle_fold_n_taken_n;
 uint64_t idle_fold_slot_runs;
 uint64_t idle_fold_in_delayslot;
 struct m88k_tc_physpage *cur_physpage; struct m88k_instr_call *cur_ic_page; struct m88k_instr_call *next_ic; struct m88k_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct m88k_instr_call *, int low_addr);
 struct m88k_vpg_tlb_entry vph_tlb_entry[128];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct m88k_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
 unsigned char *host_load_usr[1048576]; unsigned char *host_store_usr[1048576]; uint32_t phys_addr_usr[1048576]; struct m88k_tc_physpage *phys_page_usr[1048576]; uint8_t vaddr_to_tlbindex_usr[1048576];
};
int m88k_cpu_instruction_has_delayslot(struct cpu *cpu, unsigned char *ib);
int m88k_run_instr(struct cpu *cpu);
void m88k_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void m88k_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void m88k_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
int m88k_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void m88k_cpu_family_init(struct cpu_family *);
void m88k_ldcr(struct cpu *cpu, uint32_t *r32ptr, int cr);
void m88k_stcr(struct cpu *cpu, uint32_t value, int cr, int rte);
void m88k_fstcr(struct cpu *cpu, uint32_t value, int fcr);
void m88k_exception(struct cpu *cpu, int vector, int is_trap);
int m88k_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu_family;
struct emul;
struct machine;
struct timer;
struct mips_cpu_type_def {
 const char *name;
 int rev;
 int sub;
 char flags;
 char exc_model;
 char mmu_model;
 char isa_level;
 char isa_revision;
 int nr_of_tlb_entries;
 char instrs_per_cycle;
 int picache;
 int pilinesize;
 int piways;
 int pdcache;
 int pdlinesize;
 int pdways;
 int scache;
 int slinesize;
 int sways;
};
struct mips_tlb {
 uint64_t hi;
 uint64_t lo0;
 uint64_t lo1;
 uint64_t mask;
};
struct mips_coproc {
 int coproc_nr;
 uint64_t reg[32];
 struct mips_tlb *tlbs;
 int nr_of_tlbs;
 uint64_t fcr[32];
};
struct r3000_cache_line {
 uint32_t tag_paddr;
 int tag_valid;
};
struct mips_instr_call { void (*f)(struct cpu *, struct mips_instr_call *); uintptr_t arg[3]; }; struct mips_tc_physpage { struct mips_instr_call ics[(1 << 10)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint64_t physaddr; }; struct mips_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint64_t vaddr_page; uint64_t paddr_page; unsigned char *host_page; };
struct mips_l3_64_table { unsigned char *host_load[1 << 18]; unsigned char *host_store[1 << 18]; uint64_t phys_addr[1 << 18]; uint8_t vaddr_to_tlbindex[1 << 18]; struct mips_tc_physpage *phys_page[1 << 18]; struct mips_l3_64_table *next; int refcount; }; struct mips_l2_64_table { struct mips_l3_64_table *l3[1 << 17]; struct mips_l2_64_table *next; int refcount; };
enum mips_fold_id {
 MIPS_FOLD_MULTI_SW_2_LE, MIPS_FOLD_MULTI_SW_3_LE,
 MIPS_FOLD_MULTI_SW_4_LE, MIPS_FOLD_MULTI_SW_5_LE,
 MIPS_FOLD_MULTI_SW_2_BE, MIPS_FOLD_MULTI_SW_3_BE,
 MIPS_FOLD_MULTI_SW_4_BE, MIPS_FOLD_MULTI_SW_5_BE,
 MIPS_FOLD_MULTI_LW_2_LE, MIPS_FOLD_MULTI_LW_3_LE,
 MIPS_FOLD_MULTI_LW_4_LE, MIPS_FOLD_MULTI_LW_5_LE,
 MIPS_FOLD_MULTI_LW_2_BE, MIPS_FOLD_MULTI_LW_3_BE,
 MIPS_FOLD_MULTI_LW_4_BE, MIPS_FOLD_MULTI_LW_5_BE,
 MIPS_FOLD_MEMSET_ADDIU_BNE_SW,
 MIPS_FOLD_NETBSD_R3K_PICACHE_DO_INV,
 MIPS_FOLD_LINUX_PMAX_IDLE,
 MIPS_FOLD_NETBSD_PMAX_IDLE,
 MIPS_FOLD_STRLEN_LB_ADDIU_BNE_NOP,
 MIPS_FOLD_BNE_SAMEPAGE_NOP,
 MIPS_FOLD_BEQ_SAMEPAGE_NOP,
 MIPS_FOLD_XOR_ANDI_SLL,
 MIPS_FOLD_ANDI_SLL,
 MIPS_FOLD_LUI_ORI,
 MIPS_FOLD_MULTI_ADDU_3,
 MIPS_FOLD_ADDIU_BNE_SAMEPAGE_ADDIU,
 MIPS_FOLD_LUI_ADDIU,
 MIPS_FOLD_B_SAMEPAGE_ADDIU,
 MIPS_FOLD_BEQ_SAMEPAGE_ADDIU,
 MIPS_FOLD_BNE_SAMEPAGE_ADDIU,
 MIPS_FOLD_JR_RA_ADDIU,
 MIPS_FOLD_B_SAMEPAGE_DADDIU,
 MIPS_N_FOLDS
};
enum mips_combine_site {
 MIPS_CSITE_SW, MIPS_CSITE_LW,
 MIPS_CSITE_R3K_CACHE_INV,
 MIPS_CSITE_NOP, MIPS_CSITE_SLL,
 MIPS_CSITE_ORI, MIPS_CSITE_ADDU,
 MIPS_CSITE_ADDIU, MIPS_CSITE_B_DADDIU,
 MIPS_N_COMBINE_SITES
};
struct mips_cpu {
 struct mips_cpu_type_def cpu_type;
 uint64_t gpr[32];
 uint64_t scratch;
 uint64_t hi;
 uint64_t lo;
 struct mips_coproc *coproc[4];
 uint64_t cop0_config_select1;
 int last_written_tlb_index;
 int compare_register_set;
 int compare_interrupts_pending;
 int32_t count_register_read_count;
 struct interrupt irq_compare;
 struct timer *timer;
 int rmw;
 uint64_t rmw_len;
 uint64_t rmw_addr;
 uint64_t gpr_quadhi[32];
 uint64_t hi1;
 uint64_t lo1;
 uint32_t r5900_sa;
 int cache_picache;
 int cache_pdcache;
 int cache_secondary;
 int cache_picache_linesize;
 int cache_pdcache_linesize;
 int cache_secondary_linesize;
 unsigned char *cache[2];
 void *cache_tags[2];
 uint64_t cache_last_paddr[2];
 int cache_size[2];
 int cache_linesize[2];
 int cache_mask[2];
 struct mips_tc_physpage *cur_physpage; struct mips_instr_call *cur_ic_page; struct mips_instr_call *next_ic; struct mips_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct mips_instr_call *, int low_addr);
 struct mips_vpg_tlb_entry vph_tlb_entry[192];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct mips_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
 struct mips_l3_64_table *l3_64_dummy; struct mips_l3_64_table *next_free_l3; struct mips_l2_64_table *l2_64_dummy; struct mips_l2_64_table *next_free_l2; struct mips_l2_64_table *l1_64[1 << 17];
 uint64_t fold_arm[MIPS_N_COMBINE_SITES];
 uint64_t fold_install[MIPS_N_FOLDS];
 uint64_t fold_fire[MIPS_N_FOLDS];
 uint64_t idle_entered[2];
};
void mips_cpu_interrupt_assert(struct interrupt *interrupt);
void mips_cpu_interrupt_deassert(struct interrupt *interrupt);
int mips_cpu_instruction_has_delayslot(struct cpu *cpu, unsigned char *ib);
void mips_cpu_tlbdump(struct cpu* cpu, int rawflag);
void mips_cpu_register_match(struct machine *m, char *name,
 int writeflag, uint64_t *valuep, int *match_register);
void mips_cpu_register_dump(struct cpu *cpu, int gprs, int coprocs);
int mips_cpu_disassemble_instr(struct cpu *cpu, unsigned char *instr,
        int running, uint64_t addr);
void mips_cpu_exception(struct cpu *cpu, int exccode, int tlb, uint64_t vaddr,
                                    int coproc_nr, uint64_t vaddr_vpn2,
        int vaddr_asid, int x_64);
int mips_cpu_run(struct emul *emul, struct machine *machine);
void mips_cpu_dumpinfo(struct cpu *cpu, _Bool verbose);
void mips_cpu_list_available_types(void);
void mips_cpu_family_init(struct cpu_family *);
struct mips_coproc *mips_coproc_new(struct cpu *cpu, int coproc_nr);
void mips_coproc_tlb_set_entry(struct cpu *cpu, int entrynr, int size,
        uint64_t vaddr, uint64_t paddr0, uint64_t paddr1,
        int valid0, int valid1, int dirty0, int dirty1, int global, int asid,
        int cachealgo0, int cachealgo1);
void coproc_register_read(struct cpu *cpu,
        struct mips_coproc *cp, int reg_nr, uint64_t *ptr, int select);
void coproc_register_write(struct cpu *cpu,
        struct mips_coproc *cp, int reg_nr, uint64_t *ptr, int flag64,
 int select);
void coproc_tlbpr(struct cpu *cpu, int readflag);
void coproc_tlbwri(struct cpu *cpu, int randomflag);
void coproc_rfe(struct cpu *cpu);
void coproc_eret(struct cpu *cpu);
void coproc_function(struct cpu *cpu, struct mips_coproc *cp, int cpnr,
        uint32_t function, int unassemble_only, int running);
int memory_cache_R3000(struct cpu *cpu, int cache, uint64_t paddr,
 int writeflag, size_t len, unsigned char *data);
int mips_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
int translate_v2p_mmu3k(struct cpu *cpu, uint64_t vaddr,
        uint64_t *return_addr, int flags);
int translate_v2p_mmu8k(struct cpu *cpu, uint64_t vaddr,
        uint64_t *return_addr, int flags);
int translate_v2p_mmu10k(struct cpu *cpu, uint64_t vaddr,
        uint64_t *return_addr, int flags);
int translate_v2p_mmu4100(struct cpu *cpu, uint64_t vaddr,
        uint64_t *return_addr, int flags);
int translate_v2p_generic(struct cpu *cpu, uint64_t vaddr,
        uint64_t *return_addr, int flags);
void mips_unaligned_loadstore(struct cpu *cpu, struct mips_instr_call *ic,
 int is_left, int wlen, int store);
int mips_run_instr(struct cpu *cpu);
void mips_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void mips_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void mips_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
int mips32_run_instr(struct cpu *cpu);
void mips32_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void mips32_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void mips32_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
struct cpu_family;
struct ppc_cpu_type_def {
 const char *name;
 int pvr;
 int bits;
 int flags;
 int icache_shift;
 int ilinesize;
 int iway;
 int dcache_shift;
 int dlinesize;
 int dway;
 int l2cache_shift;
 int l2linesize;
 int l2way;
 int altivec;
};
struct ppc_instr_call { void (*f)(struct cpu *, struct ppc_instr_call *); uintptr_t arg[3]; }; struct ppc_tc_physpage { struct ppc_instr_call ics[(1 << 10)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint64_t physaddr; }; struct ppc_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint64_t vaddr_page; uint64_t paddr_page; unsigned char *host_page; };
struct ppc_l3_64_table { unsigned char *host_load[1 << 18]; unsigned char *host_store[1 << 18]; uint64_t phys_addr[1 << 18]; uint8_t vaddr_to_tlbindex[1 << 18]; struct ppc_tc_physpage *phys_page[1 << 18]; struct ppc_l3_64_table *next; int refcount; }; struct ppc_l2_64_table { struct ppc_l3_64_table *l3[1 << 17]; struct ppc_l2_64_table *next; int refcount; };
struct ppc_cpu {
 struct ppc_cpu_type_def cpu_type;
 uint64_t of_emul_addr;
 int mode;
 int bits;
 int irq_asserted;
 int dec_intr_pending;
 uint64_t zero;
 uint32_t cr;
 uint32_t fpscr;
 uint64_t gpr[32];
 uint64_t fpr[32];
 uint64_t vr_hi[32];
 uint64_t vr_lo[32];
 uint64_t msr;
 uint64_t tgpr[4];
 uint32_t sr[16];
 uint64_t spr[1024];
 uint64_t ll_addr;
 int ll_bit;
 struct ppc_tc_physpage *cur_physpage; struct ppc_instr_call *cur_ic_page; struct ppc_instr_call *next_ic; struct ppc_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct ppc_instr_call *, int low_addr);
 struct ppc_vpg_tlb_entry vph_tlb_entry[128];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct ppc_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
 struct ppc_l3_64_table *l3_64_dummy; struct ppc_l3_64_table *next_free_l3; struct ppc_l2_64_table *l2_64_dummy; struct ppc_l2_64_table *next_free_l2; struct ppc_l2_64_table *l1_64[1 << 17];
};
int ppc_run_instr(struct cpu *cpu);
int ppc32_run_instr(struct cpu *cpu);
void ppc_exception(struct cpu *cpu, int exception_nr);
void ppc_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void ppc32_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void ppc_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void ppc32_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void ppc_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void ppc32_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void ppc_init_64bit_dummy_tables(struct cpu *cpu);
int ppc_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void ppc_cpu_family_init(struct cpu_family *);
int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu_family;
struct riscv_instr_call { void (*f)(struct cpu *, struct riscv_instr_call *); uintptr_t arg[3]; }; struct riscv_tc_physpage { struct riscv_instr_call ics[(1 << 11)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint64_t physaddr; }; struct riscv_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint64_t vaddr_page; uint64_t paddr_page; unsigned char *host_page; };
struct riscv_l3_64_table { unsigned char *host_load[1 << 18]; unsigned char *host_store[1 << 18]; uint64_t phys_addr[1 << 18]; uint8_t vaddr_to_tlbindex[1 << 18]; struct riscv_tc_physpage *phys_page[1 << 18]; struct riscv_l3_64_table *next; int refcount; }; struct riscv_l2_64_table { struct riscv_l3_64_table *l3[1 << 17]; struct riscv_l2_64_table *next; int refcount; };
struct riscv_cpu {
 uint64_t extensions;
 uint64_t x[32];
 uint64_t zero_scratch;
 int irq_asserted;
 struct riscv_tc_physpage *cur_physpage; struct riscv_instr_call *cur_ic_page; struct riscv_instr_call *next_ic; struct riscv_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct riscv_instr_call *, int low_addr);
 struct riscv_vpg_tlb_entry vph_tlb_entry[192];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct riscv_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
 struct riscv_l3_64_table *l3_64_dummy; struct riscv_l3_64_table *next_free_l3; struct riscv_l2_64_table *l2_64_dummy; struct riscv_l2_64_table *next_free_l2; struct riscv_l2_64_table *l1_64[1 << 17];
};
void riscv_cpu_family_init(struct cpu_family *);
void riscv_exception(struct cpu *cpu, int vector, int is_trap);
int riscv_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
int riscv_run_instr(struct cpu *cpu);
void riscv_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void riscv_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void riscv_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
int riscv32_run_instr(struct cpu *cpu);
void riscv32_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void riscv32_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void riscv32_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
int riscv_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
int riscv32_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu_family;
struct sh_cpu_type_def {
 const char *name;
 int bits;
 int arch;
 uint32_t pvr;
 uint32_t prr;
};
struct sh_instr_call { void (*f)(struct cpu *, struct sh_instr_call *); uintptr_t arg[2]; }; struct sh_tc_physpage { struct sh_instr_call ics[(1 << 11)+2]; uint32_t next_ofs; uint32_t translations_bitmap; uint32_t translation_ranges_ofs; uint32_t physaddr; }; struct sh_vpg_tlb_entry { uint8_t valid; uint8_t writeflag; uint32_t vaddr_page; uint32_t paddr_page; unsigned char *host_page; };
struct sh_cpu {
 struct sh_cpu_type_def cpu_type;
 uint32_t r[16];
 uint32_t r_bank[8];
 uint32_t fr[16];
 uint32_t xf[16];
 uint32_t mach;
 uint32_t macl;
 uint32_t pr;
 uint32_t fpscr;
 uint32_t fpul;
 uint32_t sr;
 uint32_t ssr;
 uint32_t spc;
 uint32_t gbr;
 uint32_t vbr;
 uint32_t sgr;
 uint32_t dbr;
 uint32_t ccr;
 uint32_t qacr0;
 uint32_t qacr1;
 uint32_t pteh;
 uint32_t ptel;
 uint32_t ptea;
 uint32_t ttb;
 uint32_t tea;
 uint32_t mmucr;
 uint32_t itlb_hi[4];
 uint32_t itlb_lo[4];
 uint32_t utlb_hi[64];
 uint32_t utlb_lo[64];
 uint32_t tra;
 uint32_t expevt;
 uint32_t intevt;
 uint16_t intc_ipra;
 uint16_t intc_iprb;
 uint16_t intc_iprc;
 uint16_t intc_iprd;
 uint32_t intc_intpri00;
 uint32_t intc_intpri04;
 uint32_t intc_intpri08;
 uint32_t intc_intpri0c;
 uint32_t intc_intreq00;
 uint32_t intc_intreq04;
 uint32_t intc_intmsk00;
 uint32_t intc_intmsk04;
 uint8_t int_prio_and_pending[0x1000 / 0x20];
 int16_t int_to_assert;
 unsigned int int_level;
 int pclock;
 uint32_t dmac_sar[8];
 uint32_t dmac_dar[8];
 uint32_t dmac_tcr[8];
 uint32_t dmac_chcr[8];
 uint32_t dmaor;
 struct pci_data *pcic_pcibus;
 struct sh_tc_physpage *cur_physpage; struct sh_instr_call *cur_ic_page; struct sh_instr_call *next_ic; struct sh_tc_physpage *physpage_template; void (*combination_check)(struct cpu *, struct sh_instr_call *, int low_addr);
 struct sh_vpg_tlb_entry vph_tlb_entry[128];
 unsigned char *host_load[1048576]; unsigned char *host_store[1048576]; uint32_t phys_addr[1048576]; struct sh_tc_physpage *phys_page[1048576]; uint8_t vaddr_to_tlbindex[1048576];
};
void sh_cpu_interrupt_assert(struct interrupt *interrupt);
void sh_cpu_interrupt_deassert(struct interrupt *interrupt);
int sh_cpu_instruction_has_delayslot(struct cpu *cpu, unsigned char *ib);
int sh_run_instr(struct cpu *cpu);
void sh_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
 unsigned char *host_page, int writeflag, uint64_t paddr_page);
void sh_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void sh_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void sh_init_64bit_dummy_tables(struct cpu *cpu);
int sh_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
 unsigned char *data, size_t len, int writeflag, int cache_flags);
void sh_cpu_family_init(struct cpu_family *);
void sh_update_interrupt_priorities(struct cpu *cpu);
void sh_update_sr(struct cpu *cpu, uint32_t new_sr);
void sh_exception(struct cpu *cpu, int expevt, int intevt, uint32_t vaddr);
int sh_translate_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
int sh_translate_sq_v2p(struct cpu *cpu, uint64_t vaddr,
 uint64_t *return_addr, int flags);
struct cpu;
struct emul;
struct machine;
struct memory;
struct settings;
struct cpu_family {
 struct cpu_family *next;
 int arch;
 char *name;
 int (*cpu_new)(struct cpu *cpu, struct memory *mem,
        struct machine *machine,
        int cpu_id, char *cpu_type_name);
 void (*init_tables)(struct cpu *cpu);
 void (*list_available_types)(void);
 int (*disassemble_instr)(struct cpu *cpu,
        unsigned char *instr, int running,
        uint64_t dumpaddr);
 void (*register_dump)(struct cpu *cpu,
        int gprs, int coprocs);
 void (*dumpinfo)(struct cpu *cpu, _Bool verbose);
 void (*tlbdump)(struct cpu *cpu, int rawflag);
 void (*functioncall_trace)(struct cpu *,
        int n_args);
};
struct cpu {
 struct machine *machine;
 struct settings *settings;
 struct cpu_family* cpu_family;
 char *name;
 char *path;
 int64_t ninstrs;
 int64_t ninstrs_show;
 int64_t ninstrs_flush;
 int64_t ninstrs_since_gettimeofday;
 struct timeval starttime;
 uint8_t byte_order;
 uint8_t is_32bit;
 uint8_t delay_slot;
 _Bool running;
 int cpu_id;
 struct memory *mem;
 uint64_t vaddr_mask;
 int (*run_instr)(struct cpu *cpu);
 int (*memory_rw)(struct cpu *cpu,
       struct memory *mem, uint64_t vaddr,
       unsigned char *data, size_t len,
       int writeflag, int cache_flags);
 int (*translate_v2p)(struct cpu *, uint64_t vaddr,
       uint64_t *return_paddr, int flags);
 void (*update_translation_table)(struct cpu *,
       uint64_t vaddr_page, unsigned char *host_page,
       int writeflag, uint64_t paddr_page);
 void (*invalidate_translation_caches)(struct cpu *,
       uint64_t paddr, int flags);
 void (*invalidate_code_translation)(struct cpu *,
       uint64_t paddr, int flags);
 void (*useremul_syscall)(struct cpu *cpu, uint32_t code);
 int (*instruction_has_delayslot)(struct cpu *cpu,
       unsigned char *ib);
 uint64_t pc;
 int trace_tree_depth;
 int last_was_function_transition;
 _Bool wants_to_idle;
 _Bool is_halted;
 _Bool has_been_idling;
 int translation_readahead;
 int n_translated_instrs;
 unsigned char *translation_cache;
 size_t translation_cache_cur_ofs;
 union {
  struct alpha_cpu alpha;
  struct arm_cpu arm;
  struct i960_cpu i960;
  struct m88k_cpu m88k;
  struct mips_cpu mips;
  struct ppc_cpu ppc;
  struct riscv_cpu riscv;
  struct sh_cpu sh;
 } cd;
};
struct cpu *cpu_new(struct memory *mem, struct machine *machine,
        int cpu_id, char *cpu_type_name);
void cpu_destroy(struct cpu *cpu);
void cpu_tlbdump(struct cpu *cpu, int rawflag);
void cpu_register_dump(struct machine *m, struct cpu *cpu,
 int gprs, int coprocs);
int cpu_disassemble_instr(struct machine *m, struct cpu *cpu,
 unsigned char *instr, int running, uint64_t addr);
void cpu_functioncall_trace(struct cpu *cpu, uint64_t f);
void cpu_functioncall_trace_return(struct cpu *cpu);
void cpu_create_or_reset_tc(struct cpu *cpu);
void cpu_run_init(struct machine *machine);
void cpu_run_deinit(struct machine *machine);
void cpu_dumpinfo(struct machine *m, struct cpu *cpu, _Bool verbose);
void cpu_list_available_types(void);
void cpu_show_cycles(struct machine *machine, _Bool forced);
void cpu_print_pc_indicator_in_disassembly(struct cpu *cpu, int running, uint64_t dumpaddr);
void cpu_init(void);
struct machine;
struct pci_device;
struct devinit {
 struct machine *machine;
 char *name;
 char *name2;
 uint64_t addr;
 uint64_t addr2;
 uint64_t len;
 char *interrupt_path;
 int in_use;
 int addr_mult;
 int pci_little_endian;
 void *return_ptr;
};
struct device_entry {
 char *name;
 int (*initf)(struct devinit *);
};
struct pci_entry {
 char *name;
 void (*initf)(struct machine *, struct memory *,
       struct pci_device *);
};
void autodev_init(void);
int device_register(const char *name, int (*initf)(struct devinit *));
struct device_entry *device_lookup(char *name);
int device_unregister(char *name);
void *device_add(struct machine *machine, const char *name_and_params);
void device_dumplist(void);
void device_set_exit_on_error(int exit_on_error);
void device_init(void);
int pci_register(const char *name, void (*initf)(struct machine *, struct memory *,
 struct pci_device *));
void (*pci_lookup_initf(const char *name))(struct machine *machine,
 struct memory *mem, struct pci_device *pd);
struct cpu;
struct machine;
struct memory;
struct pci_data;
struct timer;
struct pic8259_data {
 struct interrupt irq;
 int irq_base;
 int current_command;
 int init_state;
 int priority_reg;
 uint8_t irr;
 uint8_t isr;
 uint8_t ier;
};
struct dec_ioasic_data {
 uint32_t scsi_dmaptr;
 uint32_t scsi_nextptr;
 uint32_t lance_dmaptr;
 uint32_t floppy_dmaptr;
 uint32_t isdn_x_dmaptr;
 uint32_t isdn_x_nextptr;
 uint32_t isdn_r_dmaptr;
 uint32_t isdn_r_nextptr;
 uint32_t csr;
 uint32_t intr;
 uint32_t imsk;
 uint32_t isdn_x_data;
 uint32_t isdn_r_data;
 uint32_t lance_decode;
 uint32_t scsi_decode;
 uint32_t scc0_decode;
 uint32_t scc1_decode;
 uint32_t floppy_decode;
 uint32_t scsi_scr;
 uint32_t scsi_sdr0;
 uint32_t scsi_sdr1;
 int (*dma_func[8])(struct cpu *, void *, uint64_t addr, size_t dma_len, int tx);
 void *dma_func_extra[8];
 int rackmount_flag;
 struct interrupt *irq;
 int int_asserted;
};
void dec_ioasic_reassert(struct dec_ioasic_data*);
int dev_dec_ioasic_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
struct dec_ioasic_data *dev_dec_ioasic_init(struct cpu *cpu, struct memory *mem, uint64_t baseaddr, int rackmount_flag, struct interrupt* irq);
int dev_asc_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
void dev_asc_init(struct machine *machine, struct memory *mem, uint64_t baseaddr,
 const char *irq_path, void *turbochannel, int mode,
 size_t (*dma_controller)(void *dma_controller_data,
  unsigned char *data, size_t len, int writeflag),
 void *dma_controller_data);
int dev_bt431_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
struct vfb_data;
void dev_bt431_init(struct memory *mem, uint64_t baseaddr,
 struct vfb_data *vfb_data, int color_fb_flag);
int dev_bt455_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
struct vfb_data;
void dev_bt455_init(struct memory *mem, uint64_t baseaddr,
 struct vfb_data *vfb_data);
int dev_bt459_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
struct vfb_data;
void dev_bt459_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, uint64_t baseaddr_irq, struct vfb_data *vfb_data,
 int color_fb_flag, const char *irq_path, int type);
int dev_colorplanemask_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_colorplanemask_init(struct memory *mem, uint64_t baseaddr,
 unsigned char *color_plane_mask);
void dev_dc7085_tick(struct cpu *cpu, void *);
int dev_dc7085_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
int dev_dc7085_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char *irq_path, int use_fb);
int dev_deccca_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
void dev_deccca_init(struct memory *mem, uint64_t baseaddr);
int dev_decxmi_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
void dev_decxmi_init(struct memory *mem, uint64_t baseaddr);
struct vfb_data {
 struct memory *memory;
 struct machine *machine;
 int vfb_type;
 int vfb_scaledown;
 int xsize;
 int ysize;
 int bit_depth;
 int color32k;
 int psp_15bit;
 unsigned char color_plane_mask;
 int bytes_per_line;
 int visible_xsize;
 int visible_ysize;
 size_t framebuffer_size;
 int x11_xsize, x11_ysize;
 int update_x1, update_y1, update_x2, update_y2;
 unsigned char rgb_palette[256 * 3];
 char *name;
 char title[100];
 void (*redraw_func)(struct vfb_data *, int, int);
 unsigned char *framebuffer;
 struct fb_window *fb_window;
};
void set_grayscale_palette(struct vfb_data *d, int ncolors);
void dev_fb_resize(struct vfb_data *d, int new_xsize, int new_ysize);
void dev_fb_setcursor(struct vfb_data *d, int cursor_x, int cursor_y, int on,
        int cursor_xsize, int cursor_ysize);
void framebuffer_blockcopyfill(struct vfb_data *d, int fillflag, int fill_r,
 int fill_g, int fill_b, int x1, int y1, int x2, int y2,
 int from_x, int from_y);
void dev_fb_tick(struct cpu *, void *);
int dev_fb_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
struct vfb_data *dev_fb_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, int vfb_type, int visible_xsize, int visible_ysize,
 int xsize, int ysize, int bit_depth, const char *name);
int dev_gt_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
struct pci_data *dev_gt_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, const char *timer_irq_path, const char *isa_irq_path, int type);
size_t dev_jazz_dma_controller(void *dma_controller_data,
 unsigned char *data, size_t len, int writeflag);
int dev_kn01_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_kn01_init(struct memory *mem, uint64_t baseaddr, int color_fb);
int dev_vdac_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_vdac_init(struct memory *mem, uint64_t baseaddr,
 unsigned char *rgb_palette, int color_fb_flag);
int dev_dec5500_ioboard_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
struct dec5500_ioboard_data *dev_dec5500_ioboard_init(struct cpu *cpu, struct memory *mem, uint64_t baseaddr);
int dev_sgec_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
void dev_sgec_init(struct memory *mem, uint64_t baseaddr, int irq_nr);
int dev_le_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_le_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, uint64_t buf_start, uint64_t buf_end,
 const char *irq_path, int len);
void dev_mc146818_tick(struct cpu *cpu, void *);
int dev_mc146818_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_mc146818_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char *irq_path, int access_style, int addrdiv);
int dev_pckbc_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
int dev_pckbc_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, int type, char *keyboard_irqpath,
 char *mouse_irqpath, int in_use, int pc_style_flag);
int dev_pmagja_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_pmagja_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, const char *irq_path);
struct px_data {
 struct memory *fb_mem;
 struct vfb_data *vfb_data;
 int type;
 const char *px_name;
 struct interrupt irq;
 int bitdepth;
 int xconfig;
 int yconfig;
 uint32_t intr;
 unsigned char sram[128 * 1024];
};
int dev_px_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_px_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, int px_type, const char *irq_path);
int dev_ram_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_ram_init(struct machine *machine, uint64_t baseaddr, uint64_t length,
 int mode, uint64_t otheraddr, const char* name);
int dev_scc_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
int dev_scc_dma_func(struct cpu *cpu, void *extra, uint64_t addr,
 size_t dma_len, int tx);
void *dev_scc_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char* irq_path, int use_fb, int scc_nr, int addrmul);
int dev_sfb_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_sfb_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, struct vfb_data *vfb_data);
int dev_sgi_gbe_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len, int writeflag,
 void *);
void dev_sgi_gbe_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr);
int dev_sgi_re_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_sgi_re_init(struct machine *machine, struct memory *mem, uint64_t baseaddr);
int dev_sgi_de_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
struct sgi_re_data;
void dev_sgi_de_init(struct memory *mem, uint64_t baseaddr, struct sgi_re_data *);
int dev_sgi_re_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_sgi_mte_init(struct memory *mem, uint64_t baseaddr, struct sgi_re_data *);
int dev_sgi_de_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_sgi_de_status_init(struct memory *mem, uint64_t baseaddr, struct sgi_re_data *);
struct sgi_ip20_data {
 int dummy;
};
int dev_sgi_ip20_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
struct sgi_ip20_data *dev_sgi_ip20_init(struct cpu *cpu, struct memory *mem, uint64_t baseaddr);
struct sgi_ip22_data {
 int guiness_flag;
 uint32_t reg[0x100 / 4];
 uint32_t imc_reg[0x100 / 4];
 uint32_t unknown2_reg[0x100 / 4];
 uint32_t unknown_timer;
};
int dev_sgi_ip22_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *);
struct sgi_ip22_data *dev_sgi_ip22_init(struct machine *machine, struct memory *mem, uint64_t baseaddr, int guiness_flag);
void dev_crime_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char *irq_path, int use_fb);
int dev_macepci_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
struct pci_data *dev_macepci_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char *irq_path);
int dev_sgi_mec_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_sgi_mec_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, char *irq_path, unsigned char *macaddr);
int dev_sgi_ust_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_sgi_ust_init(struct memory *mem, uint64_t baseaddr);
void dev_sii_tick(struct cpu *cpu, void *);
int dev_sii_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_sii_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, uint64_t buf_start, uint64_t buf_end,
 char *irq_path);
int dev_ssc_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_ssc_init(struct machine *machine, struct memory *mem,
 uint64_t baseaddr, const char *irq_path, int use_fb);
int dev_turbochannel_access(struct cpu *cpu, struct memory *mem,
 uint64_t relative_addr, unsigned char *data, size_t len,
 int writeflag, void *);
void dev_turbochannel_init(struct machine *machine, struct memory *mem,
 int slot_nr, uint64_t baseaddr, uint64_t endaddr, const char *device_name,
 const char *irq_path);
struct pci_data *dev_uninorth_init(struct machine *machine, struct memory *mem,
 uint64_t addr, int irqbase, int pciirq);
int dev_vga_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr,
 unsigned char *data, size_t len, int writeflag, void *);
void dev_vga_init(struct machine *machine, struct memory *mem,
 uint64_t videomem_base, uint64_t control_base, const char *name);
struct vr41xx_data *dev_vr41xx_init(struct machine *machine,
 struct memory *mem, int cpumodel);
struct lk201_data {
        int use_fb;
 int console_handle;
        int (*space_available_in_queue)(void *,int);
        void (*add_to_rx_queue)(void *,int,int);
 void *add_data;
        unsigned char keyb_buf[8];
        int keyb_buf_pos;
        int mouse_mode;
        int mouse_revision;
        int mouse_buttons;
};
void lk201_tick(struct machine *, struct lk201_data *);
void lk201_tx_data(struct lk201_data *, int port, int idata);
void lk201_init(struct lk201_data *d, int use_fb,
 int (*space_available_in_queue)(void *,int),
 void (*add_to_rx_queue)(void *,int,int),
 int console_handle, void *);
struct symbol {
 struct symbol *next;
 uint64_t addr;
 uint64_t len;
 char *name;
 int type;
 int n_args;
};
struct symbol_context {
 struct symbol *first_symbol;
 int sorted_array;
 int n_symbols;
};
int symbol_nsymbols(struct symbol_context *);
int get_symbol_addr(struct symbol_context *, const char *symbol, uint64_t *addr);
char *get_symbol_name_and_n_args(struct symbol_context *, uint64_t addr,
 uint64_t *offset, int *n_argsp);
char *get_symbol_name(struct symbol_context *, uint64_t addr, uint64_t *offset);
void add_symbol_name(struct symbol_context *, uint64_t addr,
 uint64_t len, const char *name, int type, int n_args);
void symbol_readfile(struct symbol_context *, char *fname);
void symbol_recalc_sizes(struct symbol_context *);
void symbol_init(struct symbol_context *);
char *symbol_demangle_cplusplus(const char *name);
struct cpu_family;
struct diskimage;
struct emul;
struct fb_window;
struct machine_arcbios;
struct machine_pmax;
struct memory;
struct of_data;
struct settings;
struct isa_pic_data {
 struct pic8259_data *pic1;
 struct pic8259_data *pic2;
 int *pending_timer_interrupts;
 int last_int;
};
struct breakpoints {
 int n;
 char **string;
 uint64_t *addr;
 uint64_t *hitcount;
 int64_t *ignore_left;
};
struct watchpoints {
 int n;
 char **string;
 uint64_t *addr;
 uint64_t *len;
};
struct statistics {
 char *filename;
 FILE *file;
 int enabled;
 char *fields;
};
struct tick_functions {
 int n_entries;
 int *ticks_till_next;
 int *ticks_reset_value;
 void (**f)(struct cpu *, void *);
 void **extra;
};
struct x11_md {
 int in_use;
 int scaledown;
 int scaleup;
 int n_display_names;
 char **display_names;
 int current_display_name_nr;
 int n_fb_windows;
 struct fb_window **fb_windows;
};
struct machine {
 struct emul *emul;
 struct settings *settings;
 char *name;
 char *path;
 int machine_type;
 int machine_subtype;
 const char *machine_name;
 int serial_nr;
 int nr_of_nics;
 struct memory *memory;
 int main_console_handle;
 struct tick_functions tick_functions;
 char *cpu_name;
 int byte_order_override;
 int bootstrap_cpu;
 int use_random_bootstrap_cpu;
 _Bool start_paused;
 int ncpus;
 struct cpu **cpus;
 struct diskimage *first_diskimage;
 struct symbol_context symbol_context;
 int random_mem_contents;
 uint32_t physical_ram_in_mb;
 int memory_offset_in_mb;
 int prom_emulation;
 int register_dump;
 int arch_pagesize;
 int bootdev_type;
 int bootdev_id;
 char *bootstr;
 char *bootarg;
 struct breakpoints breakpoints;
 struct watchpoints watchpoints;
 int halt_on_nonexistant_memaccess;
 int instruction_trace;
 int show_nr_of_instructions;
 int show_trace_tree;
 int emulated_hz;
 int allow_instruction_combinations;
 int force_netboot;
 uint64_t file_loaded_end_addr;
 char *boot_kernel_filename;
 char *boot_string_argument;
 int n_gfx_cards;
 struct statistics statistics;
 struct x11_md x11_md;
 union {
  struct machine_arcbios *arc;
  struct machine_pmax *pmax;
  struct of_data *of_data;
 } md;
 struct isa_pic_data isa_pic_data;
};
struct machine_entry_subtype {
 int machine_subtype;
 const char *name;
 int n_aliases;
 char **aliases;
};
struct machine_entry {
 struct machine_entry *next;
 int machine_type;
 const char *name;
 int n_aliases;
 char **aliases;
 void (*setup)(struct machine *, struct cpu *);
 void (*set_default_cpu)(struct machine *);
 void (*set_default_ram)(struct machine *);
 int n_subtypes;
 struct machine_entry_subtype **subtype;
};
void automachine_init(void);
struct machine *machine_new(char *name, struct emul *emul, int id);
void machine_destroy(struct machine *machine);
int machine_name_to_type(char *stype, char *ssubtype, int *type, int *subtype);
void machine_add_breakpoint_string(struct machine *machine, char *str);
int machine_watchpoint_match(struct machine *machine, uint64_t addr,
 uint64_t len);
void machine_add_tickfunction(struct machine *machine,
 void (*func)(struct cpu *, void *), void *extra, int clockshift);
void machine_statistics_init(struct machine *, char *fname);
void machine_register(char *name, void (*setup)(struct machine *, struct cpu *));
void machine_setup(struct machine *);
void machine_add_devices_as_symbols(struct machine *machine, uint64_t offset);
void machine_memsize_fix(struct machine *);
void machine_default_cputype(struct machine *);
void machine_dumpinfo(struct machine *);
_Bool machine_run(struct machine *machine);
void machine_list_available_types_and_cpus(void);
struct machine_entry *machine_entry_new(const char *name, int oldstyle_type);
void machine_entry_add_alias(struct machine_entry *me, const char *name);
void machine_entry_add_subtype(struct machine_entry *me, const char *name,
 int oldstyle_subtype, ...);
void machine_entry_register(struct machine_entry *me);
void machine_init(void);
struct cpu;
struct memory_device {
 uint64_t baseaddr;
 uint64_t endaddr;
 uint64_t length;
 int flags;
 const char *name;
 int (*f)(struct cpu *,struct memory *,
       uint64_t,unsigned char *,size_t,int,void *);
 void *extra;
 unsigned char *dyntrans_data;
 uint64_t dyntrans_write_low;
 uint64_t dyntrans_write_high;
};
struct memory {
 uint64_t physical_max;
 void *pagetable;
 int dev_dyntrans_alignment;
 int n_mmapped_devices;
 int last_accessed_device;
 uint64_t mmap_dev_minaddr;
 uint64_t mmap_dev_maxaddr;
 struct memory_device *devices;
};
uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len);
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len,
 uint64_t data);
void *zeroed_alloc(size_t s);
struct memory *memory_new(uint64_t physical_max);
int memory_points_to_string(struct cpu *cpu, struct memory *mem,
 uint64_t addr, int min_string_length);
char *memory_conv_to_string(struct cpu *cpu, struct memory *mem,
 uint64_t addr, char *buf, int bufsize);
unsigned char *memory_paddr_to_hostaddr(struct memory *mem,
 uint64_t paddr, int writeflag);
void memory_device_dyntrans_access(struct cpu *, struct memory *mem,
 void *extra, uint64_t *low, uint64_t *high);
void memory_device_update_data(struct memory *mem, void *extra,
 unsigned char *data);
void memory_device_update_length(struct memory *mem, void *extra,
 uint64_t newlength);
void memory_device_register(struct memory *mem, const char *,
 uint64_t baseaddr, uint64_t len, int (*f)(struct cpu *,
     struct memory *,uint64_t,unsigned char *,size_t,int,void *),
 void *extra, int flags, unsigned char *dyntrans_data);
void memory_device_remove(struct memory *mem, int i);
void dump_mem_string(struct cpu *cpu, uint64_t addr);
void store_string(struct cpu *cpu, uint64_t addr, const char *s);
int store_64bit_word(struct cpu *cpu, uint64_t addr, uint64_t data64);
int store_32bit_word(struct cpu *cpu, uint64_t addr, uint64_t data32);
int store_16bit_word(struct cpu *cpu, uint64_t addr, uint64_t data16);
void store_byte(struct cpu *cpu, uint64_t addr, uint8_t data);
void store_64bit_word_in_host(struct cpu *cpu, unsigned char *data,
        uint64_t data32);
void store_32bit_word_in_host(struct cpu *cpu, unsigned char *data,
        uint64_t data32);
void store_16bit_word_in_host(struct cpu *cpu, unsigned char *data,
        uint16_t data16);
uint64_t load_64bit_word(struct cpu *cpu, uint64_t addr);
uint32_t load_32bit_word(struct cpu *cpu, uint64_t addr);
uint16_t load_16bit_word(struct cpu *cpu, uint64_t addr);
void store_buf(struct cpu *cpu, uint64_t addr, const char *s, size_t len);
void add_environment_string(struct cpu *cpu, const char *s, uint64_t *addr);
void add_environment_string_dual(struct cpu *cpu,
        uint64_t *ptrp, uint64_t *addrp, const char *s1, const char *s2);
void store_pointer_and_advance(struct cpu *cpu, uint64_t *addrp,
        uint64_t data, int flag64);
_Bool memory_warn_about_unimplemented_addr(struct cpu *cpu, struct memory *mem,
 int writeflag, uint64_t paddr, size_t len);
struct footbridge_data {
 struct interrupt irq;
 struct pci_data *pcibus;
 int console_handle;
 uint32_t timer_load[4];
 uint32_t timer_value[4];
 uint32_t timer_control[4];
 struct interrupt timer_irq[4];
 struct timer *timer[4];
 int pending_timer_interrupts[4];
 int pending_bound[4];
 int irq_asserted;
 uint32_t irq_status;
 uint32_t irq_enable;
 uint32_t fiq_status;
 uint32_t fiq_enable;
};
static void footbridge_pending(struct footbridge_data *d, int nr)
{
 if (d->pending_timer_interrupts[nr] >= d->pending_bound[nr])
  d->pending_timer_interrupts[nr] = 1;
 else
  d->pending_timer_interrupts[nr] ++;
}
static void timer_tick0(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 0); }
static void timer_tick1(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 1); }
static void timer_tick2(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 2); }
static void timer_tick3(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 3); }
static uint64_t footbridge_effective_cycles(uint32_t load, uint32_t control,
 int with_prescaler)
{
 uint64_t cycles = load;
 if (cycles == 0)
  cycles = (uint64_t)0x00FFFFFF + 1;
 if (!with_prescaler)
  return cycles;
 if ((control & (0x04 | 0x08))
     == (0x04 | 0x08)) {
  ;
 } else if (control & 0x04)
  cycles *= 16;
 else if (control & 0x08)
  cycles *= 256;
 return cycles;
}
static void reload_timer_value(struct cpu *cpu, struct footbridge_data *d,
 int timer_nr)
{
 double freq = (double)cpu->machine->emulated_hz;
 freq /= (double) footbridge_effective_cycles(d->timer_load[timer_nr],
     d->timer_control[timer_nr], 1);
 d->timer_value[timer_nr] = d->timer_load[timer_nr];
 {
  double bound = freq;
  if (!(bound <= (double)1048576 * 65.0))
   bound = (double)1048576 * 65.0;
  if (!(bound >= 1.0))
   bound = 1.0;
  d->pending_bound[timer_nr] = (int) bound;
 }
 if (d->timer[timer_nr] == ((void *)0)) {
  switch (timer_nr) {
  case 0: d->timer[0] = timer_add(freq, timer_tick0, d); break;
  case 1: d->timer[1] = timer_add(freq, timer_tick1, d); break;
  case 2: d->timer[2] = timer_add(freq, timer_tick2, d); break;
  case 3: d->timer[3] = timer_add(freq, timer_tick3, d); break;
  }
 } else {
  timer_update_frequency(d->timer[timer_nr], freq);
 }
}
void dev_footbridge_tick(struct cpu *cpu, void *extra)
{
 struct footbridge_data *d = (struct footbridge_data *) extra;
 int i;
 for (i=0; i<4; i++) {
  if (d->timer_control[i] & 0x80) {
   if (d->pending_timer_interrupts[i] > 0) {
    d->timer_value[i] = random() %
        footbridge_effective_cycles(d->timer_load[i],
        d->timer_control[i], 0);
    (d->timer_irq[i]).interrupt_assert(&(d->timer_irq[i]));
   }
  }
 }
}
void footbridge_interrupt_assert(struct interrupt *interrupt)
{
 struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
 d->irq_status |= interrupt->line;
 if ((d->irq_status & d->irq_enable) ) {
  d->irq_asserted = 1;
  (d->irq).interrupt_assert(&(d->irq));
 }
}
void footbridge_interrupt_deassert(struct interrupt *interrupt)
{
 struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
 d->irq_status &= ~interrupt->line;
 if (!(d->irq_status & d->irq_enable) && d->irq_asserted) {
  d->irq_asserted = 0;
  (d->irq).interrupt_deassert(&(d->irq));
 }
}
int dev_footbridge_isa_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *extra)
{
 uint64_t idata = 0, odata = 0;
 int x;
 if (writeflag == 1) {
  idata = memory_readmax64(cpu, data, len);
  fatal("[ footbridge_isa: WARNING/TODO: write! idata = 0x%016" "l" "x"" ]\n", idata);
 }
 x = cpu->machine->isa_pic_data.last_int;
 if (x < 8)
  odata = cpu->machine->isa_pic_data.pic1->irq_base + x;
 else
  odata = cpu->machine->isa_pic_data.pic2->irq_base + x - 8;
 if (writeflag == 0)
  memory_writemax64(cpu, data, len, odata);
 return 1;
}
int dev_footbridge_reset_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *extra)
{
 uint64_t idata = 0;
 if (writeflag == 1) {
  idata = memory_readmax64(cpu, data, len);
  if (idata & 0x40) {
   debug("[ footbridge_reset: GP16: Halting. ]\n");
   cpu->running = 0;
  }
 }
 return 1;
}
int dev_footbridge_pci_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *extra)
{
 struct footbridge_data *d = (struct footbridge_data *) extra;
 uint64_t idata = 0, odata = 0;
 int bus, dev, func, reg;
 if (writeflag == 1)
  idata = memory_readmax64(cpu, data, len|128);
 bus_pci_decompose_1(relative_addr, &bus, &dev, &func, &reg);
 bus_pci_setaddr(cpu, d->pcibus, bus, dev, func, reg);
 if (bus == 255) {
  fatal("[ footbridge DEBUG ERROR: bus 255 unlikely,"
      " pc (might not be updated) = 0x%08x ]\n", (int)cpu->pc);
  return 1;
 }
 debug("[ footbridge pci: %s bus %i, device %i, function %i, register "
     "%i ]\n", writeflag == 0? "read from" : "write to", bus,
     dev, func, reg);
 bus_pci_data_access(cpu, d->pcibus, writeflag == 0?
     &odata : &idata, len, writeflag);
 if (writeflag == 0)
  memory_writemax64(cpu, data, len|128, odata);
 return 1;
}
int dev_footbridge_access(struct cpu *cpu, struct memory *mem, uint64_t relative_addr, unsigned char *data, size_t len, int writeflag, void *extra)
{
 struct footbridge_data *d = (struct footbridge_data *) extra;
 uint64_t idata = 0, odata = 0;
 int timer_nr = 0;
 if (writeflag == 1)
  idata = memory_readmax64(cpu, data, len);
 if (relative_addr >= 0x300 && relative_addr <= 0x36C) {
  timer_nr = (relative_addr >> 5) & (4 - 1);
  relative_addr &= ~0x060;
 }
 switch (relative_addr) {
 case 0x00:
  odata = 0x1011;
  break;
 case 0x02:
  odata = 0x1065;
  break;
 case 0x04:
 case 0x0c:
 case 0x10:
 case 0x14:
 case 0x18:
  break;
 case 0x08:
  odata = 3;
  break;
 case 0x140:
  if (writeflag == 1 && idata != 0)
   fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
       "EXTENSION: 0x%llx ]\n", (long long)idata);
  break;
 case 0x13C:
  odata = (1 << 31);
  break;
 case 0x160:
  if (writeflag == 1)
   console_putchar(d->console_handle, idata);
  break;
 case 0x164:
  odata = 0;
  break;
 case 0x178:
  odata = 0x20;
  break;
 case 0x180:
  if (writeflag == 0)
   odata = d->irq_status & d->irq_enable;
  else {
   fatal("[ WARNING: footbridge write to irq status? ]\n");
   exit(1);
  }
  break;
 case 0x184:
  if (writeflag == 0)
   odata = d->irq_status;
  else {
   fatal("[ footbridge write to irq_raw_status ]\n");
   exit(1);
  }
  break;
 case 0x188:
  if (writeflag == 1) {
   d->irq_enable |= idata;
   if (d->irq_status & d->irq_enable)
    (d->irq).interrupt_assert(&(d->irq));
   else
    (d->irq).interrupt_deassert(&(d->irq));
  } else {
   odata = d->irq_enable;
   fatal("[ WARNING: footbridge read from "
       "ENABLE SET? ]\n");
   exit(1);
  }
  break;
 case 0x18c:
  if (writeflag == 1) {
   d->irq_enable &= ~idata;
   if (d->irq_status & d->irq_enable)
    (d->irq).interrupt_assert(&(d->irq));
   else
    (d->irq).interrupt_deassert(&(d->irq));
  } else {
   odata = d->irq_enable;
   fatal("[ WARNING: footbridge read from "
       "ENABLE CLEAR? ]\n");
   exit(1);
  }
  break;
 case 0x280:
  if (writeflag == 0)
   odata = d->fiq_status & d->fiq_enable;
  else {
   fatal("[ WARNING: footbridge write to fiq status? ]\n");
   exit(1);
  }
  break;
 case 0x284:
  if (writeflag == 0)
   odata = d->fiq_status;
  else {
   fatal("[ footbridge write to fiq_raw_status ]\n");
   exit(1);
  }
  break;
 case 0x288:
  if (writeflag == 1)
   d->fiq_enable |= idata;
  break;
 case 0x28c:
  if (writeflag == 1)
   d->fiq_enable &= ~idata;
  break;
 case 0x300:
  if (writeflag == 0)
   odata = d->timer_load[timer_nr];
  else {
   d->timer_load[timer_nr] = idata & 0x00FFFFFF;
   reload_timer_value(cpu, d, timer_nr);
   (d->timer_irq[timer_nr]).interrupt_deassert(&(d->timer_irq[timer_nr]));
  }
  break;
 case 0x304:
  if (writeflag == 0)
   odata = d->timer_value[timer_nr];
  else
   d->timer_value[timer_nr] = idata & 0x00FFFFFF;
  break;
 case 0x308:
  if (writeflag == 0)
   odata = d->timer_control[timer_nr];
  else {
   d->timer_control[timer_nr] = idata;
   if (idata & 0x80) {
    reload_timer_value(cpu, d, timer_nr);
   } else {
    d->pending_timer_interrupts[timer_nr] = 0;
   }
   (d->timer_irq[timer_nr]).interrupt_deassert(&(d->timer_irq[timer_nr]));
  }
  break;
 case 0x30C:
  if (writeflag == 1) {
   if (d->timer_control[timer_nr] & 0x40) {
    reload_timer_value(cpu, d, timer_nr);
   }
   if (d->pending_timer_interrupts[timer_nr] > 0) {
    d->pending_timer_interrupts[timer_nr] --;
   }
   (d->timer_irq[timer_nr]).interrupt_deassert(&(d->timer_irq[timer_nr]));
  }
  break;
 case 0x100:
  if (writeflag == 0) {
   fatal("[ footbridge read from sdram_ba_mask ]\n");
   exit(1);
  } else {
   switch (idata) {
   case 0x00000000:
   case 0x00040000:
   case 0x000C0000:
   case 0x001C0000:
   case 0x003C0000:
   case 0x007C0000:
   case 0x00FC0000:
   case 0x01FC0000:
   case 0x03FC0000:
   case 0x07FC0000:
   case 0x0FFC0000:
    break;
   default:
    fatal("[ footbridge write to sdram_ba_mask "
        "%#llx ]\n", (long long)idata);
    break;
   }
  }
  break;
 case 0x104:
  if (writeflag == 0) {
   fatal("[ footbridge read from sdram_ba_offset ]\n");
   exit(1);
  } else {
   if (idata != 0)
    fatal("[ footbridge write to sdram_ba_offset "
        "%#llx ]\n", (long long)idata);
  }
  break;
 default:if (writeflag == 0) {
   fatal("[ footbridge: read from 0x%x ]\n",
       (int)relative_addr);
  } else {
   fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
       (int)relative_addr, (long long)idata);
  }
 }
 if (writeflag == 0)
  memory_writemax64(cpu, data, len, odata);
 return 1;
}
int devinit_footbridge (struct devinit *devinit)
{
 struct footbridge_data *d;
 char irq_path[300], irq_path_isa[400];
 uint64_t pci_addr = 0x7b000000;
 int i;
 { if ((d = (struct footbridge_data *) malloc(sizeof(struct footbridge_data))) == ((void *)0)) { char where_msg[400]; snprintf(where_msg, sizeof(where_msg), "%s, line %i, function %s().\n", "../src/devices/dev_footbridge.c", 768, __func__); fprintf(stderr, "\n%s, in %s\n", "Out of memory", where_msg); exit(1); }; };
 memset(d, 0, sizeof(struct footbridge_data));
 for (i = 0; i < 4; i++)
  d->pending_bound[i] = 1;
 { interrupt_handler_lookup(devinit->interrupt_path, &(d->irq)); interrupt_connect(&(d->irq), 0); };
 memory_device_register(devinit->machine->memory, devinit->name,
     devinit->addr, 0x400,
     dev_footbridge_access, d, 0, ((void *)0));
 memory_device_register(devinit->machine->memory, "footbridge_isa",
     0x79000000, 8, dev_footbridge_isa_access, d, 0, ((void *)0));
 d->console_handle = console_start_slave(devinit->machine, "fcom", 0);
 snprintf(irq_path, sizeof(irq_path), "%s.footbridge",
     devinit->interrupt_path);
 for (i=0; i<32; i++) {
  struct interrupt interrupt_template;
  char tmpstr[600];
  memset(&interrupt_template, 0, sizeof(interrupt_template));
  interrupt_template.line = (uint32_t)1 << i;
  snprintf(tmpstr, sizeof(tmpstr), "%s.%i", irq_path, i);
  interrupt_template.name = tmpstr;
  interrupt_template.extra = d;
  interrupt_template.interrupt_assert =
      footbridge_interrupt_assert;
  interrupt_template.interrupt_deassert =
      footbridge_interrupt_deassert;
  interrupt_handler_register(&interrupt_template);
  if (i>=0x04 && i<=0x07)
   { interrupt_handler_lookup(tmpstr, &(d->timer_irq[i-0x04])); interrupt_connect(&(d->timer_irq[i-0x04]), 0); };
 }
 switch (devinit->machine->machine_type) {
 case 5002:
  snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.10", irq_path);
  break;
 case 5004:
  snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.11", irq_path);
  break;
 default:fatal("footbridge unimpl machine type\n");
  exit(1);
 }
 d->pcibus = bus_pci_init(
     devinit->machine,
     irq_path,
     0x7c000000,
     0x80000000,
     0x00000000,
     0x00000000,
     irq_path,
     0x7c000000,
     0x80000000,
     irq_path_isa);
 switch (devinit->machine->machine_type) {
 case 5002:
  bus_pci_add(devinit->machine, d->pcibus,
      devinit->machine->memory, 0xc0, 7, 0, "ali_m1543");
  bus_pci_add(devinit->machine, d->pcibus,
      devinit->machine->memory, 0xc0, 10, 0, "dec21143");
  bus_pci_add(devinit->machine, d->pcibus,
      devinit->machine->memory, 0xc0, 16, 0, "ali_m5229");
  break;
 case 5004:
  bus_pci_add(devinit->machine, d->pcibus,
      devinit->machine->memory, 0xc0, 11, 0, "symphony_83c553");
  bus_pci_add(devinit->machine, d->pcibus,
      devinit->machine->memory, 0xc0, 11, 1, "symphony_82c105");
  memory_device_register(devinit->machine->memory,
      "footbridge_reset", 0x7c000338, 1,
      dev_footbridge_reset_access, d, 0, ((void *)0));
  break;
 default:fatal("footbridge: unimplemented machine type.\n");
  exit(1);
 }
 memory_device_register(devinit->machine->memory,
     "footbridge_pci", pci_addr, 0x1000000,
     dev_footbridge_pci_access, d, 0, ((void *)0));
 for (i=0; i<4; i++) {
  d->timer_control[i] = 0x40;
  d->timer_load[i] = 0x00FFFFFF;
 }
 machine_add_tickfunction(devinit->machine,
     dev_footbridge_tick, d, 14);
 devinit->return_ptr = d->pcibus;
 return 1;
}
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpedantic"
#pragma GCC diagnostic pop
struct settings *global_settings;
int extra_argc;
char **extra_argv;
char *progname = (char *) "fbpending_bound";
size_t dyntrans_cache_size = (96*1048576);
static struct machine fake_machine;
static struct cpu fake_cpu;
static int failures;
static int rows;
static void row(const char *name, int good, const char *fmt, ...)
{
 va_list ap;
 printf("  %-4s %-44s ", good ? "ok" : "FAIL", name);
 __builtin_va_start(ap,fmt);
 vprintf(fmt, ap);
 __builtin_va_end(ap);
 printf("\n");
 rows ++;
 if (!good)
  failures ++;
}
static void drive(struct footbridge_data *d, int nr, long long n,
 int *peak, int *trough)
{
 long long i;
 *peak = (-0x7fffffff - 1);
 *trough = 0x7fffffff;
 for (i = 0; i < n; i++) {
  switch (nr) {
  case 0: timer_tick0(((void *)0), d); break;
  case 1: timer_tick1(((void *)0), d); break;
  case 2: timer_tick2(((void *)0), d); break;
  case 3: timer_tick3(((void *)0), d); break;
  }
  if (d->pending_timer_interrupts[nr] > *peak)
   *peak = d->pending_timer_interrupts[nr];
  if (d->pending_timer_interrupts[nr] < *trough)
   *trough = d->pending_timer_interrupts[nr];
 }
}
static void arm(struct footbridge_data *d, int nr, uint32_t load, uint32_t control)
{
 d->timer_control[nr] = control;
 d->timer_load[nr] = load & 0x00FFFFFF;
 reload_timer_value(&fake_cpu, d, nr);
}
int main(int argc, char *argv[])
{
 struct footbridge_data *d;
 int peak, trough, nr;
 long long deep = 0;
 double f;
 if (argc > 1)
  deep = atoll(argv[1]);
 fake_cpu.machine = &fake_machine;
 timer_init();
 printf("==============================================================\n");
 printf("fbpending OFFLINE BOUND DETECTOR (rung 1 -- a DETECTOR, not a\n");
 printf("reproduction).  TIMER_MAX_CATCHUP=%d  TIMER_BASE_FREQUENCY=%.0f\n",
     1048576, (double)65.0);
 printf("  the most one timer can be ticked in one wall second: %.0f\n",
     (double)1048576 * 65.0);
 printf("==============================================================\n");
 d = (struct footbridge_data *) calloc(1, sizeof(*d));
 fake_machine.emulated_hz = 50000000;
 arm(d, 0, 1, 0x80);
 drive(d, 0, 4096, &peak, &trough);
 row("R0 the harness can drive the counter at all", peak >= 4096,
     "peak after 4096 direct ticks = %d (expect >= 4096 with no bound)", peak);
 free(d);
 {
  static const struct { int hz; uint32_t load; uint32_t ctrl;
   const char *what; } cases[] = {
      { 50000000, 0x000100, 0x80|0x08, "cats, load 256/256" },
      { 50000000, 0x000001, 0x80, "cats, load 1  (50 MHz)" },
      { 63750000, 0x000001, 0x80, "netwinder, load 1" },
      { 1000000000, 0x000001, 0x80, "-I 1e9, load 1" },
      { 2147483647, 0x000001, 0x80, "-I INT_MAX, load 1" },
      { 2147483647, 0x000000, 0x80, "-I INT_MAX, load 0 (2^24)" },
      { 50000000, 0xFFFFFF, 0x80|0x08, "cats, slowest legal" },
  };
  const int ceiling = (int)(1048576 * (int)65.0);
  size_t c;
  for (c = 0; c < sizeof(cases)/sizeof(cases[0]); c++) {
   int worst_peak = (-0x7fffffff - 1), worst_trough = 0x7fffffff;
   d = (struct footbridge_data *) calloc(1, sizeof(*d));
   fake_machine.emulated_hz = cases[c].hz;
   for (nr = 0; nr < 4; nr++) {
    arm(d, nr, cases[c].load, cases[c].ctrl);
    drive(d, nr, (long long)ceiling + 4096, &peak, &trough);
    if (peak > worst_peak)
     worst_peak = peak;
    if (trough < worst_trough)
     worst_trough = trough;
   }
   f = (double)cases[c].hz /
       (double)footbridge_effective_cycles(cases[c].load & 0x00FFFFFF,
       cases[c].ctrl, 1);
   row("R1 bounded across all 4 timers",
       worst_peak <= ceiling && worst_trough >= 0,
       "%-28s rate %12.2f Hz  peak %11d trough %11d  (ceiling %d)",
       cases[c].what, f, worst_peak, worst_trough, ceiling);
   {
    int want = (int) f;
    if (want < 1)
     want = 1;
    if (want > ceiling)
     want = ceiling;
    row("R5 the bound IS this timer's rate",
        worst_peak == want,
        "%-28s peak %11d  want %11d", cases[c].what,
        worst_peak, want);
   }
   row("R3 the reset still owes one interrupt",
       worst_trough >= 1,
       "%-28s lowest value the counter ever held: %d",
       cases[c].what, worst_trough);
   free(d);
  }
 }
 if (deep > 0) {
  d = (struct footbridge_data *) calloc(1, sizeof(*d));
  fake_machine.emulated_hz = 2147483647;
  arm(d, 0, 1, 0x80);
  drive(d, 0, deep, &peak, &trough);
  row("R2 no signed overflow", trough >= 0 && peak >= 0,
      "%lld direct ticks: peak %d trough %d", deep, peak, trough);
  free(d);
 } else {
  printf("  --   R2 no signed overflow                       "
         "SKIPPED (pass a depth, e.g. 2147487744)\n");
 }
 {
  int peak, trough;
  struct footbridge_data *r6 =
      (struct footbridge_data *) calloc(1, sizeof(*r6));
  fake_machine.emulated_hz = 50000000;
  arm(r6, 0, 1, 0x80);
  arm(r6, 1, 256, 0x80 | 0x08);
  arm(r6, 0, 256, 0x80 | 0x08);
  drive(r6, 0, 4096, &peak, &trough);
  row("R6 a re-armed timer's bound follows its NEW rate",
      peak == 762, "timer 0 re-armed 50 MHz -> 762 Hz: peak %d want 762",
      peak);
  drive(r6, 1, 4096, &peak, &trough);
  row("R6b each timer carries its OWN bound",
      peak == 762, "timer 1: peak %d want 762", peak);
  free(r6);
 }
 {
  int sc_f = failures, sc_r = rows, sc_bad = 0;
  row("@@SELFCHECK@@/false", 0, "a deliberate mismatch");
  if (failures <= sc_f)
   sc_bad++;
  failures = sc_f; rows = sc_r;
  row("@@SELFCHECK@@/true", 1, "a deliberate match");
  if (failures != sc_f)
   sc_bad++;
  failures = sc_f; rows = sc_r;
  row("SELFCHECK the comparator can still fail", sc_bad == 0,
      "both directions");
 }
 row("R4 every case bounded (the selfmutant pin)", failures == 0,
     "%d row failure(s) above", failures);
 row("IDENTITY: row count", rows + 1 == (deep > 0 ? 28 : 27),
     "%d rows (expect %d with R2, %d without)",
     rows + 1, 28, 27);
 printf("\nFBBOUND_%s\n", failures ? "FAIL" : "PASS");
 return failures ? 1 : 0;
}
