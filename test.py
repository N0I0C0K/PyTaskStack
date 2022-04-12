from TaskStack import *
url, sess = applySession('test', 'ipconfig')
print(url)
runSession(sess)
