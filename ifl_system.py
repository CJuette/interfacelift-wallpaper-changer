import webbrowser

def openLink(url):
    print("Trying to open link %s" % url)
    webbrowser.open(url, new=2, autoraise=True)