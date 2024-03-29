from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
	NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class Paddle(Widget):
	score = NumericProperty(0)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vel_x,vel_y = ball. velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vel_x, vel_y)
			velocity = bounced * 1.1
			ball.velocity = velocity.x, velocity.y + offset
			
class PongGame(Widget):
	ball = ObjectProperty(None)

	def serve_ball(self):
		self.ball.center = self.center
		self.ball.velocity = Vector(4,0)

	def update(self, dt):
		self.ball.move()
		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

		if self.ball.y < 0 or self.ball.top > self.height:
			self.ball.velocity_y *= -1

		if self.ball.x < 0:
			self.player2.score += 1
			self.serve_ball()
		if self.ball.right > self.width:
			self.player1.score += 1
			self.serve_ball()

	def on_touch_move(self, touch):
		if touch.x < self.width / 3:
			if touch.y <=  100: self.player1.center_y = 100
			elif touch.y >= self.height - 100: self.player1.center_y = self. height - 100
			else: self.player1.center_y = touch.y
		if touch.x > self.width * 2 / 3:
			if touch.y <=  100: self.player2.center_y = 100
			elif touch.y >= self.height - 100: self.player2.center_y = self. height - 100
			else: self.player2.center_y = touch.y

class Ball(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0/60.0)
		return game


if __name__ == '__main__':
    PongApp().run()
