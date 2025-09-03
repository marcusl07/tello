from record_tello import detect_face

class Face(object):
	"""docstring for Face"""
	def __init__(self):
		super(Face, self).__init__()
		
		self.N = 3 #length of avg

		self.faces = [[], [], [], []] #len = avg + 1
		self.i = 0
		self.inited = False

		self.face_avg = []
		self.face_predict = []

	def update(self, frame):
		self.face_predict = get_face_predict()

		self.i = (self.i+1)%self.N
		self.faces[self.i] = detect_face(frame)

		self.face_avg = get_face_avg()

		if (not self.inited) and (self.i == 0):
			self.inited = True


	def get_face(self):
		return self.faces[self.i]

	def get_face_avg(self, shift=0):
		face_avg = [0, 0, 0, 0]
		N = 0

		for i in range(self.N):
			face = faces[ (self.i+shift-i)%N ]
			if len(face) == 1:
				face = face[0]
				N += 1
				for x in range(4):
					face_avg[x] += face[x]

		if N > 0:
			for x in range(4):
				face_avg[x] /= N
			return face_avg
		else:
			return []

	def get_face_predict(self):
		prev_face_avg = get_face_avg(shift=-1)
		if len(prev_face_avg) == 0 or len(self.face_avg) == 0:
			return []
		else:
			face_predict = [0, 0, 0, 0]
			for x in range(4):
				face_predict[x] = 2*self.face_avg[x] - prev_face_avg[x]

			return face_predict












