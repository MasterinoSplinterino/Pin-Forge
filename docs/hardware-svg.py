# -*- coding: utf-8 -*-
"""Схема крепежа для README. Два файла, русский и английский.

Три колонки по 400 px, масштаб чертежа фурнитуры 14 px на миллиметр.
Подписи держатся внутри своей колонки, чтобы ничего не наезжало.
"""
import io, os

L = {
    'ru': {
        'file': 'docs/hardware.svg',
        't1': 'ИГЛА-БАБОЧКА',
        't2': 'КАК СИДИТ В ЗНАЧКЕ',
        't3': 'НЕОДИМОВЫЙ МАГНИТ',
        'cap': 'прижимная шайба',
        'pin': 'игла с пятаком',
        'body': 'значок',
        'socket': 'гнездо в спинке',
        'fabric': 'ткань',
        'clutch2': 'шайба',
        'mate': 'ответный магнит',
        'pocket': 'карман в спинке',
        'mm': 'мм',
        'n1a': 'Пятак вклеивается в гнездо на спинке.',
        'n1b': 'Игла проходит сквозь ткань, шайба держит с изнанки.',
        'n2a': 'Магнит вклеивается заподлицо, ответный с изнанки.',
        'n2b': 'Клеить только в паре: полярность выставится сама.',
    },
    'en': {
        'file': 'docs/hardware.en.svg',
        't1': 'BUTTERFLY CLUTCH PIN',
        't2': 'HOW IT SITS IN THE PIN',
        't3': 'NEODYMIUM MAGNET',
        'cap': 'clutch cap',
        'pin': 'needle with base disc',
        'body': 'pin body',
        'socket': 'socket in the back',
        'fabric': 'fabric',
        'clutch2': 'clutch',
        'mate': 'mating magnet',
        'pocket': 'pocket in the back',
        'mm': 'mm',
        'n1a': 'The disc is glued into the socket on the back.',
        'n1b': 'The needle goes through the fabric, the clutch holds it.',
        'n2a': 'The magnet is glued in flush, the mating one is inside.',
        'n2b': 'Glue it only as a pair: the polarity then sets itself.',
    },
}

STYLE = """
  .metal{fill:#c9ccd3;stroke:#6f747d;stroke-width:1.4}
  .body{fill:#e6e8ec;stroke:#6f747d;stroke-width:1.4}
  .relief{fill:#f4f6f9;stroke:#6f747d;stroke-width:1.2}
  .hole{fill:#8b9099;stroke:none}
  .dim{stroke:#c8643c;stroke-width:1;fill:none}
  .dimtick{stroke:#c8643c;stroke-width:1}
  .dimtxt{fill:#c8643c;font-size:12px;font-weight:600;
    font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
  .title{fill:#8d8d86;font-size:11px;font-weight:700;letter-spacing:1.4px;
    font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
  .lbl{fill:#8d8d86;font-size:11.5px;
    font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
  .note{fill:#8d8d86;font-size:11.5px;
    font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
  .fabric{stroke:#8d8d86;stroke-width:1.4;stroke-dasharray:6 5;fill:none}
  .lead{stroke:#b4b4ad;stroke-width:1;fill:none}
"""


def hdim(x1, x2, y, text, mm, above=False):
    ty = y - 9 if above else y + 17
    return (
        '<line class="dim" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<line class="dimtick" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<line class="dimtick" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<text class="dimtxt" x="%g" y="%g" text-anchor="middle">%s&#160;%s</text>'
    ) % (x1, y, x2, y, x1, y - 4, x1, y + 4, x2, y - 4, x2, y + 4,
         (x1 + x2) / 2.0, ty, text, mm)


def vdim(y1, y2, x, text, mm):
    my = (y1 + y2) / 2.0
    return (
        '<line class="dim" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<line class="dimtick" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<line class="dimtick" x1="%g" y1="%g" x2="%g" y2="%g"/>'
        '<text class="dimtxt" x="%g" y="%g" text-anchor="middle" '
        'transform="rotate(-90 %g %g)">%s&#160;%s</text>'
    ) % (x, y1, x, y2, x - 4, y1, x + 4, y1, x - 4, y2, x + 4, y2,
         x + 15, my, x + 15, my, text, mm)


def lead(x1, y1, x2, y2):
    return '<line class="lead" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x1, y1, x2, y2)


def txt(x, y, s, cls='lbl', anchor='start'):
    return '<text class="%s" x="%g" y="%g" text-anchor="%s">%s</text>' % (cls, x, y, anchor, s)


