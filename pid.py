from time import time

class PID(object):
	"""docstring for PID"""
	def __init__(self, p, i, d, _min, _max, margin):
		super(PID, self).__init__()
		self.p = p
		self.i = i
		self.d = d
		self.min = _min
		self.max = _max
		self.margin = margin

		self.int_err = 0
		self.prev_err = 0
		self.prev_t = -1

		self.satHigh = False
		self.satLow = False
		
	def getAmount(self, err):
		if abs(err) < self.margin:
			return 0

		res = 0

		if self.prev_t == -1:
			self.prev_err = err
			self.prev_t = time()
			res = self.p*err
		else:
			dt = time()-self.prev_t
			if ((not self.satHigh) or (self.prev_err < 0)) or ((not self.satLow) or (self.prev_err > 0)):
				self.int_err += self.prev_err*dt
			
			der_err = (err-self.prev_err)/dt

			res = self.p*err + self.i*self.int_err + self.d*der_err

		print(res, err)

		if res > self.max:
			res = self.max
			self.satHigh = True
			self.satLow = False
		elif res < self.min:
			res = self.min
			self.satLow = True
			self.satHigh = False
		else:
			self.satLow = False
			self.satHigh = False

		return res