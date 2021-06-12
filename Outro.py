from manim import *
import random
import math

# set random seed for consistency 
random.seed(3)  

intersect = 0
total = 0
pi_estimate = 0

class Outro(Scene):
    def construct(self):
        global intersect, total, pi_estimate

        dashed_line = DashedLine(8*LEFT, 8*RIGHT)

        _3b1b = Tex("Inspired by 3blue1brown").scale(2)
        made = Tex("Made by Bradley He and Jansen Wong").scale(1.5)
        thanks = Tex("Thanks for \\\ watching!", color="yellow").scale(2)

        _3b1b.move_to(2.75*UP)
        made.move_to(1.25*UP)
        thanks.move_to(2*DOWN + 4*LEFT)

        self.add(dashed_line, _3b1b, made, thanks)

        paper_left = 2.5
        paper_right = 6.5
        paper_bottom = -3
        paper_top = -1
        num_paper_lines = 3 # >1

        # formula for calculating pi  only works if needle_len <= paper_spacing
        needle_len = (paper_top - paper_bottom)/(num_paper_lines - 1)/2
        paper_spacing = (paper_top - paper_bottom)/(num_paper_lines - 1)

        pi_num = DecimalNumber(0,
                                num_decimal_places=3,
                                include_sign=False,
                                unit=None,
                                show_ellipsis=True
                                )
        pi_num.add_updater(lambda d: d.set_value(pi_estimate))


        for x in reversed(range(num_paper_lines)):
            line = Line([paper_left, paper_bottom + paper_spacing*x, 0], 
                        [paper_right, paper_bottom + paper_spacing*x,0]).set_color(WHITE)
            self.add(line) 

        def draw_needles(num_needles, fade, time=0):
            global intersect, total, pi_estimate

            for _ in range(num_needles):
                # get random point that will be the center of the line, also keep line from sticking outside paper for aesthetics
                point_x = random.uniform(paper_left + needle_len/2, paper_right - needle_len/2)
                point_y = random.uniform(paper_bottom, paper_top)

                # calculate the closest distance between the point and a gridline
                closest_dist = min(point_y - (paper_bottom + paper_spacing*math.floor((point_y - paper_bottom)/paper_spacing)), 
                                   paper_bottom + paper_spacing*math.ceil((point_y - paper_bottom)/paper_spacing) - point_y)
                
                angle = random.random()*math.pi            
                needle = Line([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])
                
                # check for intersection
                if closest_dist <= math.sin(angle)*needle_len/2:
                    needle.set_color(RED) 
            
                if fade:
                    self.play(FadeIn(needle, scale=0.66))
                else:
                    self.add(needle)
                    self.wait(time)
                
                if closest_dist <= math.sin(angle)*needle_len/2:
                    intersect += 1
                total += 1
                pi_estimate = 2*needle_len*total/intersect/paper_spacing if intersect else 0

                if num_needles == 1:
                    return ([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])

        pi_var = MathTex("\\pi \\approx")
        pi_var.move_to(0.25*LEFT + 2*DOWN)
        pi_num.move_to(1.25*RIGHT + 2*DOWN)
        self.add(pi_var, pi_num)

        self.play(AnimationGroup(*[FadeIn(x) for x in self.get_top_level_mobjects()], lag_ratio=0))
        draw_needles(200, False, 0.05)
        self.wait(1)
        
        print(pi_estimate)