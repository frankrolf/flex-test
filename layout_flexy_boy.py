'''
Make a PDF illustrating different variations of flex in different sizes.
'''

import os
import sys
import subprocess
import drawBot as db

MARGIN = 40  # pt
TEXTBOX_HEIGHT = 100
FLEX_FONT_PATH = 'build/FlexyBoy-Regular.otf'

if not os.path.exists(FLEX_FONT_PATH):
    sys.exit('No flex font found! Please consult the README.md file :-)')


def make_label(message):
    label = db.FormattedString(
        message,
        font='SourceCodePro-Regular',
        fontSize=10,
    )
    return label


def make_flex_page(flex_option, description=None):
    db.newPage('Letter')

    # how many sizes to show
    pt_size_step = 10
    font_sizes = range(pt_size_step, 100 + pt_size_step, pt_size_step)

    # text area of the description
    description_width = 100

    # text area of the content
    content_width = db.width() - MARGIN - description_width

    x_step = content_width / len(font_sizes)
    y = db.height() - MARGIN  # position of first line
    headline = make_label(description)
    db.text(headline, (MARGIN, y))

    for flex_amount in range(6):
        x = MARGIN + description_width
        y -= TEXTBOX_HEIGHT

        if flex_amount > 0:
            feature_name = f'ss{flex_amount:02}'
            for font_size in font_sizes:
                fs = db.FormattedString(
                    flex_option,
                    font=FLEX_FONT_PATH,
                    fontSize=font_size,
                    openTypeFeatures={
                        feature_name: True
                    },
                )
                size_fs = make_label(str(font_size))
                db.text(fs, (x, y), align='center')
                db.text(size_fs, (x, y - 20), align='center')
                x += x_step
        else:
            for font_size in font_sizes:
                fs = db.FormattedString(
                    flex_option,
                    font=FLEX_FONT_PATH,
                    fontSize=font_size,
                )
                size_fs = make_label(str(font_size))
                db.text(fs, (x, y), align='center')
                db.text(size_fs, (x, y - 20), align='center')
                x += x_step
        label = make_label(f'flex{flex_amount}')

        db.text(
            label,
            (MARGIN, y),
        )


flex_options = {
    'V': 'vertical curveTo flex',
    'v': 'vertical lineTo flex',
    'H': 'horizontal curveTo flex',
    'h': 'horizontal lineTo flex',
}

for flex_option, description in flex_options.items():
    make_flex_page(flex_option, description)

pdf_path = os.path.abspath('build/flex test.pdf')
db.saveImage(pdf_path)
subprocess.call(['open', pdf_path])
