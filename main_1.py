import copy
import random

def Ik(k):
    Ik = []
    for i in range(0, k):
        I = []
        for j in range(0, k):
            if j == i:
                I.append(1)
            else:
                I.append(0)
        Ik.append(I)
    return Ik


def attachHorizontal(M1, M2):
    M3 = []
    for i in range(0, len(M1)):
        m = []
        for j in range(0, len(M1[0]) + len(M2[0])):
            if j < len(M1[0]):
                m.append(M1[i][j])
            else:
                m.append(M2[i][j - len(M1[0])])
        M3.append(m)
    return M3


def attachVertical(M1, M2):
    M3 = copy.copy(M1)
    for m in M2:
        M3.append(m)
    return M3


def sum(V):
    s = 0
    for v in V:
        s += v
    return s


def genX(n, k):
    X = []
    x = []
    for i in range(0, n - k):
        x.append(0)
    flag = True
    while flag:
        flag = False
        for j in range(0, len(x)):
            if x[len(x) - j - 1] == 0:
                x[len(x) - j - 1] = 1
                break
            else:
                x[len(x) - j - 1] = 0
        if (sum(x) > 1):
            X.append(copy.copy(x))
        if len(X) != k:
            flag = True
    return X


def G1(r):
    n = 2 ** r - 1
    k = 2 ** r - r - 1
    return attachHorizontal(Ik(k), genX(n, k))


# def G2(r):
#     n = 2 ** r
#     k = 2 ** r - r - 1
#     return attachHorizontal(Ik(k), genX(n, k))


def H1(r):
    n = 2 ** r - 1
    k = 2 ** r - r - 1
    return attachVertical(genX(n, k), Ik(n - k))


# def H2(r):
#     n = 2 ** r
#     k = 2 ** r - r - 1
#     return attachVertical(genX(n, k), Ik(n - k))

def G2(r):
    G = G1(r)
    for i in range(0, len(G)):
        a = 0
        for j in range(0, len(G[i])):
            if G[i][j] == 1:
                a += 1
        if a & 1:
            G[i].append(1)
        else:
            G[i].append(0)
    return G


def H2(r):
    H = H1(r)
    h = []
    for i in range(0, len(H[0])):
        h.append(0)
    H.append(h)
    for i in range(0, len(H)):
        H[i].append(1)
    return H


def sumV(v1, v2):
    v3 = []
    for i in range(0, len(v1)):
        v3.append((v1[i] + v2[i]) % 2)
    return v3


def located(v, M):
    for i in range(0, len(M)):
        a = 0
        for j in range(0, len(M[0])):
            if v[j] == M[i][j]:
                a += 1
        if a == len(M[0]):
            return True
    return False


def U(g):
    U = []
    G = copy.copy(g)
    for j in range(0, len(G[0])):
        u = []
        for i in range(0, len(G)):
            u.append(G[i][j])
        if not located(u, U):
            U.append(u)
    flag = True
    while flag:
        flag = False
        for i in range(0, len(U)):
            for j in range(i + 1, len(U)):
                if len(U) == 2047:
                    return U
                if not located(sumV(U[i], U[j]), U):
                    U.append(sumV(U[i], U[j]))
                    flag = True
    return U


def vM(v, M):
    vM = []
    for i in range(0, len(M[0])):
        c = 0
        for j in range(0, len(M)):
            c += M[j][i] * v[j]
        vM.append(c % 2)
    return vM


def V(u, g):
    U = copy.copy(u)
    G = copy.copy(g)
    V = []
    for i in range(0, len(U)):
        V.append(vM(U[i], G))
    return V


def e(n, errors):
    e = []
    for i in range(0, n):
        e.append(0)
    for i in range(0, errors):
        flag = True
        while flag:
            j = round(random.random() * n) - 1
            if e[j] != 1:
                e[j] = 1
                flag = False
    return e


def locatedIndex(v, M):
    for i in range(0, len(M)):
        a = 0
        for j in range(0, len(M[0])):
            if v[j] == M[i][j]:
                a += 1
        if a == len(M[0]):
            return i
    return -1


def correctWord(H, sindrom, word):
    i = locatedIndex(sindrom, H)
    if i != -1:
        word[i] = (word[i] + 1) % 2
    else:
        print("Такого синдрома нет в матрице Н")
    return word


def correctWord2mistakes(H, sindrom, word):
    k = -1
    d = -1
    for i in range(len(H)):
        if located(sindrom, [H[i]]):
            k = i
            break
        for j in range(i + 1, len(H)):
            if located(sindrom, [sumV(H[i], H[j])]):
                k = i
                d = j
    if k == -1:
        print("Такого синдрома нет в матрице синдромов")
    else:
        word[k] += 1
        word[k] %= 2
        if d != -1:
            word[d] += 1
            word[d] %= 2
    return word


def correctWord3mistakes(H, sindrom, slovo):
    k = -1
    d = -1
    g = -1
    for i in range(len(H)):
        if located(sindrom, [H[i]]):
            k = i
            break
        for j in range(i + 1, len(H)):
            if located(sindrom, [sumV(H[i], H[j])]):
                k = i
                d = j
                break
            for e in range(j + 1, len(H)):
                if located(sindrom, [sumV(sumV(H[i], H[j]), H[e])]):
                    k = i
                    d = j
                    g = e
                    break
            if k >= 0:
                break
        if k >= 0:
            break
    if k == -1:
        print("Такого синдрома нет в матрице синдромов", '\n')
    else:
        slovo[k] += 1
        slovo[k] %= 2
        if d != -1:
            slovo[d] += 1
            slovo[d] %= 2
        if g != -1:
            slovo[g] += 1
            slovo[g] %= 2
    return slovo


