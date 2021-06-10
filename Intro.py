from manim import *

class Intro(Scene):
	def construct(self):
		pi = MathTex("\\pi").scale(3).move_to([0, 0, 0])
		self.play(Write(pi))
		self.wait(1)

		circle = Circle(radius=1, stroke_width=2, fill_opacity=1)
		poly = RegularPolygon(n=4, height=2, stroke_width=2, fill_opacity=1)
		circle.move_to(4*LEFT + 2*UP)
		poly.move_to(circle)
		shapes = VGroup()
		shapes.add(circle, poly)

		self.play(Write(shapes))
		self.wait(1)

		machin = MathTex("\\frac{\\pi}{4}=4\\arctan\\frac{1}{5}-\\arctan\\frac{1}{239}").scale(0.8)
		machin.move_to(4*RIGHT + 2*UP)

		chudnovsky = MathTex("\\frac{1}{\\pi}=12\\sum_{k=0}^{\\infty}\\frac{(-1)^k(6k)!(13591409+545140134k)}{(3k!)(k!)^3 640320^{3k+3/2}}").scale(0.6)
		chudnovsky.move_to(3.5*LEFT + 2*DOWN)
		
		for i in range(6, 12, 2):
			if i == 8:
				self.play(Write(machin))
			if i == 10:
				self.play(Write(chudnovsky)) 
			self.play(Transform(poly, RegularPolygon(n=i, height=2, stroke_width=2, fill_opacity=1).move_to(circle)))
			self.wait(1)

		self.play(Write(Tex("\"Buffon's needle problem\"").move_to(4*RIGHT + 2*DOWN).scale(0.8)))

		self.wait(1)