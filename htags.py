# Author: cicero ma
# Contact: mawenping@gmail.com

"""Simple HTML tags generator library

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
"""

class DefaultStyle():
	def __init__(self):
		pass;
	def __str__(self):
		return """	<style>
		//li {float: left; margin-left:20px;font-family:"consolas"}
		li {margin-left:10px;font-family:"consolas"; font-size:12px;}
		table {
			border-collapse:collapse; 
			font-family:"consolas";
			font-size: small;
		}
		table,tr,th,td {border: 1px solid green;}
			th{ background-color:lightgreen; }
		table.noborder, .noborder tr, .noborder td {border: 0px;}
			.noborder th {border: 0px; background-color:white;}
		table.hasborder, .hasborder tr, .hasborder td {border: 1px solid green;}
			.hasborder th {border: 1px solid green; background-color:lightgreen;}
			
		pre,code {
			font-family:"courier new"; font-size:12px;
			background-color: #ffc;
			border: solid 1px #999;  
			box-shadow: 0 1px 1px #ccc;
			padding: 0.5em 1em;
		}
		hr { height:1px;border-width:0;color:gray;background-color:gray }
		</style>
		""";

class Html():
	template = """<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=%s">
		<title>%s</title>
		%s
	</head>
	<body>
		%s
	</body>
	</html>""";
	def __init__(self,title="",body=[],encoding="utf8"):
		if isinstance(title,list):
			body,title = title,body;
			if isinstance(title,list): title = '';
		self.title = title;
		self.head = [DefaultStyle()];
		self.body = body;
		self.encoding = encoding;
	def addhead(self,elem):
		if isinstance(elem,list): self.body.extend(elem);
		else: self.body.append(elem);
	def add(self,elem):
		if isinstance(elem,list): self.body.extend(elem);
		else: self.body.append(elem);
	def __str__(self):
		hh = map(str,self.head);
		bb = map(str,self.body);
		heads = "\n".join(hh);
		elems = "\n".join(bb);
		return self.template%(self.encoding,self.title,heads,elems);
	def __unicode__(self):
		hh = map(unicode,self.head);
		bb = map(unicode,self.body);
		heads = "\n".join(hh);
		elems = "\n".join(bb);
		return self.template%(self.encoding,self.title,heads,elems);
	def cont(self):
		return unicode(self).encode(self.encoding);
	def render(self):
		print self.cont();
		
class Element(object):
	def __init__(self,*cont,**kwargs):
		object.__setattr__(self,"attribs",kwargs);
		if len(cont)==0: 
			object.__setattr__(self,"cont",[]);
		elif isinstance(cont[0],list):
			object.__setattr__(self,"cont",cont[0]);
		else:
			object.__setattr__(self,"cont",[unicode(cont[0])]);
			
	def __getattr__(self,k):
		if self.attribs.has_key(k):
			return self.attribs[k];
		else: raise AttributeError();
	def __setattr__(self,k,v):
		self.attribs[k]=v;
	def add(self,cont):
		if isinstance(cont,list):
			self.cont.extend(cont);
		else: 
			self.cont.append(cont);
	def __unicode__(self):
		lis = "".join([unicode(li) for li in self.cont]);
		attrs = self.attribs.items();
		if len(attrs)>0:
			aa = " ".join(["%s='%s'"% (k,unicode(v)) for k,v in attrs]);
			if len(lis)>0:
				return "<%s %s>%s</%s>\n" % (self.tag, aa, lis, self.tag);
			else:
				return "<%s %s />\n" % (self.tag, aa);
		else:
			if len(lis)>0:
				return "<%s>%s</%s>\n" % (self.tag,lis,self.tag);
			else:
				return "<%s />" % (self.tag);
		pass;
class Pre(Element):
	tag = "pre";
class Code(Element):
	tag = "code";
class B(Element):
	tag = "b";
class I(Element):
	tag = "i";
class U(Element):
	tag = "u";
class Center(Element):
	tag = "center";
class P(Element):
	tag = "p";
