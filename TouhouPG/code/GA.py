from random import choices, randint, randrange, random
from typing import List

class gene:
    chromosome= List[int]
    population = List[chromosome]
    ft_total = 0
    num_chromo = int
    num_popul = int



    def generate_chromosome(self,size: int) -> chromosome:
        return [randint(0,30) for _ in range(size)]

    def generate_population(self,size: int, chromosome_length: int)-> population:
        return  [self.generate_chromosome(chromosome_length) for _ in range(size)]


    def chromosome_to_str(self,chromosome: chromosome)->str:
        return ",".join(map(str,chromosome))

    def population_to_str(self,population: population):
        print("Population: [%s]" % " <> ".join([self.chromosome_to_str(chromosome) for chromosome in population]))
    
    def calculate_fx(self,chromosome: chromosome)->int:
       a=chromosome[0]
       b=chromosome[1]
       c=chromosome[2]  
       d=chromosome[3]
       ''' formula a cambiar '''
       f_x = (a+2*b+3*c+4*d ) - 30 
       
       return f_x
    
    def calculate_fx_population(self,population: population)->List[int]:
        f_x_list = []
        for chromosome in population:
            f_x_list.append( self.calculate_fx(chromosome))
        return f_x_list
             
    
    def calc_fitness(self,f_x:List[int])->[float]: 
      Lista =[]
      for fit in f_x:
            resul =(1/(1+(fit)))
            Lista.append(resul)
      return Lista      
               
      
    def calc_fitness_total(self,f_x:List[int]): 
       Fitness =self.calc_fitness(f_x)

       for fit in Fitness:
             self.ft_total = self.ft_total + fit
    
    def calc_probability(self,f_x:List[int])->List[float]:
          probability = []
          fitness= self.calc_fitness(f_x)
          for fitnessI in fitness:

            probability.append((fitnessI)/self.ft_total)
          return probability
    
    def calc_cum_probability(self,f_x:List[int])->List[float]:
            probability = self.calc_probability(f_x)
            cumumulative = []
            for i in probability:
                result = 0
                for j in probability:
                     result = j + result
                     if j == i : 
                        cumumulative.append(result)
                        break
            
            return cumumulative
    def random(self,size:int)->List[float]:
        randoms =[]
        contador=0
        tamano = range(0,size)
        for _ in tamano:
            if(contador>size):
                break
            randoms.append((float)(randint(0,1000))/1000)
        return randoms
        
    def range_max(self,cumulative:List[float],random:List[float])->List[int]:
        range_list = []
        posicion = 0
        for valor in random:
            
            check = True
            temp = posicion
            resul = 1
            
            while(check):
                posi = posicion
                if(abs((cumulative[temp]-valor))<resul and cumulative[temp]>valor):
                    resul = abs(cumulative[temp]-valor)
                    posi = temp+1
                if(temp+1 == len(random)):
                    temp=0
                else:    
                    temp+=1
                if(temp==posicion):
                        range_list.append(posi)
                        check = False    
            posicion+=1
        return range_list
    
    def chromosome_change(self,population:population,range:List[int])->List:
        list_copy = []
        for pos in range:
            list_copy.append(population[pos-1])
        return list_copy                        

    def selected_crossover(self,randoms:List[float],change:population,numC:int)->List:
        ### valor para la mutacion .20
        
        index_selecCross = []
        index = []
        selec_cross = []
        pos = 0
        max_val = numC-1
        for val in randoms:
            if val < .20 :
              selec_cross.append([pos+1,randint(1,max_val)])
              index.append(pos+1)
                
            pos+=1 
        if(len(selec_cross)>0):
            temp = selec_cross.pop(0)
            selec_cross.append(temp)
        index_selecCross.append(index)
        index_selecCross.append(selec_cross)  

        return index_selecCross
                
    def crossover(self,index_selecross:List,pop:population)->population:
            pop_copy = pop
            index_list = index_selecross[0]
            selec_cross = index_selecross[1]
            index = 0
            
            for item in index_list:
                    item -= 1
                    i_b = selec_cross[index] 
                    a = pop[item]
                    b =pop[(i_b[0])-1]
                    temp = a[0:i_b[1]] + b[i_b[1]:]
                    pop_copy[item] = temp
                    del a
                    del b
                    index+=1
    
            return pop_copy
    def mutations(self,mutationrate:float,totalGen:int,population:population,random:int)->population:
        num_mutation =(int) (mutationrate * totalGen)
        mutations=[]
        for _ in range(0,num_mutation):
            mutations.append( randint(0,random) )
            contador =0
            for chrom in population:
                index=0
                for _ in chrom:
                    
                    if contador in mutations:
                        chrom[index] = randint(0,30)
                    index+=1
                    contador+=1
        return population


    def generar_generacion(self,numChrom:int,numPop:int)->population:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = self.generate_population(numPop,numChrom)
            print(self.population_to_str(population))
            f_x =self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total" , self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades" ,probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob )
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob,randoms)
            print("rangos ",range_list)
            population = self.chromosome_change(population,range_list)
            print("gene cambio ",population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2,population,numChrom)
            print("selec cross",crossing )
            cambio = self.crossover(crossing,population)
            print("crossover",cambio)
            gen2 = self.mutations(.10,totalGen,cambio,30)

            return gen2
    
    def generar_generacion_population(self,numChrom:int,numPop:int,pop:population)->population:
            self.num_chromo = numChrom
            self.num_popul = numPop
            totalGen = numChrom * numPop
            population = pop
            print(self.population_to_str(population))
            f_x =self.calculate_fx_population(population)
            print(f_x)
            self.calc_fitness_total(f_x)
            print("total" , self.ft_total)
            probability = self.calc_probability(f_x)
            print("Probabilidades" ,probability)
            cumu_prob = self.calc_cum_probability(f_x)
            print("Probabilidades Acumulads", cumu_prob )
            randoms = self.random(numPop)
            print("Randoms", randoms)
            range_list = self.range_max(cumu_prob,randoms)
            print("rangos ",range_list)
            population = self.chromosome_change(population,range_list)
            print("gene cambio ",population)
            randoms_2 = self.random(numPop)
            print("Randoms", randoms_2)
            crossing = self.selected_crossover(randoms_2,population,numChrom)
            print("selec cross",crossing )
            cambio = self.crossover(crossing,population)
            print("crossover",cambio)
            gen2 = self.mutations(.10,totalGen,cambio,30)

            return gen2
           

gen = gene()

gene1=gen.generar_generacion(4,6)

gen.generar_generacion_population(4,6,gene1)