import json, re, os, time

def parse(file, debug=False):
	if debug: _stime = time.time()
	_f = open(os.path.join(file),'r')
	
	read_all = False
	_dict = '{'
	_fval = None
	
	for line in _f.readlines():
		if line == '#READ ALL\n':
			read_all = True
		
		if not _fval:
			_re = re.search('<[\w-]*>',line)
			
			if _re:
				_fval = _re.group(0)
		else:
			try:
				if read_all:
					_farg = re.search('<[\w-]*>',line).group(0)
					_larg = re.search('</[\w-]*>',line).group(0)
					_val = line[line.find(_farg)+len(_farg):line.find(_larg)]
					_dict += '\"%s\":\"%s\"}\n{' % (_farg[1:len(_farg)-1],_val)
					
					if reduce(lambda u,v: u.strip(v), [_re.group(0), '</', '>']) == reduce(lambda u,v: u.strip(v), [_farg, '<', '>']):
						_dict = _dict[:len(_dict)-1]
						_fval = None
				else:
					_farg = re.search('<[\w-]*>',line).group(0)
					_larg = re.search('</[\w-]*>',line).group(0)
					_val = line[line.find(_farg)+len(_farg):line.find(_larg)]
					_dict += '\"%s\":\"%s\",' % (_farg[1:len(_farg)-1],_val)
				
			except:
				#who cares
				pass
			
			#Look for the closing tag
			_re = re.search('</[\w-]*>',line)
			
			if _re and not read_all:
				if reduce(lambda u,v: u.strip(v), [_re.group(0), '</', '>']) == reduce(lambda u,v: u.strip(v), [_fval, '<', '>']):
					_dict = _dict[:len(_dict)-1] + '}\n{'
					_fval = None
						
	if _dict[len(_dict)-1] == '{':
		_dict = _dict[:len(_dict)-1]
		
	_f = open(file.split('.')[0]+'.json','w')
	_f.write(_dict)
	_f.close()
	
	if debug: print '%s -> %s (took %s)' % (file,file.split('.')[0]+'.json',time.time()-_stime)