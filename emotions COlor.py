class Emotions(object):
    def __init__(self, emotion, color):
        self.emotion = emotion
        self.draw  = draw
        self.color = color
        
    def changeColor(self):
        if self.emotion == "angry":
            self.color = [0,0,250] #red
        if self.emotion == "sad":
            self.color = [250,0,0] #blue
        if self.emotion == "happy":
            self.color = [0,250,0] #yellow
            