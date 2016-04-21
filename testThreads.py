import multiprocessing as mp

def f(x):
#  f.q.put("Writing Value %s" % x)
  return "Value returned "+str(x)

#def f_init(q):
#  f.q = q
#  
def main():
  jobs = range(1,5)
  
#  q = mp.Queue()
  p = mp.Pool(20)
  
  results = p.map(f, jobs)
  p.close()
  
  for i in range(len(jobs)):
#    print(q.get())
    print(results.next())
    
if __name__ == "__main__":
  main()