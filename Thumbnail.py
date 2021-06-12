from manim import *
import math
import random
import numpy as np

# set random seed for consistency 
random.seed(2)  

intersect = 0
total = 0
pi_estimate = 0

class Thumbnail(Scene):
    def construct(self):
        global intersect, total, pi_estimate
        paper_left = -1.5
        paper_right = 6.5
        paper_bottom = -3
        paper_top = 3
        num_paper_lines = 5 # >1

        # formula for calculating pi  only works if needle_len <= paper_spacing
        needle_len = (paper_top - paper_bottom)/(num_paper_lines - 1)
        paper_spacing = (paper_top - paper_bottom)/(num_paper_lines - 1)

        for x in reversed(range(num_paper_lines)):
            line = Line([paper_left, paper_bottom + paper_spacing*x, 0], 
                        [paper_right, paper_bottom + paper_spacing*x,0], stroke_width=6).set_color(WHITE)
            self.add(line)

        def draw_needles(num_needles, fade, time=0):
            global intersect, total, pi_estimate

            for _ in range(num_needles):
                # get random point that will be the center of the line, also keep line from sticking outside paper for aesthetics
                point_x = random.uniform(paper_left + needle_len/2, paper_right - needle_len/2)
                point_y = random.uniform(paper_bottom + needle_len/2, paper_top - needle_len/2)

                # calculate the closest distance between the point and a gridline
                closest_dist = min(point_y - (paper_bottom + paper_spacing*math.floor((point_y - paper_bottom)/paper_spacing)), 
                                   paper_bottom + paper_spacing*math.ceil((point_y - paper_bottom)/paper_spacing) - point_y)
                
                angle = random.random()*math.pi            
                needle = Line([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0], stroke_width=6)
                
                # check for intersection
                if closest_dist <= math.sin(angle)*needle_len/2:
                    needle.set_color(RED) 
            
                if fade:
                    self.play(FadeIn(needle, scale=0.66))
                else:
                    self.add(needle)
                
                if closest_dist <= math.sin(angle)*needle_len/2:
                    intersect += 1
                total += 1
                pi_estimate = 2*needle_len*total/intersect/paper_spacing if intersect else 0

                if num_needles == 1:
                    return ([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])
       
        draw_needles(50, False, 0)

        
        pi_formula = MathTex("\\pi = \\! ?").scale(3)
        pi_formula.move_to(4.25*LEFT)
        self.add(pi_formula)