def correctWord4mistakes(H, sindrom, slovo):
    k = -1
    d = -1
    g = -1
    z = -1
    for i in range(len(H)):
        if located(sindrom, [H[i]]):
            k = i
            break
        for j in range(i + 1, len(H)):
            if located(sindrom, [sumV(H[i], H[j])]):
                k = i
                d = j
                break
            for e in range(j + 1, len(H)):
                if located(sindrom, [sumV(sumV(H[i], H[j]), H[e])]):
                    k = i
                    d = j
                    g = e
                    break
                for y in range(e + 1, len(H)):
                    if located(sindrom, [sumV(sumV(sumV(H[i], H[j]), H[e]), H[y])]):
                        k = i
                        d = j
                        g = e
                        z = y
                        break
                if k >= 0:
                    break
            if k >= 0:
                break
        if k >= 0:
            break
    if k == -1:
        print("Такого синдрома нет в матрице синдромов", '\n')
    else:
        slovo[k] += 1
        slovo[k] %= 2
        if d != -1:
            slovo[d] += 1
            slovo[d] %= 2
        if g != -1:
            slovo[g] += 1
            slovo[g] %= 2
        if z != -1:
            slovo[z] += 1
            slovo[z] %= 2
    return slovo


def fun1 (R):
    r = R

    G = G1(r)
    print("\nG = ")
    for k in range(0, len(G)):
        print(G[k])

    H = H1(r)
    print("\nH = ")
    for k in range(0, len(H)):
        print(H[k])

    U1 = U(G)
    print("\nU = ")
    print(U1[random.randint(0, len(U1) - 1)])

    V1 = V(U1, G)
    v = V1[random.randint(0, len(V1) - 1)]
    print("\nкодовое слово = ")
    print(v)

    e1 = e(len(v), 1)
    print("\ne1 = ")
    print(e1)

    word1 = sumV(v, e1)
    print("\nкодовое слово с одной ошибкой = ")
    print(word1)

    sindrom1 = vM(word1, H)
    print("\nсиндром кодового слова с одной ошибкой = ")
    print(sindrom1)

    print("\nисправленное кодовое слово c одной ошибкой = ")
    correctWord(H, sindrom1, word1)
    print(word1)

    print("\nпроверка = ")
    print(vM(word1, H))

    e2 = e(len(v), 2)
    print("\ne2 = ")
    print(e2)

    word2 = sumV(v, e2)
    print("\nкодовое слово с двумя ошибками = ")
    print(word2)

    sindrom2 = vM(word2, H)
    print("\nсиндром кодового слова с двумя ошибками = ")
    print(sindrom2)

    print("\nисправленное кодовое слово c двумя ошибками = ")
    correctWord2mistakes(H, sindrom2, word2)
    print(word2)

    print("\nпроверка = ")
    print(vM(word2, H))

    e3 = e(len(v), 3)
    print("\ne3 = ")
    print(e3)

    word3 = sumV(v, e3)
    print("\nкодовое слово с тремя ошибками = ")
    print(word3)

    sindrom3 = vM(word3, H)
    print("\nсиндром кодового слова с тремя ошибками = ")
    print(sindrom3)

    print("\nисправленное кодовое слово c тремя ошибками = ")
    correctWord3mistakes(H, sindrom3, word3)
    print(word3)

    print("\nпроверка = ")
    print(vM(word3, H))


def fun2 (R):
    r = R

    G = G2(r)
    print("\nG = ")
    for k in range(0, len(G)):
        print(G[k])

    H = H2(r)
    print("\nH = ")
    for k in range(0, len(H)):
        print(H[k])

    U1 = U(G)
    print("\nU = ")
    print(U1[random.randint(0, len(U1) - 1)])

    V1 = V(U1, G)
    v = V1[random.randint(0, len(V1) - 1)]
    print("\nкодовое слово = ")
    print(v)

    e2 = e(len(v), 2)
    print("\ne2 = ")
    print(e2)

    word2 = sumV(v, e2)
    print("\nкодовое слово с двумя ошибками = ")
    print(word2)

    sindrom2 = vM(word2, H)
    print("\nсиндром кодового слова с двумя ошибками = ")
    print(sindrom2)

    print("\nисправленное кодовое слово c двумя ошибками = ")
    correctWord2mistakes(H, sindrom2, word2)
    print(word2)

    print("\nпроверка = ")
    print(vM(word2, H))

    e3 = e(len(v), 3)
    print("\ne3 = ")
    print(e3)

    word3 = sumV(v, e3)
    print("\nкодовое слово с тремя ошибками = ")
    print(word3)

    sindrom3 = vM(word3, H)
    print("\nсиндром кодового слова с тремя ошибками = ")
    print(sindrom3)

    print("\nисправленное кодовое слово c тремя ошибками = ")
    correctWord3mistakes(H, sindrom3, word3)
    print(word3)

    print("\nпроверка = ")
    print(vM(word3, H))

    e4 = e(len(v), 4)
    print("\ne4 = ")
    print(e4)

    word4 = sumV(v, e4)
    print("\nкодовое слово с четырьмя ошибками = ")
    print(word4)

    sindrom4 = vM(word4, H)
    print("\nсиндром кодового слова с четырьмя ошибками = ")
    print(sindrom4)

    print("\nисправленное кодовое слово c четырьмя ошибками = ")
    correctWord3mistakes(H, sindrom4, word4)
    print(word4)

    print("\nпроверка = ")
    print(vM(word4, H))


fun1(2)
fun1(3)
fun1(4)
fun2(2)
fun2(3)
fun2(4)