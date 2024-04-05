# -*- coding: utf-8 -*-
import sys

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
# line = int(sys.argv[1])
# 初始化加密对象
my_ec = EC.E_C(line, '127.0.0.1', 8080)
# my_ec = EC.E_C(line, '192.168.1.103', 8080)
# 注册阶段
ID_A='111'
PW_A='111'
# S_A=my_ec.rand()
S_A=int(rand_line[line])
# print(S_A)

HW_A=my_ec.xor(en.sha256(PW_A),S_A)
D_A=my_ec.xor(en.sha256(S_A),ID_A)

data_of_UA=str(HW_A)+":"+str(D_A)
# en.write_data_to_file('U_A.txt',data_of_UA)
s=my_ec.bulid_connection_s()
CA_data=en.read_data_from_file(r'CA/CA_U_A_{}.txt'.format(str(line)))
r_A=CA_data.split(":")[0]
R_A=[int(CA_data.split(":")[1]),int(CA_data.split(":")[2])]
Z_A=CA_data.split(":")[3]
Z_B=CA_data.split(":")[4]
R_B=[int(CA_data.split(":")[5]),int(CA_data.split(":")[6])]


#密钥交换阶段**************************************************************************************************************

y_A=int(rand_line[line])
Retirieve=en.read_data_from_file('U_A.txt')
HW_A=Retirieve.split(":")[0]
D_A=Retirieve.split(":")[1]
V_A=[y_A]
V_A_em=en.read_data_from_file(str(line)+'/'+'skaleft')
V_A_em=V_A_em.split()
V_A.extend(V_A_em)
V_A= list(map(int,V_A))
W_A=[1]
W_A_em=en.read_data_from_file(str(line)+'/'+'skaright')
W_A_em=W_A_em.split()
W_A.extend(W_A_em)
W_A=list(map(int,W_A))
#向量相乘
t_v_mul_1=time.perf_counter()
Vector_V_A=np.array(V_A)
Vector_W_A=np.array(W_A)
U_A=int((Vector_V_A*Vector_W_A)[0])
t_v_mul_2=time.perf_counter()

t_encode_9=time.perf_counter()
test="abcdefg"
key="ADFSGSSSADFSGSSS"
scr=my_ec.aes_encode(test,key)
scr_=my_ec.aes_decode(scr,key)
t_encode_10=time.perf_counter()
#计算X_A
t_t_1=time.perf_counter()
t_xor_1=time.perf_counter()
X_A=en.sha256(my_ec.xor(my_ec.xor(my_ec.xor(HW_A,D_A),U_A),y_A)) #*******此处做了修改**************
t_xor_2=time.perf_counter()

#计算Y_A
t_mul_1=time.perf_counter()
Y_A=my_ec.mul(U_A+y_A)
t_mul_2=time.perf_counter()

#计算K_A
t_xor_3=time.perf_counter()
K_A=my_ec.xor(my_ec.xor(Z_A,en.sha256(HW_A+str(R_A[0])+str(R_A[1]))),X_A)
t_xor_4=time.perf_counter()

K_A= hex(K_A)[2:]
K_A=K_A[:16]

T_A=time.perf_counter()


secret=str(my_ec.xor(y_A,str(int(T_A))))



t_encode_1=time.perf_counter()
Auth=my_ec.aes_encode(secret,str(K_A))
t_encode_2=time.perf_counter()


t_hash_1=time.perf_counter()
C_A=en.sha256(str(T_A)+str(y_A)+Auth)
t_hash_2=time.perf_counter()




MESSAGE_1=str(X_A)+":"+str(Y_A[0])+":"+str(Y_A[1])+":"+str(T_A)+":"+str(C_A)+":"+str(Auth)
my_ec.send_s(MESSAGE_1,s)

#接受MESSAGE2
MESSAGE2=my_ec.recv_s(s)
X_B=MESSAGE2.split(":")[0]
Y_B=[int(MESSAGE2.split(":")[1]),int(MESSAGE2.split(":")[2])]
T_A=MESSAGE2.split(":")[3]
E_B=MESSAGE2.split(":")[4]

#计算tk_A
t_mul_3=time.perf_counter()
V_A=my_ec.mul_public(U_A+y_A,Y_B)
t_mul_4=time.perf_counter()
t_xor_5=time.perf_counter()
SK_A=my_ec.xor(my_ec.xor(X_A,X_B),en.sha256(str(V_A[0])+str(V_A[1])))
t_xor_6=time.perf_counter()
SK_A=MESSAGE2.split(":")[5]

t_encode_3=time.perf_counter()
EC_DATA=en.aes_decode(E_B,str(SK_A))
t_encode_4=time.perf_counter()
T_B=EC_DATA.split(":")[0]
HW_B_=EC_DATA.split(":")[1]
y_B_=EC_DATA.split(":")[2]
X_A_=EC_DATA.split(":")[3]
V_B_=[int(EC_DATA.split(":")[4]),int(EC_DATA.split(":")[5])]
T_A=EC_DATA.split(":")[6]
#验证X_A以及V_B
t_encode_5=time.perf_counter()
E_A=en.aes_encode(str(T_B)+":"+str(HW_A)+":"+str(y_A)+":"+str(U_A)+":"+str(X_B)+":"+str(V_A[0])+':'+str(V_A[1]),str(SK_A))
t_encode_6=time.perf_counter()
SID_A=str(X_A)+str(Y_A[0])+str(Y_A[1])+str(Y_B[0])+str(Y_B[1])
my_ec.send_s(E_A,s)
t_kdf_1=time.perf_counter()
SK=en.sha256(str(SK_A)+SID_A)
t_kdf_2=time.perf_counter()
t_t_2=time.perf_counter()
t_total=t_t_2-t_t_1
t_compute=t_kdf_2-t_kdf_1+t_encode_6-t_encode_5+t_encode_4-t_encode_3+t_encode_2-t_encode_1+t_mul_4-t_mul_3+t_mul_2-t_mul_1+t_xor_6-t_xor_5+t_xor_4-t_xor_3+t_v_mul_2-t_v_mul_1+t_xor_2-t_xor_1+t_hash_2-t_hash_1
print("t_total:", t_total)
print("t_compute:", t_compute)
print("mul1",t_mul_4-t_mul_3)
print("mul2",t_mul_2-t_mul_1)
print("vector",t_v_mul_2-t_v_mul_1)
print("KDF",t_kdf_2-t_kdf_1)
print("HASH",t_hash_2-t_hash_1)
print("encode",t_encode_2-t_encode_1)
print("encode",t_encode_4-t_encode_3)
print("encode",t_encode_6-t_encode_5)
print("encode",t_encode_10-t_encode_9)