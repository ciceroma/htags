htags
=====

Simple HTML tags generator library

This library contains some common tags used in html file

If you want simply format some data in your python code,
or generating a simple html page in your CGI program,
and don't want write too much code, you can use this
eg.
	h = Html("title");
	h.add(H1("see?"));
	h.add(Ol(dir("")));
	print h.cont();
see test() function for more