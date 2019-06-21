#!/usr/bin/env python

from pandocfilters import toJSONFilter, Str, RawInline, RawBlock
import regex

def ruby(key, val, fmt, meta):
    if key == 'Header' and fmt == 'latex':
        headerLevel = val[0]
        val = val[1][0]
        val = r'\section{%s}' %val
        for i in range(headerLevel - 1):
            val = regex.sub(r'^.', r'\sub', val)
        return RawBlock('tex', val)
    if key != 'Str':
        return
    for matchedVals in regex.findall(r'(?:(?:｜(?:\p{Hiragana}|\p{Katakana}|\p{Han}|ー)+?)|(?:\p{Han}+?))《.*?》', val):
        base = regex.search(r'(((?<=｜)(.*?)(?=《))|(\p{Han}*?(?=《)))', matchedVals).groups(1)[0]
        ruby = regex.search(r'((?<=《)(.*?)(?=》))', matchedVals).groups(1)[1]
        filteredRuby = regex.search(r'^((.*?)(?=｜))', ruby)[0] if regex.search(r'(.*)?｜(?!.*《)(?!.*｜)', ruby) else ruby
        for groupedRuby in regex.findall(r'(((?<=｜)(.*?)(?=｜))|((?<=｜)(.*)(?=$)))', ruby):
            if fmt == 'latex':
                filteredRuby = r'%s|%s' % (filteredRuby,groupedRuby[0])
            elif fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
                filteredRuby = r'%s%s' % (filteredRuby,groupedRuby[0])
        ruby = filteredRuby
        if fmt == 'latex':
            filteredStr = r'\\ruby{%s}{%s}' % (base,ruby)
        elif fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
            filteredStr = r'<ruby><rb>%s</rb><rp>《</rp><rt>%s</rt><rp>》</rp></ruby>' % (base,ruby)
        val = regex.sub(r'%s' % matchedVals, r'%s' % filteredStr, val)

    for matchedVals in regex.findall(r'《《(?:\p{Hiragana}|\p{Katakana}|\p{Han}|\p{P}|ー)+?》》', val):
        base = regex.search(r'《《(.+?)》》', matchedVals).groups(0)[0]
        if fmt == 'latex':
            filteredStr = r'\\kenten{%s}' % (base)
        elif fmt == 'html' or 'html5' or fmt == 'epub' or fmt == 'epub3':
            kenten = ''
            for kentenCount in base:
                kenten += r'・'
            filteredStr = r'<ruby><rb>%s</rb><rp>《</rp><rt>%s</rt><rp>》</rp></ruby>' % (base,kenten)
        val = regex.sub(r'%s' % matchedVals, r'%s' % filteredStr, val)

    if regex.search(r'｜《', val):
        val = regex.sub(r'｜《', r'《', val)

    if fmt == 'latex':
        return RawInline('tex', r'%s' %val)
    elif fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
        return RawInline('html', r'%s' %val)


if __name__ == '__main__':
    toJSONFilter(ruby)