class H1(Element):
	tag = "h1";
class H2(Element):
	tag = "h2";
class H3(Element):
	tag = "h3";
class H4(Element):
	tag = "h4";	
class H5(Element):
	tag = "h5";	
class H6(Element):
	tag = "h6";	

class A(Element):
	tag = 'a';

class ListElement(Element):
	def __init__(self,cont,**kwargs):
		if isinstance(cont,list):
			cl = self.memberclass;
			cont = map(lambda x: (isinstance(x,cl) and x) or cl(x),cont);
		Element.__init__(self,cont,**kwargs);
	def add(self,el):
		if not isinstance(el,self.memberclass):
			el = self.memberclass(el);
		Element.add(self,el);
	def addlist(self,ll):
		for l in ll: self.add(l);
		
class Li(Element):
	tag = "li";
class Ul(ListElement):
	tag = "ul";
	memberclass = Li;
class Ol(Ul):
	tag = "ol";

class Form(Element):
	tag = 'form';
class Input(Element):
	tag = 'input';

class Option(Element):
	tag = 'option';
	def __init__(self,cont,**kwargs):
		kwargs.setdefault("value",unicode(cont));
		Element.__init__(self,cont,**kwargs);
	
class Select(ListElement):
	tag = 'select';
	memberclass = Option;
	
class SingleElem():
	def __init__(self,num=1):
		self.number = num;
	def __str__(self):
		return ("<%s />"%(self.tag))*self.number;
class Br(SingleElem):
	tag = 'br';
class Hr(SingleElem):
	tag = "hr";

class Img(Element):
	tag = 'img';
	def __init__(self,*cont,**kwargs):
		if len(cont)>0:
			kwargs.setdefault("src",unicode(cont[0]));
		Element.__init__(self,**kwargs);

class Td(Element):
	tag = 'td';
class Th(Element):
	tag = 'th';
class Tr(ListElement):
	tag = 'tr';
	memberclass = Td;
class HelperTrheader(ListElement):
	tag = 'tr';
	memberclass = Th;
class Table(ListElement):
	tag = 'table';
	memberclass = Tr;
	def __init__(self,*cont,**kwargs):
		if len(cont)>0 and isinstance(cont[0],list):
			if isinstance(cont[0][0],list):
				ListElement.__init__(self,cont[0],**kwargs);
			else: 
				ListElement.__init__(self,[],**kwargs);
				self.addhead(cont[0]);
		else:
			ListElement.__init__(self,[],**kwargs);
	def addhead(self,hd):
		if not isinstance(hd,HelperTrheader):
			hd = HelperTrheader(hd);
		self.cont.insert(0,hd);
		
class SimpleTable(Element):
	def __init__(self,col=0,**kwargs):
		Element.__init__(self,**kwargs);
		object.__setattr__(self,"head","");
		if isinstance(col,list):
			object.__setattr__(self,"col",0);
			self.sethead(col);
		else:
			object.__setattr__(self,"col",col);
	def sethead(self,r):
		col = self.col;
		if len(r)>col: object.__setattr__(self,"col",len(r));
		if len(r)<col: r.extend(["" for i in range(col-len(r))]);
		head = "<tr>%s</tr>\n" % " ".join(["<th>%s</th>"%t for t in r]);
		object.__setattr__(self,"head",head);
	def addrow(self,r):
		ct = " ".join(["<td>%s</td>"%t for t in r]);
		self.cont.append("<tr>%s</tr>"%ct);
	def addlist(self,ls):
		i=0;
		while i<len(ls):
			self.addrow(ls[i:i+self.col]);
			i = i+self.col;
	def __unicode__(self):
		aa = " ".join(["%s='%s'"% (k,unicode(v)) for k,v in self.attribs.items()]);
		return "<table %s>%s\n%s</table>" % (aa,self.head,"\n".join(self.cont));


def test():
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
	
	right = Td(["this is a table"],width="200px");
	
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
	h.render();


if __name__=="__main__":
	test();










