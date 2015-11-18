#This function makes a default experimental layerlines for input into Rosetta
#note that its dependent on resH and resL
def makeDefExp(name, res_high, res_low):
    import numpy as np
    from trydjango18.views import PathMaker
    layer_lines = 3
    #res_high = 0.251
    #res_low = 0.0
    R_step = 0.001
    path = PathMaker(name, "grid.dat")  #save in users folder
    f = open(path, "w")
    for layer_line in range(0,layer_lines,1):
        for q in np.arange(res_low,res_high,R_step):
            line = "10 %8.4f %4d\n" %(q,layer_line)
            f.write(line)
    f.close()
