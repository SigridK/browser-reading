import pandas as pd

demo = pd.DataFrame.from_csv('alldemostimuli.txt', encoding = 'utf-8', sep='\t', header=None)
test = pd.DataFrame.from_csv('allteststimuli.txt', encoding = 'utf-8', sep='\t', header=None)

demo = demo.sort_index()
test = test.sort_index()

demo.to_csv('alldemostimulisorted.txt', encoding = 'utf-8', sep='\t', header=None)
test.to_csv('allteststimulisorted.txt', encoding = 'utf-8', sep='\t', header=None)