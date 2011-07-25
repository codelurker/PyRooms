import json, re, os, sys

if not len(sys.argv) > 1: sys.exit()

def parse():
	_f = open(os.path.join(sys.argv[1]),'r')
	
	_dict = ''
	_fval = None
	
	for line in _f.readlines():
		if not _fval:
			_re = re.search('<\w*>',line)
			
			if _re:
				_fval = _re.group(0)
				_dict += '{'
		else:
			try:
				_farg = re.search('<\w*>',line).group(0)
				_larg = re.search('</\w*>',line).group(0)
				_val = line[line.find(_farg)+len(_farg):line.find(_larg)]
				#print '{\"%s\":\"%s\"}' % (_farg,_val)
				_dict += '\"%s\":\"%s\",' % (_farg[1:len(_farg)-1],_val)
				
			except:
				#who cares
				pass
			
			#Look for the closing tag
			_re = re.search('</\w*>',line)
			
			if _re:
				#if _re.group(0).partition('/')[2] == _fval[1:]:
				if reduce(lambda u,v: u.strip(v), [_re.group(0), '</', '>']) == reduce(lambda u,v: u.strip(v), [_fval, '<', '>']):
					_dict = _dict[:len(_dict)-1] + '}'
					_fval = None
	
	return _dict

def save(f,file):
	f = f.replace('}','}\n').replace(',','\n\t')
	
	_f = open(file,'w')
	_f.write(f)
	_f.close()

_ret = parse()
save(_ret,sys.argv[1].split('.')[0]+'.json')