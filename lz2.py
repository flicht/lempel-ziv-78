from numpy import random, arange
from math import ceil, log
import csv
import time


def make_random_binary_string(length,probofzero):
    """Makes a random string of binary with a given length and probability"""
    
    output = ''
    
    for i in range(length):
        
        output += str(random.choice(arange(0,2),p=[probofzero,1-probofzero]))
        
    return output


def encode(inputstring):
    """Encodes a binary string using Lempel Ziv 78"""
    outputstring = make_pointers(check_last_substring_unique(make_ordered_array(inputstring)))
    
    return outputstring
    
    
def make_ordered_array(source):
    """STEP 1 OF ENCODER: Make an array of unseen substrings of the source message"""
    output_array = ['']
    i = 0
    j = 1
    
    while j <= len(source):
        block = source[i:j]
        while block in output_array:
            if j == len(source):
                block = source[i:]
                break
            j += 1
            block = source[i:j]
            
            
        output_array.append(block)
        i=j
        j+=1
    
    return output_array


def check_last_substring_unique(ordered_array):
    """STEP 2 OF ENCODER: Checks to see if last substring in array is unique, if it isn't, it removes it."""
    if ordered_array[-1] in ordered_array[:-1]:
        print 'Last block not unique. Removing... \nIt had length ' + str(len(ordered_array[-1]))
        LAST_BLOCK_SIZE = len(ordered_array[-1])
        ordered_array.pop()
    
    
    return ordered_array
        
    
def make_pointers(ordered_array):
    """STEP 3 OF ENCODER: Makes the pointers and outputs encoded string"""
   
    output_string = ''
    for i in range(1,len(ordered_array)):
        block = ordered_array[i][0:len(ordered_array[i])-1]
        for j in range(i):
            if ordered_array[j] == block:
                convert_integer_to_binary = "{0:0" + str(int(ceil(log(i,2)))) + "b}"
                output_string += convert_integer_to_binary.format(j)
                output_string += ordered_array[i][-1:]

    
    output_string = output_string[1:]
    return output_string
        
        
def decode(string):
    """Decodes a lempel-ziv 78 encoded string"""
    if string == '':
        output = ''
    else:
        j = 1
        output = ['']
        output.append(string[0])
        for i in range(2,len(string)+1):
            k = int(ceil(log(i,2)))
            pointer = string[j:j+k]

            if pointer == '':
                None
            else:
                binary_converter = int(string[j:j+k],2)
                a = output[binary_converter]


                a += string[j+k]
                output.append(a)
                j+=k+1


        output = make_array_into_string(output)

    return output


def make_array_into_string(array):
    """Turns a given array into a string"""
   
    output_string = ''
    
    for i in array:
        output_string = output_string + str(i)
    
    return output_string



def main(prob):
    """Runs the algorithm 1000 times for different length of strings given a probability, decodes the string and writes to a csv file"""
    length = [10,100,1000,10000,100000,1000000,10000000]
    with open('outputfile.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)

        for i in length:
            for j in range(1000):
                timer = time.time()
                print i
                a = make_random_binary_string(i,prob)
                b = make_ordered_array(a)
                c = check_last_substring_unique(b)
                d = do_lempel_ziv(c)
                time_elapsed = time.time() - timer
                e = decoder(d)
                l = ''
                for k in c:
                    l+=k
                print l==e
                writer.writerow([i,len(d),len(l),l==e, time_elapsed])


                
if __name__ == "__main__":
    main(0.11)
    
        






    

