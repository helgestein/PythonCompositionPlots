import matplotlib.cm as cm
import numpy
import pylab
import operator, copy, os

#os.chdir('C:/Users/Gregoire/Documents/PythonCode/ternaryplot')
from myternaryutility import TernaryPlot

class ternaryfaces_folded:
    def __init__(self, ax, ellabels=['A', 'B', 'C', 'D'], offset=0.2, nintervals=10.):
        self.nint=1.*nintervals
        self.delta=1./self.nint
        self.ternaryplot=TernaryPlot(ax, outline=False)
        self.ax=ax
        self.offset=offset
        #self.ax.set_xlim(-.1, 2.6)
        #self.ax.set_ylim(-.1, 3.**.5/2+.1)
        self.ax.set_ylim(-.1-3.**.5/4., .1+3.**.5/4.)
        self.cartendpts=numpy.float32([[0, 0], [.5, numpy.sqrt(3.)/2.], [1, 0]])
        self.ellabels=ellabels
        self.scalefcn=lambda ntern:(self.nint-ntern)/self.nint
        shift=0.
        self.shift_ntern=[]
        perminds=[0, 1, 2]
        self.perminds_ntern=[]
        for ntern in range(int(self.nint)+1):
            self.shift_ntern+=[shift]
            shift+=self.delta*1.5+0.5*self.scalefcn(ntern)
            self.perminds_ntern+=[perminds]
            #if ntern%2==0:
            perminds=[perminds[i] for i in [1, 2, 0]]
#            else:
#                perminds=[perminds[i] for i in [1, 0, 2]]
            
        self.ax.set_xlim(-.1, shift+self.delta*1.5+1.*self.scalefcn(ntern)+.1)
        
        self.s=numpy.diff(ax.transData.transform([0., self.delta]))[0]
        self.outline()
    
    def xy_ntern(self, x, y, ntern):
        if ntern%2==1:
            y=-1.*y+3.**.5/2
        y-=3.**.5/2/2.
        y*=self.scalefcn(ntern)
        x*=self.scalefcn(ntern)
        x+=self.shift_ntern[ntern]
        return x, y
        
    def outline(self):
        for ntern in range(int(self.nint)):
            for i, ep in enumerate(self.cartendpts):
                for ep2 in self.cartendpts[i+1:]:
                    x, y=self.xy_ntern(numpy.array([ep[0], ep2[0]]), numpy.array([ep[1], ep2[1]]), ntern)
                    self.ax.plot(x, y, 'k-')
        
    def label(self, **kwargs):#takeabs is to avoid a negative sign for ~0 negative compositions
        for count, (va, y) in enumerate(zip(['bottom','top'], [-3.**.5/4.-self.offset, 3.**.5/4.+self.offset])):
            self.ax.text(count*.5, y, self.ellabels[count], ha='center', va=va, **kwargs)
        for i in range(0, int(self.nint)):
            y=(3.**.5/4.)*self.scalefcn(i)+self.offset
            if i%2==1:
                va='top'
            else:
                va='bottom'
                y*=-1
            x=self.shift_ntern[i+1]+.5*self.scalefcn(i+1)
            self.ax.text(x, y, self.ellabels[(i+2)%3], ha='center', va=va, **kwargs)
            
    def toCart(self, quatcomps, ntern):
        qc=numpy.array(quatcomps)
        perminds=self.perminds_ntern[ntern]
        x, y=self.ternaryplot.toCart(qc[:, perminds])
        x, y=self.xy_ntern(x, y, ntern)
        return x, y
    
    def scatter(self, quatcomps, c,  s=None, **kwargs):
        if s is None:
            s=self.s
        quatcomps=numpy.int32(numpy.round(quatcomps*self.nint))
        for ntern in range(int(self.nint)):
            ba=quatcomps[:, -1]==ntern
            self.shellcomps=quatcomps[ba]
            shellc=c[ba]
            self.shellcomps=self.shellcomps[:, :-1]/(self.nint-ntern)
            x, y=self.toCart(self.shellcomps, ntern)
            self.ax.scatter(x, y, c=shellc, **kwargs)
        ba=quatcomps[:, -1]==self.nint
        if True in ba:
            self.shellcomps=quatcomps[ba]#only 1 comp but might be duplicated
            shellc=c[ba]
            for cv in shellc:
                self.ax.scatter(self.shift_ntern[-1], 0, c=cv, **kwargs)
#            if ntern==0:
#                break