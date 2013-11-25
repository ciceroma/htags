#!python

from htags import *;

class CgiParam(object):
	def __init__(self):	
		dt = {};
		form = cgi.FieldStorage();
		for k in form:
			dt[k] = form.getvalue(k);
		object.__setattr__(self,"fields",dt);
	def __getattr__(self,k):
		return self.fields[k];
	def has(self,k):
		return self.fields.has_key(k);

def test():
	import cgitb
	cgitb.enable()
	
	h = Html("hello");
	
	tt = Table(Class="noborder",align="center");
	tt.add(Tr(Td(H1("see?"),colspan="2")));
	
	left = Td([
		Code("hello world",style="width:200px;"),
		Hr(),
		Pre("from hell's heart i stab at thee!"),
		Img('http://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Don_Quijote_and_Sancho_Panza.jpg/435px-Don_Quijote_and_Sancho_Panza.jpg'),
		Hr(),
	],width="600px");
	
	right = Td(["hello","world"],width="200px");
	
	t = SimpleTable(map(lambda x: "<----- header %d ---->"%x,range(5)),CLASS="hasborder");
	t.addlist(range(100));
	right.add(t);
	
	f = Form(name='queryinfo');
	f.add(Table([
			["hello:",Input(type="text"),   ],
		    ["aa:",   Input(type="text")    ],
			["cc:",   Input(type="text")    ],
			["bb:",   Input(type="text")    ],
	],CLASS="noborder"));
	
	left.add(f);
	
	tt.add([left,right]);
	h.add(tt);
	print "Content-Type: text/html\n\n";
	h.render();
	
if __name__=="__main__":
	test();