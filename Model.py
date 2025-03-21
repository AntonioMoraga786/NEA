import random
import time

class Conv():
    def __init__(self,kD,n,I):
        # function to intialize all the paramers of the layers
        # kD is a variablel with the dimensions of the kernel [x,y,z]
        self.n = n# number of neurons
        self.im = I# input image dimensions [x,y,z]
        self.outputD = [1+self.im[0]-self.k[0],1+self.im[1]-self.k[1],self.n]
        
        self.bias = [2*random.random()-1 for i in range(n)]

        ## initialize the weights
        self.k = kD# save the kernel dimensions
        self.kernel = []# initialize the kernel weights list

        # loop though every neuron
        for neuron in range(self.n):
            k = []# buffer for the whole kernel of a neuron
            # loop though all of the kernel values to initialize them
            for z in range(self.k[2]):
                plane = []# buffer for the weights of the kernel

                for y in range(self.k[1]):
                    row = []# buffer for the weights of the kernel

                    for x in range(self.k[0]):
                        # generate a random weight -1 to 1
                        w = 2*random.random()-1
                        row.append(w)

                    plane.append(row)
                k.append(plane)
            self.kernel.append(k)

    def Pass(self,image):
        # perform a forward pass
        self.input = image# store the input matrix as well

        # initialize output list
        self.output = [[[0 for i in range(self.outputD[0])] for i in range(self.outputD[1])] for i in range(self.outputD[2])]

        # loop though all the output values
        for z in range(self.n):# for every neuron
            for y in range(self.outputD[1]):
                for x in range(self.outputD[0]):
                    o = self.bias[z]

                    # loop though allthe values in convolution of this value
                    for kz in range(self.k[2]):
                        for ky in range(self.k[1]):
                            for kx in range(self.k[0]):
                                o += self.input[kz][y+ky][x+kx]*self.kernel[z][kz][ky][kx]

                    self.output[z][y][x] = o

        # convolution is done

    def Back(self,dLdO):# perform back propagation
        ## initialize derivative lists
        self.dLdB = []#dL/dB

        ## calculate dL/dB:

        # for the dLdO of every kernel (2D)
        for kernel in dLdO:# for every neuron
            dLdB = 0# buffer for dL/dB for a kernel
            for row in kernel:# for the row in each plane
                dLdB += sum(row)# add the sum of all the values in the row

            self.dLdB.append(dLdB)# add value into bias derivatives

        ## v2
        self.dLdI = [[[0 for i in range(self.im[0])] for i in range(self.im[1])] for i in range(self.im[2])]
        self.dLdW = [[[[0 for i in range(self.k[0])] for i in range(self.k[1])] for i in range(self.k[2])] for i in range(self.n)]
        
        # loop though all the output values
        for z in range(self.outputD[2]):# for every neuron
            for y in range(self.outputD[1]):# for every row in each output
                for x in range(self.outputD[0]):

                    for kz in range(self.k[2]):
                        for ky in range(self.k[1]):
                            for kx in range(self.k[0]):
                                self.dLdI[kz][y+ky][x+kx] += self.kernel[z][kz][ky][kx]*dLdO[z][y][x]
                                self.dLdW[z][kz][ky][kx] += self.input[kz][y+ky][x+kx]*dLdO[z][y][x]

class dense():
    def __init__(self,n,I):
        self.inputD = I# input dimension (a singular integer value)
        self.bias = [2*random.random()-1 for i in range(n)]
        self.outputD = n

        self.kernel = []
        # loop though every neuron and generate its kernel values
        for neuron in range(n):
            weights = [2*random.random()-1 for i in range(I)]

            self.kernel.append(weights)

    def Pass(self,Input):
        # initialize variables
        self.input = Input
        self.output = []

        # loop though every neuron and calculate the output
        for n in range(self.outputD):
            output = self.bias[n]# add the bias value first

            # loop though every pair of weight and input vals
            for w,i in zip(self.kernel[n],self.input):
                output += w*i

            self.output.append(output)# append the calculated value into the list of outputs

        

