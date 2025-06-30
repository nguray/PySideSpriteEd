
from rint import RInt
from selectcorner import SelectCorner

class SelectRect:


    def __init__(self) -> None:

        self._left = RInt(0)
        self._top = RInt(0)
        self._right = RInt(0)
        self._bottom = RInt(0)
        self.TopLeft = SelectCorner()
        self.TopRight = SelectCorner()
        self.BottomLeft = SelectCorner()
        self.BottomRight = SelectCorner()
        self.left_bak = RInt(0)
        self.top_bak = RInt(0)
        self.right_bak = RInt(0)
        self.bottom_bak = RInt(0)

        self.TopLeft.x = self._left
        self.TopLeft.y = self._top
        self.TopRight.x = self._right
        self.TopRight.y = self._top
        self.BottomLeft.x = self._left
        self.BottomLeft.y = self._bottom
        self.BottomRight.x = self._right
        self.BottomRight.y = self._bottom

    def setTopLeft(self,x: int,y: int):
        self.TopLeft.x.val = x
        self.TopLeft.y.val = y
    
    def getTopLeft(self):
        return self.TopLeft.x.val,self.TopLeft.y.val

    def setTopRight(self,x: int,y: int):
        self.TopRight.x.val = x
        self.TopRight.y.val = y

    def getTopRight(self):
        return self.TopRight.x.val,self.TopRight.y.val

    def setBottomRight(self,x: int,y: int):
        self.BottomRight.x.val = x
        self.BottomRight.y.val = y

    def getBottomRight(self):
        return self.BottomRight.x.val,self.BottomRight.y.val

    def setBottomLeft(self,x: int,y: int):
        self.BottomLeft.x.val = x
        self.BottomLeft.y.val = y

    def getBottomLeft(self):
        return self.BottomLeft.x.val,self.BottomLeft.y.val

    def isEmpty(self):
        return ((self._left.val == self._right.val) and (self._top.val == self._bottom.val))
    
    def getNormalize(self):
        l = self._left.val
        t = self._top.val
        r = self._right.val
        b = self._bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        return l,t,r,b
    
    def normalize(self):
        l = self._left.val
        t = self._top.val
        r = self._right.val
        b = self._bottom.val
        if l>r:
            l,r = r,l
        if t>b:
            t,b = b,t
        self._left.val = l
        self._top.val = t
        self._right.val = r
        self._bottom.val = b

    def contains(self, x, y):
        if (x >= self._left.val) and (x <= self._right.val) and \
            (y >= self._top.val) and (y <= self._bottom.val):
            return True
        return False
    
    def backup(self):
        self.left_bak.val   = self._left.val
        self.top_bak.val    = self._top.val
        self.right_bak.val  = self._right.val
        self.bottom_bak.val = self._bottom.val

    def restore(self):
        self._left.val   = self.left_bak.val
        self._top.val    = self.top_bak.val
        self._right.val  = self.right_bak.val
        self._bottom.val = self.bottom_bak.val

    def offset(self,dx: int,dy: int):
        self._left.val += dx
        self._right.val += dx
        self._top.val += dy
        self._bottom.val += dy

    def width(self):
        if (self._right.val > self._left.val):
            return self._right.val - self._left.val
        else:
            return self._left.val - self._right.val

    def height(self):
        if (self._bottom.val > self._top.val):
            return self._bottom.val - self._top.val
        else:
            return self._top.val - self._bottom.val

    @property
    def left(self):
        return self._left.val
    
    @left.setter
    def left(self, val):
        if isinstance(val, int):
            self._left.val = val
        else:
            return
        
    @property
    def top(self):
        return self._top.val
    
    @top.setter
    def top(self, val):
        if isinstance(val, int):
            self._top.val = val
        else:
            return

    @property
    def right(self):
        return self._right.val
    
    @right.setter
    def right(self, val):
        if isinstance(val, int):
            self._right.val = val
        else:
            return

    @property
    def bottom(self):
        return self._bottom.val
    
    @bottom.setter
    def bottom(self, val):
        if isinstance(val, int):
            self._bottom.val = val
        else:
            return
