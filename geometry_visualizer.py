#========================= AUTHOR (of class Shape only) :- IIITD-IP course Faculty   ===================
#-------------------------------------------------------------------------------------------------------
#=================================    AUTHOR :-  PRERAK SEMWAL     =====================================

import numpy as np
import matplotlib.pyplot as plt

class Shape:
    def __init__(self):
        self.T_s = None
        self.T_r = None
        self.T_t = None

    def translate(self, dx, dy):
        self.T_t = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

    def scale(self, sx, sy):
        self.T_s = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])

    def rotate(self, deg):
        rad = deg * (np.pi / 180)
        self.T_r = np.array([[np.cos(rad), np.sin(rad), 0], [-np.sin(rad), np.cos(rad), 0], [0, 0, 1]])

    def plot(self, x_dim, y_dim):
        x_dim, y_dim = 1.2 * x_dim, 1.2 * y_dim
        plt.plot((-x_dim, x_dim), [0, 0], 'k-')
        plt.plot([0, 0], (-y_dim, y_dim), 'k-')
        plt.xlim(-x_dim, x_dim)
        plt.ylim(-y_dim, y_dim)
        plt.grid()
        plt.show()


#################################################################################### 

class Polygon(Shape):

    def __init__(self, A):                                          
        super().__init__()       # self have T_t,T_s,T_r
        self.A = A.T
        self.n = (self.A).shape[1]
        self.plot_no=1
        
    def __str__(self):
        print(f"A = {self.A} ")


    def translate(self, dx, dy=None):                                    
        if dy==None:
            dy=dx
        super().translate(dx,dy)     # inititalise   self.T_t
        self.A = self.multiply(self.T_t,self.A)   # calls static method multiply

        m =np.zeros( (3, self.n ) )    # initializes a zero matrix of appropriate dimensions
        for i in range(3):
            for j in range(self.n):
                m[i][j] = round(self.A[i][j] ,2)
        
        return ( m[0] , m[1] )



    def scale(self, sx, sy=None):                                 
        if sy==None:
            sy=sx
        self.axis_sum = (self.A).sum(axis=1)
        self.centre_x= float(self.axis_sum[0])/self.n 
        self.centre_y= float(self.axis_sum[1])/self.n 

        for i in range(self.n):
            self.A[0][i] -= self.centre_x        # make apparent origin to centre
        for i in range(self.n):
            self.A[1][i] -= self.centre_y

        super().scale(sx,sy)               # assigns T_s
        self.A = self.multiply(self.T_s , self.A)


        for i in range(self.n):
            self.A[0][i] += self.centre_x       # undo the coordinate changes
        for i in range(self.n):
            self.A[1][i] += self.centre_y   

        m =np.zeros( (3, self.n ) )
        for i in range(3):
            for j in range(self.n):
                m[i][j] = round(self.A[i][j] ,2)
        
        return ( m[0] , m[1] )



    def rotate(self, deg, rx=0, ry=0):           

        super().rotate(deg)  # assign T_r
        for i in range(self.n):
            self.A[0][i] -= rx        # make apparent origin to centre
        for i in range(self.n):
            self.A[1][i] -= ry

        self.A = self.multiply(self.T_r , self.A)                 

        for i in range(self.n):
            self.A[0][i] += rx       # undo the coordinate changes
        for i in range(self.n):
            self.A[1][i] += ry 

        m =np.zeros( (3, self.n ) )
        for i in range(3):
            for j in range(self.n):
                m[i][j] = round(self.A[i][j] ,2)
        
        return ( m[0] , m[1] )
 
  

    def plot(self):

        x_ = list(self.A[0])
        y_ = list(self.A[1])
        x_.append(x_[0])
        y_.append(y_[0])
        x_max = sorted(x_)
        x_max = max(x_max[-1],abs(x_max[0]))      # find the max. magnitude for abscissa
        y_max = sorted(y_)
        y_max = max(y_max[-1],abs(y_max[0]))      # find the max. magnitude for ordinate

        
        if self.plot_no==0:                     # plot dotted also
            x__ = list(polygon_object_.A[0])
            y__ = list(polygon_object_.A[1])
            x__.append(x__[0])
            y__.append(y__[0])
            x__max = sorted(x__)
            x__max = max(x__max[-1],abs(x__max[0]))
            y__max = sorted(y__)
            y__max = max(y__max[-1],abs(y__max[0]))
            plt.plot(x__, y__ , linestyle="--", color="black",linewidth=1)
            plt.plot(x_ , y_ , linestyle="-", color="red",linewidth=2)
            if x_max<x__max:
                x_max=x__max
            if y_max<y__max:
                y_max=y__max
            super().plot(x_max,y_max)
        else:
            plt.plot(x_,y_ , color="black")
            super().plot(x_max,y_max)  




    @staticmethod
    def multiply(a,b):
        ans=[]
        B = b.T
        N= B.shape[0]
        for i in range(3):
            for j in range(N):      
                ans.append(sum(a[i]*B[j]))


        return (np.array(ans)).reshape(3,N)

