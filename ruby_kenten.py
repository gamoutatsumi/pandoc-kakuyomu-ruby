#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pandocfilters import toJSONFilter, Str, RawInline, Header
import regex

def ruby_kenten(key, val, fmt, meta):
    ruby_pattern = r'(?:(?:｜(?:\p{Hiragana}|\p{Katakana}|\p{Han}|ー|\p{P})+?)|(?:\p{Han}+?))《.*?》'
    kenten_pattern = r'《《(?:\p{Hiragana}|\p{Katakana}|\p{Han}|\p{P}|ー)+?》》'
    if key == 'Header':
        val[1][0] = val[2][0]['c']
        return Header(val[0], val[1], val[2])
    if key != 'Str':
        return
    filtered_val = val
    for matched_vals in regex.findall(ruby_pattern, filtered_val):
        base = regex.search(r'(((?<=｜)(.*?)(?=《))|(\p{Han}*?(?=《)))', matched_vals).groups(1)[0]
        ruby = regex.search(r'((?<=《)(.*?)(?=》))', matched_vals).groups(1)[1]
        filtered_ruby = regex.search(r'^((.*?)(?=｜))', ruby)[0] if regex.search(r'(.*)?｜(?!.*《)(?!.*｜)', ruby) else ruby
        for grouped_ruby in regex.findall(r'(((?<=｜)(.*?)(?=｜))|((?<=｜)(.*)(?=$)))', ruby):
            if fmt == 'latex':
                filtered_ruby = r'%s|%s' % (filtered_ruby, grouped_ruby[0])
            elif fmt in ('html', 'html5', 'epub', 'epub3'):
                filtered_ruby = r'%s%s' % (filtered_ruby, grouped_ruby[0])
        ruby = filtered_ruby
        if fmt == 'latex':
            filtered_str = r'\\ruby{%s}{%s}' % (base, ruby)
        elif fmt in ('html', 'html5', 'epub', 'epub3'):
            filtered_str = (r'<ruby><rb>%s</rb><rp>'
                            '《</rp><rt>%s</rt><rp>》'
                            '</rp></ruby>') % (base, ruby)
        filtered_val = regex.sub(r'%s' % matched_vals, r'%s' % filtered_str, filtered_val)
    for matched_vals in regex.findall(kenten_pattern, filtered_val):
        base = regex.search(r'《《(.+?)》》', matched_vals).groups(0)[0]
        if fmt == 'latex':
            filtered_str = r'\\kenten{%s}' % base
        elif fmt in ('html', 'html5', 'epub', 'epub3'):
            kenten = ''
            for kenten_count in base:
                kenten += r'・'
            filtered_str = (r'<ruby><rb>%s</rb><rp>'
                            '《</rp><rt>%s</rt><rp>》'
                            '</rp></ruby>') % (base, kenten)
        filtered_val = regex.sub(r'%s' % matched_vals, r'%s' % filtered_str, filtered_val)

    if fmt == 'latex':
        for matched_vals in regex.findall(r'…', filtered_val):
            filtered_val = regex.sub(r'%s' % matched_vals, r'…', filtered_val)
        for matched_vals in regex.findall(r'―', filtered_val):
            filtered_val = regex.sub(r'%s' % matched_vals, r'—', filtered_val)

    filtered_val = regex.sub(r'｜《', r'《', filtered_val)

    if 'matched_vals' in locals():
        if fmt == 'latex':
            return RawInline('latex', r'%s' %filtered_val)
        if fmt in ('html', 'html5', 'epub', 'epub3'):
            return RawInline('html', r'%s' %filtered_val)
    else:
        return Str(filtered_val)

if __name__ == '__main__':
    toJSONFilter(ruby_kenten)