def build(t):
    p = []
    a = p.append

    # ===== колонка 1: фурнитура отдельно =====
    x0, cx = 40, 200
    a(txt(x0, 32, t['t1'], 'title'))

    capw = 11.5 * 14 / 2.0                       # половина Ø11.5
    a(hdim(cx - capw, cx + capw, 70, 'Ø11.5', t['mm'], above=True))
    a('<path class="metal" d="M %g 108 L %g 86 Q %g 79 %g 86 L %g 108 Z"/>'
      % (cx - capw, cx - capw + 7, cx, cx + capw - 7, cx + capw))
    a('<ellipse class="hole" cx="%g" cy="85" rx="5" ry="2.3"/>' % cx)
    a(txt(cx, 128, t['cap'], 'lbl', 'middle'))

    top, bot = 168, 294                          # 126 px = 9 мм
    a('<path class="metal" d="M %g %g L %g %g L %g %g Z"/>'
      % (cx, top, cx - 7, top + 18, cx + 7, top + 18))
    a('<rect class="metal" x="%g" y="%g" width="14" height="%g"/>'
      % (cx - 7, top + 17, bot - 12 - (top + 17)))
    a('<rect class="metal" x="%g" y="%g" width="140" height="12" rx="5"/>'
      % (cx - 70, bot - 12))
    a(vdim(top, bot, cx + 108, '9', t['mm']))
    a(hdim(cx - 70, cx + 70, bot + 26, 'Ø10', t['mm']))
    a(txt(cx, bot + 62, t['pin'], 'lbl', 'middle'))

    # ===== колонка 2: разрез со значком =====
    x1, bx = 440, 600
    a(txt(x1, 32, t['t2'], 'title'))
    a('<rect class="relief" x="%g" y="101" width="34" height="11" rx="3"/>' % (bx - 78))
    a('<rect class="relief" x="%g" y="101" width="58" height="11" rx="3"/>' % (bx - 26))
    a('<rect class="relief" x="%g" y="101" width="22" height="11" rx="3"/>' % (bx + 44))
    a('<rect class="body" x="%g" y="110" width="230" height="38" rx="9"/>' % (bx - 115))
    a('<rect class="metal" x="%g" y="137" width="90" height="11" rx="4"/>' % (bx - 45))
    a('<rect class="metal" x="%g" y="148" width="11" height="92" rx="2"/>' % (bx - 5.5))
    a('<path class="metal" d="M %g 240 L %g 254 L %g 240 Z"/>' % (bx - 5.5, bx, bx + 5.5))
    a('<line class="fabric" x1="%g" y1="178" x2="%g" y2="178"/>' % (bx - 150, bx - 12))
    a('<line class="fabric" x1="%g" y1="178" x2="%g" y2="178"/>' % (bx + 12, bx + 150))
    a('<path class="metal" d="M %g 208 L %g 186 Q %g 179 %g 186 L %g 208 Z"/>'
      % (bx - 68, bx - 61, bx, bx + 61, bx + 68))
    a(lead(bx - 118, 122, bx - 148, 122)); a(txt(bx - 153, 126, t['body'], 'lbl', 'end'))
    a(lead(bx - 48, 143, bx - 148, 143)); a(txt(bx - 153, 147, t['socket'], 'lbl', 'end'))
    a(lead(bx + 152, 178, bx + 172, 178)); a(txt(bx + 177, 182, t['fabric']))
    a(lead(bx + 70, 198, bx + 172, 198)); a(txt(bx + 177, 202, t['clutch2']))
    a(txt(x1, 300, t['n1a'], 'note'))
    a(txt(x1, 318, t['n1b'], 'note'))

    # ===== колонка 3: магнит =====
    x2, mx = 840, 1010
    a(txt(x2, 32, t['t3'], 'title'))
    a('<rect class="metal" x="%g" y="74" width="84" height="42" rx="3"/>' % (mx - 42))
    a(vdim(74, 116, mx + 58, '3', t['mm']))
    a(hdim(mx - 42, mx + 42, 140, 'Ø6', t['mm']))

    a('<rect class="relief" x="%g" y="191" width="44" height="11" rx="3"/>' % (mx - 60))
    a('<rect class="relief" x="%g" y="191" width="26" height="11" rx="3"/>' % (mx + 8))
    a('<rect class="body" x="%g" y="200" width="190" height="38" rx="9"/>' % (mx - 95))
    a('<rect class="metal" x="%g" y="222" width="56" height="16" rx="2"/>' % (mx - 28))
    a('<line class="fabric" x1="%g" y1="256" x2="%g" y2="256"/>' % (mx - 112, mx + 112))
    a('<rect class="metal" x="%g" y="264" width="56" height="16" rx="2"/>' % (mx - 28))
    a(lead(mx + 32, 230, mx + 116, 230)); a(txt(mx + 121, 234, t['pocket']))
    a(lead(mx + 32, 272, mx + 116, 272)); a(txt(mx + 121, 276, t['mate']))
    a(txt(x2, 320, t['n2a'], 'note'))
    a(txt(x2, 338, t['n2b'], 'note'))

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1290 370" '
            'width="1290" height="370" role="img">\n'
            '<style>%s</style>\n%s\n</svg>\n' % (STYLE, '\n'.join(p)))


for lang, t in L.items():
    path = t['file']
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(build(t))
    print('записан', path)