####################################################################################

class Circle(Shape):

    def __init__(self, x=0, y=0, radius=5):                           

        super().__init__()             # gives T_t,t_s,T_r
        self.plot_no=1
        self.x=x
        self.y=y
        self.radius=radius
        self.A=np.array([ [self.x],
                          [self.y],
                          [1] ]) 

    def __str__(self):
        print(f"x= {self.x} , y= {self.y} , radius= {self.radius}")


    def translate(self, dx, dy=None):                             
        if dy==None:
            dy=dx
        super().translate(dx,dy)             # inititalise T_t
        self.A = self.multiply(self.T_t,self.A)

        return ( round(float(self.A[0]) , 2) , round(float(self.A[1]) , 2) , round(self.radius ,2) ) 


        

    def scale(self, sx):                                     

        self.radius = self.radius*sx 
        return ( round(float(self.A[0]) , 2) , round(float(self.A[1]) , 2) , round(self.radius , 2) ) 



    def rotate(self, deg, rx=0, ry=0):                    

        super().rotate(deg)                       # assign T_r
        self.A[0][0] -= rx                        # we change cordinates w.r.t rx,ry
        self.A[1][0] -= ry                                            
        self.A = self.multiply(self.T_r , self.A)
        self.A[0][0] += rx                        # we undo changes
        self.A[1][0] += ry
        return ( round(float(self.A[0]) , 2) , round(float(self.A[1]) , 2) , round(self.radius , 2) )


    def plot(self):

        
        if self.plot_no==0:           # plot dotted also
            circle_ = plt.Circle( (circle_object_.x,circle_object_.y), radius=circle_object_.radius ,color="black" , fc="white", linestyle="--",linewidth=1, fill=False)
            circle = plt.Circle(  (self.x,self.y), radius=self.radius ,color="red" , fc="white", linestyle="-",linewidth=2 , fill= False)#alpha=0.3
            fig, ax = plt.subplots()
            ax.add_patch(circle_)
            ax.add_patch(circle)
            ax.set_aspect(1)
            super().plot(max(self.x + self.radius,circle_object_.x + circle_object_.radius),max(self.y + self.radius,circle_object_.y + circle_object_.radius))
        else:
            circle = plt.Circle( (self.x,self.y), radius=self.radius ,color="black" , fc="white", linestyle="-",linewidth=2)
            fig, ax = plt.subplots()
            ax.add_patch(circle)
            ax.set_aspect(1)
            super().plot(self.x + 2*self.radius ,self.y + 2*self.radius )   # we send the arguments so that entire plot is visible on grid


    @staticmethod
    def multiply(a,b):
        ans=[]
        B = b.T
        N= B.shape[0]
        for i in range(3):
            for j in range(N):
                ans.append(sum(a[i]*B[j]))

        return (np.array(ans)).reshape(3,N)     # reshape would take care of appropiate dimension




####################################################################################

