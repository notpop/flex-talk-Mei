import re

def remove_custom_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'
    return re.sub(pattern, '', text)

def urlAbb(text):
    pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern, '糞なげえし読んでやらんからな！', text)
