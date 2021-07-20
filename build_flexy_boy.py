'''
Builds a UFO file which contains dummy glyphs to demonstrate different amounts
of Flex. Unflexed glyphs are represented through characters:

    V - vertical stem using curve to flex
    v - vertical stem using lines
    H - horizontal bar using curve to flex
    h - horizontal bar using lines

Flex alternates are applied through stylistic sets.

    ss01: 1 unit flex
    ss02: 2 units flex
    etc.


Requirements: fontParts
'''

import os
from fontParts.fontshell import RFont


def make_ss_feature(flex_index):
    '''
    build a single ssXX feature tailored to this project
    '''
    g_names = [
        'flex_stem_curve',
        'flex_stem_line',
        'flex_bar_curve',
        'flex_bar_line',
    ]

    f_name = f'ss{flex_index:02}'

    feature_prologue = f'feature {f_name} {{'
    feature_epilogue = f'}} {f_name};\n'
    feature_text = [feature_prologue]
    for g_name in g_names:
        feature_line = f'\tsub {g_name}_0 by {g_name}_{flex_index};'
        feature_text.append(feature_line)
    feature_text.append(feature_epilogue)
    return '\n'.join(feature_text)


def flex_stem(flex_amount, curve=True):
    if curve:
        g_name = f'flex_stem_curve_{flex_amount}'
        char = 'V'
    else:
        g_name = f'flex_stem_line_{flex_amount}'
        char = 'v'
    g = f.newGlyph(g_name, clear=True)

    if flex_amount == 0:
        g.unicode = ord(char)
    height = 500
    stem = 100
    g.width = 500
    p = g.getPen()
    right_x = g.width / 2 + stem / 2
    left_x = g.width / 2 - stem / 2
    bot_r = (right_x, 0)
    bot_l = (left_x, 0)
    top_r = (right_x, height)
    top_l = (left_x, height)
    mid_r = (right_x - flex_amount, height / 2)
    mid_l = (left_x + flex_amount, height / 2)
    bez_length = height / 2 / 3
    p.moveTo(bot_l)
    p.lineTo(bot_r)

    # draw the right side
    if curve:
        p.curveTo(
            (right_x - flex_amount / 2, bez_length),
            (right_x - flex_amount, height / 2 - bez_length),
            mid_r)
        p.curveTo(
            (right_x - flex_amount, height / 2 + bez_length),
            (right_x - flex_amount / 2, height - bez_length),
            top_r)
    else:
        p.lineTo(mid_r)
        p.lineTo(top_r)

    p.lineTo(top_l)

    # draw the left side
    if curve:
        p.curveTo(
            (left_x + flex_amount / 2, height - bez_length),
            (left_x + flex_amount, height / 2 + bez_length),
            mid_l)
        p.curveTo(
            (left_x + flex_amount, height / 2 - bez_length),
            (left_x + flex_amount / 2, bez_length),
            bot_l)

    else:
        p.lineTo(mid_l)
        p.lineTo(bot_l)

    p.closePath()


def flex_bar(flex_amount, curve=True):
    if curve:
        g_name = f'flex_bar_curve_{flex_amount}'
        char = 'H'
    else:
        g_name = f'flex_bar_line_{flex_amount}'
        char = 'h'
    g = f.newGlyph(g_name, clear=True)
    if flex_amount == 0:
        g.unicode = ord(char)

    width = 500
    height = 100
    g.width = 700
    p = g.getPen()
    right_x = g.width / 2 + width / 2
    left_x = g.width / 2 - width / 2
    bot_r = (right_x, 0)
    bot_l = (left_x, 0)
    top_r = (right_x, height)
    top_l = (left_x, height)
    mid_x = g.width / 2
    bez_length = width / 2 / 3
    p.moveTo(bot_l)

    # draw the bottom side
    if curve:
        p.curveTo(
            (left_x + bez_length, flex_amount / 2),
            (mid_x - bez_length, flex_amount),
            (mid_x, flex_amount))
        p.curveTo(
            (mid_x + bez_length, flex_amount),
            (right_x - bez_length, flex_amount / 2),
            bot_r)
    else:
        p.lineTo((mid_x, flex_amount))
        p.lineTo(bot_r)

    p.lineTo(top_r)

    # draw the top side
    if curve:
        p.curveTo(
            (right_x - bez_length, height - flex_amount / 2),
            (mid_x + bez_length, height - flex_amount),
            (mid_x, height - flex_amount))
        p.curveTo(
            (mid_x - bez_length, height - flex_amount),
            (left_x + bez_length, height - flex_amount / 2),
            top_l)
    else:
        p.lineTo((mid_x, height - flex_amount))
        p.lineTo(top_l)

    p.closePath()


def make_goadb(f):
    goadb_lines = []
    for g_name in f.glyphOrder:
        uc_value = f[g_name].unicode
        line = [g_name, g_name]
        if uc_value:
            line.append(f'uni{uc_value:04X}')
        goadb_lines.append('\t'.join(line))
    return('\n'.join(goadb_lines) + '\n')


if __name__ == '__main__':

    f = RFont()
    # max amount of flex desired
    max_flex = 5

    nd = f.newGlyph('.notdef')
    nd.width = 0
    space = f.newGlyph('space')
    space.width = 500

    # font info
    f.info.familyName = 'Flexy Boy'
    f.info.styleName = 'Regular'
    f.info.postscriptFontName = 'FlexyBoy-Regular'
    f.info.versionMajor = 1
    f.info.versionMinor = 0

    # no functional effect, but keeping makeotf from complaining
    # XXX (does not seem to have any effect at all. makeotf bug?)
    # f.info.descender = -250
    # f.info.ascender = 750
    # f.info.openTypeOS2TypoDescender = -250
    # f.info.openTypeOS2TypoAscender = 750
    # f.info.openTypeOS2WinAscent = 750
    # f.info.openTypeOS2WinDescent = 250

    # guesstimates
    f.info.postscriptBlueValues = [
        -max_flex, 0,
        100, 100 + max_flex,
        500, 500 + max_flex]
    f.info.postscriptStemSnapV = [100]
    f.info.postscriptStemSnapH = [100]

    # build the flex glyphs
    for flex_amount in range(max_flex + 1):
        flex_stem(flex_amount)
        flex_stem(flex_amount, False)
        flex_bar(flex_amount)
        flex_bar(flex_amount, False)

    # sort the font
    f.glyphOrder = ['.notdef', 'space'] + sorted(
        [name for name in f.glyphOrder if 'flex' in name])

    # write the features
    feature_text = (
        'languagesystem DFLT dflt;'
        '\n'
        'languagesystem latn dflt;'
        '\n'
    )
    for i in range(1, max_flex + 1):
        feature_text += make_ss_feature(i)

    f.features.text = feature_text

    # make output dir
    output_dir = os.path.join(os.path.dirname(__file__), 'build')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # done
    f.save(os.path.join(output_dir, 'FlexyBoy-Regular.ufo'))

    # write GlyphOrderAndAliasDB to output dir
    goadb = make_goadb(f)
    with open(os.path.join(output_dir, 'GlyphOrderAndAliasDB'), 'w') as go:
        go.write(goadb)
