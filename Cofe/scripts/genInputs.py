import os, sys
import os.path

from glob import glob

paths = glob(sys.argv[1] + '/*/')
paths = [p[:-1] for p in paths]

for p in paths:
	for dirpath, dirnames, filenames in os.walk(p):
		for filename in [f for f in filenames if f.endswith(".csv")]:
			dataset = open(os.path.join(dirpath, filename), "r")
			info = dirpath.split('/')
			
			newname = filename.split('.')[0] + "_LDA.txt"
			newnameBTM = filename.split('.')[0] + "_BTM.txt"

			lda = open(os.path.join(dirpath, newname), 'w')
			btm = open(os.path.join(dirpath, newnameBTM), 'w')

			num_lines = str(sum(1 for line in dataset))
			lda.write(num_lines + '\n')
			dataset.seek(0,0)

			for l in dataset:
				line = l.split(';')[2].strip()
				if len(line) == 0:
					raise Exception("Doc vazio: " + l)
				btm.write(line + '\n')
				lda.write(line + '\n')

			lda.close()
			btm.close()

