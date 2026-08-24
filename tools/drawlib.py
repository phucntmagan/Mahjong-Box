"""Helper ve SVG dung chung cho cac script hinh (dung tu draw_hinge.py tro di)."""
import math

class V:
    """He toa do 2D: (ox,oz) la diem (0,0); s = px/mm; z huong len."""
    def __init__(self, ox, oz, s): self.ox, self.oz, self.s = ox, oz, s
    def X(self, v): return self.ox + v*self.s
    def Z(self, v): return self.oz - v*self.s
    def P(self, p): return (self.X(p[0]), self.Z(p[1]))
    def rect(self, x0,x1,z0,z1, fill, st='#2a241c', sw=0.9, extra=''):
        return (f'<rect x="{self.X(x0):.1f}" y="{self.Z(z1):.1f}" width="{(x1-x0)*self.s:.1f}" '
                f'height="{(z1-z0)*self.s:.1f}" fill="{fill}" stroke="{st}" stroke-width="{sw}" {extra}/>')
    def poly(self, pts, fill, st='#2a241c', sw=0.9, extra=''):
        d=' '.join(f'{self.X(a):.1f},{self.Z(b):.1f}' for a,b in pts)
        return (f'<polygon points="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" '
                f'stroke-linejoin="round" {extra}/>')
    def circ(self, c, r, fill, st='#2a241c', sw=0.9):
        return (f'<circle cx="{self.X(c[0]):.1f}" cy="{self.Z(c[1]):.1f}" r="{r*self.s:.1f}" '
                f'fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
    def path(self, pts, st, sw=1.2, dash=None, fill='none'):
        d='M '+' L '.join(f'{self.X(a):.1f},{self.Z(b):.1f}' for a,b in pts)
        da=f' stroke-dasharray="{dash}"' if dash else ''
        return f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}"{da}/>'
    def dim(self, x0,x1,z, label, dy=0, col='#55524b', fs=9.5):
        a,b,y=self.X(x0),self.X(x1),self.Z(z)+dy
        return (f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{a:.1f}" y1="{y-3:.1f}" x2="{a:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<line x1="{b:.1f}" y1="{y-3:.1f}" x2="{b:.1f}" y2="{y+3:.1f}" stroke="{col}" stroke-width="0.8"/>'
                f'<text x="{(a+b)/2:.1f}" y="{y-4:.1f}" text-anchor="middle" font-size="{fs}" fill="{col}">{label}</text>')

def arrow(x1,y1,x2,y2,col,w=2.0,head=6):
    a=math.atan2(y2-y1,x2-x1)
    p=[(x2-head*math.cos(a-0.42), y2-head*math.sin(a-0.42)),
       (x2-head*math.cos(a+0.42), y2-head*math.sin(a+0.42))]
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round"/><polygon points="{x2:.1f},{y2:.1f} '
            f'{p[0][0]:.1f},{p[0][1]:.1f} {p[1][0]:.1f},{p[1][1]:.1f}" fill="{col}"/>')
def svg(w,h,body): return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
    f'viewBox="0 0 {w} {h}" font-family="DejaVu Sans" font-size="11.5">'
    f'<rect width="100%" height="100%" fill="#faf9f6"/>{body}</svg>')
def T(x,y,t,**k):
    a=' '.join(f'{kk.replace("_","-")}="{v}"' for kk,v in k.items())
    return f'<text x="{x}" y="{y}" {a}>{t}</text>'
def lead(x,y,px,py,anchor):
    dx = -8 if anchor=='end' else 8
    return (f'<polyline points="{x+dx},{y-4} {(x+dx+px)/2},{y-4} {px},{py}" fill="none" '
            f'stroke="#6b6862" stroke-width="0.9"/><circle cx="{px}" cy="{py}" r="2.2" fill="#6b6862"/>')
def annot(items, mid=470):
    o=[]
    for x,y,px,py,txt in items:
        a='end' if x>mid else 'start'
        o.append(lead(x,y,px,py,a)); o.append(T(x,y,txt,text_anchor=a))
    return ''.join(o)
def panel(x,y,w,h,label):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#b8b5ae" '
            f'stroke-width="1" stroke-dasharray="5,4"/>'
            f'<text x="{x+6}" y="{y+15}" font-size="11" font-weight="bold" fill="#55524b">{label}</text>')
def hdr(t,s1,s2=''):
    return (T(28,32,t,font_size=15.5,font_weight='bold')+T(28,52,s1,fill='#55524b')
            +(T(28,68,s2,fill='#55524b') if s2 else ''))
