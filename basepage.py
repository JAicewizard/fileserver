def html(bodyPs,cssf, jsf):
	import os
	AP = os.listdir("html/")
	body=""
	page=""
	print(bodyPs,"IM")
	for i in range(len(bodyPs)):
		bodynm = "{0}.html".format(bodyPs[i])
		print (bodynm,AP)
		if bodynm in AP:
			BHF = "html/{}".format(bodynm)
			print(BHF)
			body += "{0}".format(open(BHF).read())
			#print(body, bodynm)
	CP = os.listdir("css/")
	css=""
	for cssf in CP:
		cs = "css/{}".format(cssf)
		css += open(cs).read().replace('\n','')
	JSP = os.listdir("js/")
	js=""
	for i in range(len(jsf)):
		jspf = "{0}.js".format(jsf[i])
		if jspf in JSP:
			jsl = "js/{}".format(jspf)
			js += '<script type="text/javascript">{0}</script>'.format(open(jsl).read())
	#print(js)
	html='<html><head><title>{{page}}</title><style type="text/css">{css}</style>{javas}</head><body>{body}</body><footer></footer></html>'.format(body = body,css = css,javas = js)


	return html
