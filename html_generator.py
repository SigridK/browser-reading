# coding:utf-8

# imports
import argparse
import pandas as pd
import codecs
import json
#import os

parser = argparse.ArgumentParser(
    description="""output html-format ready for presentation
    in browser. Expects texts to have two tab-separated
    columns: ID, string.
    Will output one html doc for presenting each line as
    a separate image on screen to be advanced by keypress.
    Formated according to provided css styles.""")
parser.add_argument("css",
    help="style file for bounding boxes",
    default='style.css', nargs='?')
parser.add_argument("exp_id",
    help="identifier showed as tab-title in browser",
    default='A', nargs='?')
parser.add_argument("strings",
    help="text file with one id+stimulus per line",
    default='stimuli', nargs='?')
parser.add_argument("out_prefix", 
    help="path and prefix to stimulus files",
    default='', nargs='?')
args = parser.parse_args()

def spans(tokens):
    """Identify which characters that'll
    acquire additional white space 
    (always half a white-space char on each side)"""
    spans = []
    for token_i, token in enumerate(tokens):
        chars = list(token.strip())
        for char_i, char in enumerate(chars):
            # will break if a token starts with a punctuation mark.
            if char in ('?', '!', ':', ';', ',', '.') and not chars[char_i-1].isdigit():
                char_class = 'last'
                # Change the span class of previous character
                if len(spans) > 0:
                    last_char_class = spans[-1][2]
                    if last_char_class == 'single':
                        spans[-1][2] = 'first'
                    else:
                        spans[-1][2] = 'middle'
            elif len (chars) == 1:
                char_class = 'single'
            elif char_i == 0:
                char_class = 'first'
            elif char_i == len(chars)-1:
                char_class = 'last'
            else:
                char_class = 'middle'

            # first, middle, last
            spans.append([token_i, char_i, char_class, char, 0])
        spans[-1][4] = token.count("\n")

    span_strs = []
    for span in spans:
        char_str = u"<span id='{0:04d}-{1:02d}' class='char {2}'>{3}</span>".format(*span)
        if span[2] == "first":
            token_start = u"<span class='token'>"
            span_strs.append(token_start+char_str)
        elif span[2] == "last":
            token_end = u"</span>"
            span_strs.append(char_str+token_end)
        elif span[2] == "single":
            token_start = u"<span class='token'>"
            token_end = u"</span>"
            span_strs.append(token_start+char_str+token_end)
        else:
            span_strs.append(char_str)
        if span[4]:
            for _ in range(span[4]):
                span_strs.append(u"<br/>")
    return u"".join(span_strs)

def divs(stims):
    """Add div containers to each screen by its id."""
    return u"\t<div id='{0}' class='screen'>\n{1}\n\t</div>".format(
        stims.sc_id,stims.screen)

# open the texts as dataframe
stimuli = pd.read_csv(args.strings, encoding='utf-8',
    header=None, sep='\t', names=['sc_id','screen'])

# apply transformation to stimuli
stimuli.screen = stimuli.screen.str.replace("\n", "\n ")
stimuli.screen = stimuli.screen.str.split(" ")
stimuli.screen = stimuli.screen.apply(spans)
stimuli.screen = stimuli.apply(divs,axis=1)

x_screen = "\n<div id='x_screen' class='screen'><span id='x' class='x'>+</span></div>\n"


# extract the stimuli as one string
all_containers = x_screen+x_screen.join(stimuli.screen.values)
#print(body)

# extract css info
#css_content = codecs.open(args.css, encoding='utf-8').read()

# assemble html with reference to specified css file
html_scripts =u"""
        <script type="text/javascript" src="jquery-2.1.4.min.js"></script>
        <script type="text/javascript">

            function measure_boxes(screen_elem) {
                var timestamp = $.now()
                var boxes = $(".char",screen_elem).map(function(index, char_elem) {
                    var bb = char_elem.getBoundingClientRect()
                    return {text: char_elem.textContent,
                               id: char_elem.getAttribute("id"),
                               bottom: bb.bottom,
                               height: bb.height,
                               left: bb.left,
                               right: bb.right,
                               top: bb.top,
                               width: bb.width
                            }

                })
                var clean_boxes = boxes.get()
                $.post("http://localhost:5000/space", JSON.stringify({boxes:clean_boxes,
                    timestamp:timestamp,
                    screen_id:screen_elem.attr("id")}
                    ))

            }
            $(document).ready(function() {
                $(".screen").hide()
                $(".screen").first().show()

                $(document).keyup(function(key_event) {
                    // 49 is 1, 50 is 2, 51 is 3
                    if (key_event.which==49||key_event.which==50||key_event.which==51||key_event.which==32) {
                        var current_visible = $(".screen:visible").first()
                        current_visible.hide()
                        current_visible = current_visible.next(".screen").show()
                        measure_boxes(current_visible)
                    }

                    // press 0 for quitting
                    if (key_event.which==48) {
                        $.post("http://localhost:5000/shutdown", "shutdown")
                        //var current_visible = $(".screen:visible").first()
                        //current_visible.hide()
                        //current_visible = current_visible.next(".screen").show()
                        //measure_boxes(current_visible)
                    }

                })
            }) 
    """
html = u"""
<html>
    <head>
        <meta charset="UTF-8"/>
        <title>{title}</title>
        <link rel="stylesheet" type="text/css" href="{css}"/>
        {scripts}
        </script>
    </head>

    <body>
       {all_containers}
    </body>
</html>
""".format(title=args.exp_id,css=args.css,
    scripts=html_scripts,all_containers=all_containers)

# Write html file
out_filename = args.out_prefix+args.exp_id+'.html'
print(out_filename)
with codecs.open(
    out_filename, 'w', encoding='utf-8') as out_file:
    out_file.write(html)