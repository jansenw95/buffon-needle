from manim import *
import math
import random


class SquareToCircle(Scene):
    def construct(self):
        paper_left = -4
        paper_right = 4

        intersect = 0
        total = 0
        pi_estimate = 0
        
        rep = 1000

        paper = Group()
        paper.shift([1,0,0])
        self.add(paper)
        title = Tex("this is a grid")
        self.add(title)
        for x in range(7):
            line = Line([paper_left,-3+x,0],[paper_right,-3+x,0]).set_color(WHITE)
            paper.add(line)
            # self.add(line)
        for x in range(rep):
            point_x = random.uniform(paper_left+1, paper_right-1)
            point_y = random.random()*5-2.5
            angle = random.random()*math.pi
            line = Line([point_x-math.cos(angle)*0.5, point_y-math.sin(angle)*0.5, 0], [point_x+math.cos(angle)*0.5, point_y+math.sin(angle)*0.5, 0])
            
            closest_dist = min(point_y-math.floor(point_y), math.ceil(point_y)-point_y)
            # print(closest_dist)
            if closest_dist <= math.sin(angle)*0.5:
                line.set_color(RED) 
                intersect += 1
            total += 1
            
            # paper.add(line)
            # self.add(line)
            # self.wait(0.1)
        self.wait(1)