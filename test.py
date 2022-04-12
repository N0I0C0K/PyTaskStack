from TaskStack import *
url, sess = applySession('test', 'python -c "print(1+2+3)"')
print(url)
runSession(sess)
