import subprocess
import re

def remove_custom_emoji(text):
    pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'
    return re.sub(pattern, '', text)

def urlAbb(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern, '糞なげえし読んでやらんからな！', text)

def create_WAV(input_text):
    input_text_removed_emoji = remove_custom_emoji(input_text)
    input_text_removed_emoji_and_url = urlAbb(input_text_removed_emoji)
    input_file = 'input.txt'

    with open(input_file, 'w', encoding='shift-jis') as file:
        file.write(input_text_removed_emoji_and_url)

    command = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/open_jtalk -x {x} -m {m} -r {r} -ow {ow} {input_file}'

    dictionary_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/dic'

    
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/mei/mei_normal.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/mei/mei_bashful.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/mei/mei_angry.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/mei/mei_happy.htsvoice'
    voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/mei/mei_sad.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/othervoice/H-09.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/othervoice/雪音ルウ２.htsvoice'
    # voice_path = 'C:/Users/hapit/Documents/practice/chinko-talk/open_jtalk-1.11/bin/othervoice/風音桜凪.htsvoice'

    voice_speed = '0.9'

    output_file_name = 'output.wav'

    args= {'x':dictionary_path, 'm':voice_path, 'r':voice_speed, 'ow':output_file_name, 'input_file':input_file}

    cmd = command.format(**args)
    print(cmd)

    subprocess.run(cmd)
    return True

if __name__ == '__main__':
    create_WAV('テスト')