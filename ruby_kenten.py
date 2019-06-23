#!/usr/bin/env python

from pandocfilters import toJSONFilter, Str, RawInline, RawBlock, Header
import regex

def ruby(key, val, fmt, meta):
    if key == 'Header':
        val[1][0] = val[2][0]['c']
        return Header(val[0], val[1], val[2])
    if key != 'Str':
        return
    filteredVal = val
    for matchedVals in regex.findall(r'(?:(?:｜(?:\p{Hiragana}|\p{Katakana}|\p{Han}|ー|\p{P})+?)|(?:\p{Han}+?))《.*?》', filteredVal):
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
        filteredVal = regex.sub(r'%s' % matchedVals, r'%s' % filteredStr, filteredVal)
    for matchedVals in regex.findall(r'《《(?:\p{Hiragana}|\p{Katakana}|\p{Han}|\p{P}|ー)+?》》', filteredVal):
        base = regex.search(r'《《(.+?)》》', matchedVals).groups(0)[0]
        if fmt == 'latex':
            filteredStr = r'\\kenten{%s}' % base
        elif fmt == 'html' or 'html5' or fmt == 'epub' or fmt == 'epub3':
            kenten = ''
            for kentenCount in base:
                kenten += r'・'
            filteredStr = r'<ruby><rb>%s</rb><rp>《</rp><rt>%s</rt><rp>》</rp></ruby>' % (base,kenten)
        filteredVal = regex.sub(r'%s' % matchedVals, r'%s' % filteredStr, filteredVal)
    
    filteredVal = regex.sub(r'｜《', r'《', filteredVal)

    if 'matchedVals' in locals():
        if fmt == 'latex':
            return RawInline('latex',r'%s' %filteredVal)
        elif fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
            return RawInline('html', r'%s' %filteredVal)
    else:
        return Str(filteredVal)
    



if __name__ == '__main__':
    toJSONFilter(ruby)