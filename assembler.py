import re

dest = {'':'000','M=':'001','D=':'010','MD=':'011',
      'A=':'100','AM=':'101','AD=':'110','AMD=':'111'}

jump = {'':'000',';JGT':'001',';JEQ':'010',';JGE':'011',
      ';JLT':'100',';JNE':'101',';JLE':'110',';JMP':'111'}

comp = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100',
      'A':'0110000','M':'1110000','!D':'0001101','!A':'0110001',
      '!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011',
      'D+1':'0011111','A+1':'0110111','M+1':'1110111','D-1':'0001110',
      'A-1':'0110010','M-1':'1110010','D+A':'0000010','D+M':'1000010',
      'D-A':'0010011','D-M':'1010011','A-D':'0000111','M-D':'1000111',
      'D&A':'00000000','D&M':'1000000','D|A':'0010101','D|M':'1010101'}

symbol = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576,
         'R0':0,'R1':1,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6,'R7':7,
         'R8':8,'R9':9,'R10':10,'R11':11,'R12':12,'R13':13,'R14':14,'R15':15}

asmList=[]
a=[]
f=input('Type Name of File You Want to Assemble: ')
asm=open(f+'.asm','r')

for line in asm:
    x=re.sub(r'\/+.*\n|\n| *','',line)
    if x!='':
        a.append(x)
asm.close()
line=0
for command in a:
    symbol=re.findall(r'\(.+\)',command)
    if symbol!=[]:
        if symbol[0][1:-1] not in symbol:
            symbol[symbol[0][1:-1]] = line
            line-=1
    line+=1     
for line in a:
    x=re.sub(r'\(.+\)','',line)
    if x!='':
        asm.append(x)
vNum=16   
for command in asm:
    symbol=re.findall(r'@[a-zA-Z]+.*',command)
    if symbol!=[]:
        if symbol[0][1:] not in symbol:
            symbol[symbol[0][1:]] = vNum
            vNum+=1
       
file=open(f+'1.hack','w')
for command in asm:
    if command[0]=='@':
        address=0
        if command[1:] in symbol:
            address=symbol[command[1:]]+32768
        else:
            address=int(command[1:])+32768
        file.write('0'+bin(address)[3:]+'\n')
    else:
        de=re.findall(r'.+=',command)
        if de!=[]:
            d=dest[str(de[0])]
        else:
            d=dest['']
        je=re.findall(r';.+',command)
        if je!=[]:
            j=jump[str(je[0])]
        else:
            j=jump['']    
        c=comp[re.sub(r'.+=|;.+','',command)]
        file.write('111'+c+d+j+'\n')
file.close()