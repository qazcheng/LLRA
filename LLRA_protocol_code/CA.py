import encryption as en
import  Encrypted_communications as EC
import numpy as np
import time
rand_line = {
    # Bits : (p, order of E(GF(P)), parameter b, base point x, base point y)
    192: (541684191820677320841734963754264226856146154995016786128),

    224: (18568673932360593714232431480917659097581400459588262326088477297081),

    256: (54725303002699221537195600223559096623940939960910680097864435290408478486757),

    384: (11455259982668289845714296494190191871123081081546992065216291026857273757860828780880674871162255506298002160302770),

    521: (6352033087243871280471436447854542749103989970101364640501645545364070645744733522773491757632313594292696883112602884459480194912189621130884123005568904206)
}
line = int(input("请输入椭圆曲线的类型"))
# 初始化加密对象
my_ec = EC.E_C(line, '127.0.0.1', 8080)
ID_A='111'
pw_A='111'
pw_B='111'
ID_B='111'
S_A=int(rand_line[line])
S_B=int(rand_line[line])
a=my_ec.rand()
b=my_ec.rand()
Retirieve_A=en.read_data_from_file('U_A.txt')
HW_A=Retirieve_A.split(":")[0]
D_A=Retirieve_A.split(":")[1]
Retirieve_B=en.read_data_from_file('U_B.txt')
HW_B=Retirieve_B.split(":")[0]
D_B=Retirieve_B.split(":")[1]
r_A=my_ec.rand()
r_B=my_ec.rand()
R_A=my_ec.mul(r_A)
R_B=my_ec.mul(r_B)
Z_A=my_ec.xor(en.sha256(str(a)+str(b)+str(S_A)+str(S_B)),en.sha256(HW_A+str(R_A[0])+str(R_A[1])))

Z_B=my_ec.xor(en.sha256(str(a)+str(b)+str(S_A)+str(S_B)),en.sha256(HW_B+str(R_B[0])+str(R_B[1])))
data_A=str(r_A)+":"+str(R_A[0])+":"+str(R_A[1])+":"+str(Z_A)+":"+str(Z_B)+":"+str(R_B[0])+":"+str(R_B[1])
data_B=str(r_B)+":"+str(R_B[0])+":"+str(R_B[1])+":"+str(Z_A)+":"+str(Z_B)+":"+str(R_A[0])+":"+str(R_A[1])
en.write_data_to_file('CA_U_A_{}.txt'.format(str(line)),data_A)
en.write_data_to_file('CA_U_B_{}.txt'.format((str(line))),data_B)
