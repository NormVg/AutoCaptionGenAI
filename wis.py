import whisper
import json

#model = whisper.load_model("base")
#result = model.transcribe("main.mp3")
#print(result)

#f = open("data.json","w")
#json_object = json.dumps(result, indent=3)
#f.write(json_object)
#f.close()

fr = open("data.json","r")
result = json.loads(fr.read())
fr.close()


b = [ [x['text'],x['start'],x['end'] ] for x in result['segments']]

from pprint import pprint

pprint(b)


fw = open("main.json","w")
fw.write(json.dumps(b))
fw.close()
