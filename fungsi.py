import random

def cek_jml_pert():
    with open('pertanyaan.txt', 'r') as teks:
        q = []
        for baris in teks:
            terbesar = 0
            if baris.startswith('q'):
                q.append(int(baris[1:4]))
            else:
                continue
                
        for angka in q:
            if angka > terbesar:
                terbesar = angka
    
    return terbesar

def ambil_blok_pert(terbesar):
    with open('pertanyaan.txt', 'r') as tex:			
        acak = random.randint(1, terbesar)
        f = '{0:03}'.format(acak)
        qgroup =[]
        ketemu = False
        for row in tex:
            if row.startswith('q'+f+'#'):
                ketemu = True
            if ketemu:
                if 'q' + f + '#' in row:
                    qgroup.append(row[5:])
                else:
                    if row.strip().endswith('q'+f):
                        qgroup.append(row.strip()[:-4])
                    else:
                        qgroup.append(row[:-1].strip())
            if row.strip().endswith(f):
                ketemu = False
    return qgroup

def cetak_pert(qgroup):
    pert = []
    pert.append(qgroup[0])
    for i in range(1, len(qgroup)):
        pert.append(str(i) + '. ' + '_________')
    d = '\n'.join(pert)
    return d

def proses_jwb(qgroup, jawaban):
    j = []
    j.append(qgroup[0])
    for e in range(1, len(qgroup)):
        j.append(str(e)+'. ' + '???')
    for c in j:
        while '???' in c:
            a = jawaban.lower()
            if a in qgroup:
                p = qgroup.index(a)
                if j.count(str(p) + '. ' + a) == 1:
                    continue
                else:
                    for z in range(1,12):
                        if p == z:
                            j[z] = str(z) + '. ' + a
            g = ''.join(j)
            if '???' not in g:
                break
    return g