if __name__ == "__main__":

    verbose=int(input("verbose? 1 to plot, 0 otherwise: ")) 
    test_cases=int(input("Enter the number of test cases: "))
    while test_cases:
        test_cases-=1
        type=int(input("Enter type of shape (0: Polygon / 1:Circle):  "))
        
        if type==0:    # polygon entry
            sides=int(input("Enter number of sides:  "))
            l=[]
            for i in range(sides):
                x,y= list(map(float,input(f"enter x{i+1} , y{i+1} :  ").split()))
                l.append( [x,y,1] )

            A = np.array(l)
            polygon_object = Polygon(A)      #object of polygon class

            queries=int(input("Enter number of queries: "))
            print("""Enter the query of your choice in the following format 

1) R deg (rx) (ry)
2) T dx (dy)
3) S sx (sy)
4) P\n""")
            while queries:
                queries -=1
                choice = input().split()
                

                if choice[0]=='R':
                    deg=float(choice[1])
                    try:
                        rx= float(choice[2])
                    except:
                        rx=0
                    try:
                        ry=float(choice[3])
                    except:
                        ry=0
                    l_ = list(polygon_object.A[0]) + list(polygon_object.A[1])                    
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_)                    
                    if verbose==1:
                        mp = np.array((polygon_object.A).T)
                        polygon_object_ = Polygon(mp)                   # this is done to prevent aliasing of objects
                        t = polygon_object.rotate(deg,rx,ry)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)
                        polygon_object.plot_no= 0                    # tells python to plot state before change also
                        polygon_object.plot()
                    else:
                        t = polygon_object.rotate(deg,rx,ry)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)


                if choice[0]=='T':
                    dx = float(choice[1])
                    try:
                        dy = float(choice[2])
                    except:
                        dy=None
                    l_ = list(polygon_object.A[0]) + list(polygon_object.A[1])                    
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_)                    
                    if verbose==1:
                        mp = np.array((polygon_object.A).T)
                        polygon_object_ = Polygon(mp)                        # this is done to prevent aliasing of objects
                        t = polygon_object.translate(dx,dy)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)
                        polygon_object.plot_no=0                # tells python to plot state before change also
                        polygon_object.plot()
                    else:
                        t = polygon_object.translate(dx,dy)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)


                if choice[0]=='S':
                    sx=float(choice[1])
                    try:
                        sy=float(choice[2])
                    except:
                        sy= None
                    l_ = list(polygon_object.A[0]) + list(polygon_object.A[1])
                    
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_)                    
                    if verbose==1:
                        mp = np.array((polygon_object.A).T)
                        polygon_object_ = Polygon(mp)                  # this is done to prevent aliasing of objects
                        t = polygon_object.scale(sx,sy)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)
                        polygon_object.plot_no=0             # tells python to plot state before change also
                        polygon_object.plot()
                    else:
                        t = polygon_object.scale(sx,sy)
                        l = list(t[0]) + list(t[1])  # concatenate two np arrays
                        print(*l)


                if choice[0]=='P':
                    polygon_object.plot_no=1
                    polygon_object.plot()






        else:   # circle entry

            x0,y0,r0=list(map(float,input("enter space-separated center's abscissa, center's ordinate and circle's radius").split()))
            circle_object= Circle(x0,y0,r0)
            queries=int(input("Enter number of queries: "))
            print("""Enter the query of your choice in the following format 

1) R deg (rx) (ry)
2) T dx (dy)
3) S sx (sy)
4) P\n""")
            while queries:
                queries -=1
                choice = input().split()


                if choice[0]=='R':
                    deg = float(choice[1])
                    try:
                        rx = float(choice[2])
                    except:
                        rx=0
                    try:
                        ry= float(choice[3])
                    except:
                        ry=0
                    l_ = list(circle_object.A[0]) + list(circle_object.A[1])
                    l_.append(circle_object.radius)    
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_)                    
                    if verbose==1:
                        circle_object_ = Circle()
                        circle_object_.x = circle_object.x               # this is done to prevent aliasing of objects
                        circle_object_.y = circle_object.y
                        circle_object_.radius = circle_object.radius 
                        t = circle_object.rotate(deg,rx,ry)
                        circle_object.x=circle_object.A[0]
                        circle_object.y=circle_object.A[1]
                        print(*list(t))
                        circle_object.plot_no=0                    # tells python to plot state before change also
                        circle_object.plot()                        
                    else:
                        t = circle_object.rotate(deg,rx,ry)
                        print(*list(t))



                if choice[0]=='T':          
                    dx = float(choice[1])
                    try:
                        dy = float(choice[2])
                    except:
                        dy=None
                    l_ = list(circle_object.A[0]) + list(circle_object.A[1]) 
                    l_.append(circle_object.radius)
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_)                    
                    if verbose==1:
                        circle_object_ = Circle()
                        circle_object_.x = circle_object.x              # this is done to prevent aliasing of objects
                        circle_object_.y = circle_object.y
                        circle_object_.radius = circle_object.radius
                        t = circle_object.translate(dx,dy)
                        circle_object.x=circle_object.A[0]
                        circle_object.y=circle_object.A[1]
                        print(*list(t))
                        circle_object.plot_no=0                        # tells python to plot state before change also
                        circle_object.plot()
                    
                    else:
                        t = circle_object.translate(dx,dy)
                        print(*list(t))



                if choice[0]=='S':
                    sx = float(choice[1])
                    l_ = list(circle_object.A[0]) + list(circle_object.A[1]) 
                    l_.append(circle_object.radius)                    
                    for i in range(len(l_)):
                        l_[i]= round(l_[i],2)
                    print(*l_) 
                    if verbose==1:
                        circle_object_ = Circle()
                        circle_object_.x = circle_object.x                # this is done to prevent aliasing of objects
                        circle_object_.y = circle_object.y
                        circle_object_.radius = circle_object.radius                        
                        t = circle_object.scale(sx)
                        print(*list(t))
                        circle_object.plot_no=0                          # tells python to plot state before change also
                        circle_object.plot()
                    else:
                        t = circle_object.scale(sx)
                        print(*list(t))



                if choice[0]=='P':
                    circle_object.plot_no=1
                    circle_object.plot()
