from record_tello import detect_face

class Face(object):
	"""docstring for Face"""
	def __init__(self):
		super(Face, self).__init__()
		
		self.N = 3 #length of avg
		self.no_face_trigger = 20

		self.no_face_cnt = 0

		self.faces = [[], [], [], []] #len = avg + 1
		self.i = 0
		self.inited = False

		self.face_avg = []
		self.face_predict = []

	def update(self, frame):
		self.face_predict = self.get_face_predict()

		self.i = (self.i+1)%self.N
		self.faces[self.i] = detect_face(frame)

		self.face_avg = self.get_face_avg()

		if (not self.inited) and (self.i == 0):
			self.inited = True


	def get_face(self):
		return self.faces[self.i]

	def get_face_avg(self, shift=0):
		face_avg = [0, 0, 0, 0]
		N = 0

		for i in range(self.N):
			face = self.faces[ (self.i+shift-i)%self.N ]
			if len(face) == 1:
				face = face[0]
				N += 1
				for x in range(4):
					face_avg[x] += face[x]

		if N > 0:
			for x in range(4):
				face_avg[x] /= N
				face_avg[x] = int(face_avg[x])
			return [face_avg]
		else:
			return []

	def get_face_predict(self):
		prev_face_avg = self.get_face_avg(shift=-1)
		if len(prev_face_avg) == 0 or len(self.face_avg) == 0:
			self.no_face_cnt += 1
			if self.no_face_cnt < self.no_face_trigger:
				face_predict = self.face_predict[0][:]
				for x in range(4):
					face_predict[x] += int(self.face_predict[0][x] - prev_face_avg[0][x])
				return [face_predict]
			else:
				return []
		else:
			face_predict = [0, 0, 0, 0]
			for x in range(4):
				face_predict[x] = int(2*self.face_avg[0][x] - prev_face_avg[0][x])

			return [face_predict]












