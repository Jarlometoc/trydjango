import numpy as np
layer_lines = 3
res_high = 0.251
res_low = 0.0
R_step = 0.001
f = open("synthetic.dat", "w");
for layer_line in range(0,layer_lines,1):
	for q in np.arange(res_low,res_high,R_step):
		line = "10 %8.4f %4d\n" %(q,layer_line)
		f.write(line)
f.close() 	
