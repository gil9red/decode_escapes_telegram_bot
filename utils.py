#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import html
import re


# SOURCE: html
_charref = re.compile(
    r'&(#[0-9]+;?'
    r'|#[xX][0-9a-fA-F]+;?'
    r'|[^\t\n\f <&#;]{1,32};?)'
)


def decode(text: str) -> str:
    def _unescape(m: re.Match) -> str:
        return '<b><u>' + html.unescape(m.group()) + '</u></b>'

    text = html.escape(text, quote=False)
    text = text.replace('&amp;', '&')  # Return '&'
    text = _charref.sub(_unescape, text)
    return text


if __name__ == '__main__':
    text = decode('&#x20AC; &#8364; &euro;')
    print(text)
    assert text == '<b><u>€</u></b> <b><u>€</u></b> <b><u>€</u></b>'

    text = decode('"Hello" "World"!')
    print(text)
    assert text == '"Hello" "World"!'
