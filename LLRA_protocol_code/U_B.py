# -*- coding: utf-8 -*-
import encryption as en
import  Encrypted_communications as EC
import numpy as np
import time
import sys
import hashlib
rand_line = {
    # Bits : (p, order of E(GF(P)), parameter b, base point x, base point y)
    192: (541684191820677320841734963754264226856146154995016786128),

    224: (18568673932360593714232431480917659097581400459588262326088477297081),

    256: (54725303002699221537195600223559096623940939960910680097864435290408478486757),

    384: (11455259982668289845714296494190191871123081081546992065216291026857273757860828780880674871162255506298002160302770),

    521: (6352033087243871280471436447854542749103989970101364640501645545364070645744733522773491757632313594292696883112602884459480194912189621130884123005568904206)
}
line = int(input("请输入椭圆曲线的类型"))
# line=int(sys.argv[1])
# 初始化加密对象
my_ec = EC.E_C(line, '127.0.0.1', 8080)
# my_ec = EC.E_C(line, '192.168.1.103', 8080)
# 注册阶段
ID_B='111'
PW_B='111'
# S_B=my_ec.rand()
S_B=int(rand_line[line])
HW_B=my_ec.xor(en.sha256(PW_B),S_B)
D_B=my_ec.xor(en.sha256(S_B),ID_B)
data_of_UB=str(HW_B)+":"+str(D_B)+":"+str(S_B)
# en.write_data_to_file('U_B.txt',data_of_UB)
CA_data=en.read_data_from_file(r'CA/CA_U_A_{}.txt'.format(str(line)))
r_A=CA_data.split(":")[0]
R_A=[int(CA_data.split(":")[1]),int(CA_data.split(":")[2])]
Z_A=CA_data.split(":")[3]
Z_B=CA_data.split(":")[4]
R_B=[int(CA_data.split(":")[5]),int(CA_data.split(":")[6])]
#密钥交换阶段

y_B=int(rand_line[line])
Retirieve=en.read_data_from_file('U_B.txt')
HW_B=Retirieve.split(":")[0]
D_B=Retirieve.split(":")[1]
V_B=[y_B]
V_B_em=en.read_data_from_file(str(line)+'/'+'skbleft')
V_B_em=V_B_em.split()
V_B.extend(V_B_em)
V_B= list(map(int,V_B))
W_B=[1]
W_B_em=en.read_data_from_file(str(line)+'/'+'skbright')
W_B_em=W_B_em.split()
W_B.extend(W_B_em)
W_B=list(map(int,W_B))
#向量相乘
t_v_mul_1=time.perf_counter()
Vector_V_B=np.array(V_B)
Vector_W_B=np.array(W_B)
U_B=int((Vector_V_B*Vector_W_B)[0])
t_v_mul_2=time.perf_counter()


t_encode_9=time.perf_counter()
test="abcdefg"
key="ADFSGSSSADFSGSSS"
scr=my_ec.aes_encode(test,key)
scr_=my_ec.aes_decode(scr,key)
t_encode_10=time.perf_counter()
u=my_ec.bulid_connection_u()

t_t_1=time.perf_counter()
#计算X_A
t_xor_1=time.perf_counter()
X_B=en.sha256(my_ec.xor(my_ec.xor(my_ec.xor(HW_B,D_B),U_B),y_B))
t_xor_2=time.perf_counter()

#计算Y_A
t_mul_1=time.perf_counter()
Y_B=my_ec.mul(U_B+y_B)
t_mul_2=time.perf_counter()
T_B=time.perf_counter()



#接受用户A发的消息

t_com_3=time.perf_counter()
MESSAGE1=my_ec.recv_u(u)
t_com_4=time.perf_counter()
X_A=MESSAGE1.split(":")[0]
Y_A=[int(MESSAGE1.split(":")[1]),int(MESSAGE1.split(":")[2])]
T_A=MESSAGE1.split(":")[3]
C_A=MESSAGE1.split(":")[4]
Auth=MESSAGE1.split(":")[5]

t_xor_3=time.perf_counter()
K_A_=my_ec.xor(Z_B,my_ec.xor(en.sha256(HW_B+str(R_B[0])+str(R_B[1])),X_A))
t_xor_4=time.perf_counter()
K_A_= hex(K_A_)[2:]
K_A_=K_A_[:16]

t_encode_1=time.perf_counter()
y_A_=my_ec.xor(my_ec.aes_decode(Auth,K_A_),str(int(float(T_A))))
t_encode_2=time.perf_counter()
t_hash_1=time.perf_counter()
C_A_=en.sha256(str(T_A)+str(y_A_)+Auth)
t_hash_2=time.perf_counter()

#验证CA和CA*

t_mul_3=time.perf_counter()
V_B=my_ec.mul_public(U_B+y_B,Y_A)
t_mul_4=time.perf_counter()
t_xor_5=time.perf_counter()
SK_B=my_ec.xor(my_ec.xor(X_A,X_B),en.sha256(str(V_B[0])+str(V_B[1])))
t_xor_6=time.perf_counter()
SK_B = hex(SK_B)[2:]
SK_B=SK_B[:16]
# en.write_data_to_file('TK_B.txt',str(TK_B))
t_encode_3=time.perf_counter()
E_B=en.aes_encode(str(T_B)+":"+str(HW_B)+":"+str(y_B)+":"+str(X_A)+':'+str(V_B[0])+':'+str(V_B[1])+':'+str(T_A),str(SK_B))
t_encode_4=time.perf_counter()
#发送X_B,Y_B,T_B,C_B
MESSAGE2=str(X_B)+":"+str(Y_B[0])+":"+str(Y_B[1])+":"+str(T_B)+":"+str(E_B)+":"+str(SK_B)
my_ec.send_u(MESSAGE2,u)

#接受
t_com_1=time.perf_counter()
E_A=my_ec.recv_u(u)

t_encode_5=time.perf_counter()
EC_DATA=en.aes_decode(E_A,str(SK_B))
t_encode_6=time.perf_counter()
T_B=EC_DATA.split(":")[0]
HW_A=EC_DATA.split(":")[1]
y_A=EC_DATA.split(":")[2]
U_A=EC_DATA.split(":")[3]
X_B_=EC_DATA.split(":")[4]
V_A_=[int(EC_DATA.split(":")[5]),int(EC_DATA.split(":")[6])]
#验证X_B以及V_A和V_B
SID_B=str(X_B)+str(Y_A[0])+str(Y_A[1])+str(X_B)+str(Y_B[0])+str(Y_B[1])
t_kdf_1=time.perf_counter()
SK=en.sha256(str(SK_B)+SID_B)
t_kdf_2=time.perf_counter()
t_t_2=time.perf_counter()
t_com_2=time.perf_counter()
t_total=t_t_2-t_t_1
t_compute=t_kdf_2-t_kdf_1+t_encode_6-t_encode_5+t_encode_4-t_encode_3+t_encode_2-t_encode_1+t_mul_4-t_mul_3+t_mul_2-t_mul_1+t_xor_6-t_xor_5+t_xor_4-t_xor_3+t_xor_2-t_xor_1+t_v_mul_2-t_v_mul_1+t_hash_2-t_hash_1
print("t_total:", t_total-t_encode_10+t_encode_9)
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
print("comm2",t_com_2-t_com_1)
print("comm1",t_com_4-t_com_3)


