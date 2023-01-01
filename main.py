import os
import os.path
import telebot
import fungsi

bot = telebot.TeleBot(os.environ['API_KEY'])

def cekfile(berkas):
    if os.path.exists(berkas + '.txt') == False:
        with open(berkas + '.txt', 'w+') as buatfile:
            buatfile.close()

def cekisi(berkas):
  with open(berkas + '.txt') as baca:
      cek = baca.read(3)
  return cek

def bacafile(berkas):
    with open(berkas + '.txt', 'r') as cek:
        isi = cek.readlines()
    return isi

def ambilpertanyaan(berkas):
    with open(berkas + '.txt', 'w+') as f:
        jml = fungsi.cek_jml_pert()
        blok_pert = fungsi.ambil_blok_pert(jml)
        print(blok_pert)
        soal = '\n'.join(blok_pert)
        pertanyaan = fungsi.cetak_pert(blok_pert)
        f.write(blok_pert[0])
        nomer = []
        for n in range(1, len(blok_pert)):
            nomer.append(str(n) + '. ' + '_________')
        f.write('\n'.join(nomer))
        f.write('\n' + '#' + soal + '\n' + ':end')
    return pertanyaan


def dimulai(messages):
    for message in messages:
        a = str(message.text).lower()
        sesi = str(message.chat.id)
        if a == "/mulai" or a == "/mulai@Family100Robot":
            cekfile(sesi)
            kosong = cekisi(sesi)
            if not kosong:
                pertanyaan = ambilpertanyaan(sesi)
                bot.reply_to(message, pertanyaan)
            else:
                konten = bacafile(sesi)
                rewrite = []
                if not "_________" in ''.join(konten):
                    for vol in konten:
                        rewrite.append(vol)
                    pertanyaan = ambilpertanyaan(sesi)
                    with open(sesi + '.txt', 'r+') as restart:
                        restart.readlines()
                        restart.write('\n' + ''.join(rewrite))
                    bot.reply_to(message, pertanyaan)
                else:
                    soal = []
                    indek = [v for v, t in enumerate(konten) if '#' in t]
                    for u in konten:
                        if konten.index(u) < indek[0]:
                            soal.append(u.strip())
                    soali = "\n".join(soal)
                    bot.reply_to(message,"Kuis sudah dimulai.." + '\n' + '\n' + soali)
        elif a == "/pass" or a == "/pass@Family100Robot":
            konten = bacafile(sesi)
            kosong = cekisi(sesi)
            if not kosong or '_________' not in ''.join(konten):
                bot.reply_to(message, 'Pass apa? Game nya aja belum mulai, Ketik /mulai untuk memulai permainan.')
            else:
                rewrite = []
                if ": " in ''.join(konten):
                    skor = [i for i, s in enumerate(konten) if ": " in s]
                    for vol in konten:
                        if konten.index(vol) in skor:
                            rewrite.append(konten[konten.index(vol)])
                pertanyaan = ambilpertanyaan(sesi)
                with open(sesi + '.txt', 'a+') as logg:
                    logg.write('\n' + ''.join(rewrite))
                bot.reply_to(message, pertanyaan)
        elif a ==  "/nyerah" or a == "/nyerah@Family100Robot":
            konten = bacafile(sesi)
            kosong = cekisi(sesi)
            if not kosong or '_________' not in ''.join(konten):
                bot.reply_to(message, 'Nyerah apa? Game nya aja belum mulai, Ketik /mulai untuk memulai permainan.')
            else:
                batas = [i for i,s in enumerate(konten) if '#' in s ] 
                akhir = [i for i,s in enumerate(konten) if ':end' in s]
                tnd = []
                key = []
                for baris in konten:
                    if konten.index(baris) < batas[0]:
                        tnd.append(baris)
                    if konten.index(baris) < akhir[0] and konten.index(baris) > batas[0]:
                        key.append(baris.strip())
                tndtny = [i for i,s in enumerate(tnd) if '_________' in s]
                print(key)
                tnd[tndtny[0]] = str(tndtny[0])+ '. '+key[tndtny[0]]+ ' [bot]*\n'
                if '@' in ''.join(konten):
                    liskor = [i for i,s in enumerate(konten) if ': ' in s]
                    tnd.append('\n')
                    score = []
                    for skor in liskor:
                        tnd.append('\n'+konten[skor].strip())
                        score.append(konten[skor])
                    tnd.append('\n\nKetik /mulai untuk Pertanyaan Lainnya.')
                    bot.reply_to(message, ''.join(tnd))
                    with open(sesi+'.txt','w+') as tulis:
                        tulis.write(''.join(score)) 
                        tulis.close()
                else:
                    tnd.append('\n\nKetik /mulai untuk Pertanyaan Lainnya.')
                    bot.reply_to(message, ''.join(tnd))
        elif a == '/reset':
            with open(sesi+'.txt','w+') as clr:
                clr.close()
        else:
            kosong = cekisi(sesi)
            if not kosong:
                pass
            else:
                konten = bacafile(sesi)
                no_baris = [i for i, s in enumerate(konten) if '#' in s]
                no_baris2 = [i for i, s in enumerate(konten) if ':' in s]
                kunci_jwb = {}
                jwb = []
                for isi in konten:
                    if konten.index(isi) > 0 and konten.index(isi) < no_baris[0]:
                        jwb.append(isi[3:-1].split('(')[0])
                    if konten.index(isi) >= no_baris[0] and konten.index(isi) < no_baris2[0]:
                        if isi.startswith('#'):
                            kunci_jwb[isi[1:-1].strip()] = None
                        else:
                            kunci_jwb[isi.strip()] = None
                if a in list(kunci_jwb.keys()) and a in jwb:
                    pass
                elif a in list(kunci_jwb.keys()) and a not in jwb:
                    kunci = list(kunci_jwb.keys())
                    indeks = kunci.index(a)
                    pengirim = '@'+str(message.from_user.username)
                    skor = ['1','4','7','10','14','18','22','27','33','39','46','52']
                    for num in range(1, len(kunci)):
                        if indeks == num:
                            konten[num-1] = str(num-1)+'. '+a+' ('+skor[num-1]+')'+' [' + pengirim+']'+'\n'
                    if not pengirim + ':' in ''.join(konten):
                        konten.append('\n'+pengirim +': '+skor[indeks-1]+'\n')
                        print(skor[indeks])
                    else:
                        noskor = [i for i,s in enumerate(konten)
                            if pengirim+':' in s]
                        bariskor = konten[noskor[0]]
                        ekstrak = bariskor.split(' ')[-1]
                        jmlskor = int(ekstrak) + int(skor[indeks-1])
                        konten[noskor[0]] = '\n'+pengirim+': '+str(jmlskor)
                    with open(sesi+'.txt','w+') as tulis:
                        tulis.write(''.join(konten))
                        tulis.close()
                    skan = bacafile(sesi)
                    disp = []
                    disp2 = []
                    makskor = []
                    tanda = [i for i,s in enumerate(skan) if '#' in s]
                    mark = [i for i, s in enumerate(skan) if ': ' in s]
                    for hasil in skan:
                        if skan.index(hasil) < tanda[0]:
                            disp.append(hasil.strip())
                    for asil in skan:
                        if skan.index(asil) in mark:
                            disp2.append(asil)
                            for stat in disp2:
                                inte = stat.split(' ')[-1]
                                makskor.append(int(inte))
                    kirim = '\n'.join(disp)
                    skorr = '\n'.join(disp2)
                    maks = 0
                    for t in makskor:
                        if t > 149:
                            maks = t
                    if not '_________' in kirim:
                        bot.reply_to(message, kirim+'\n\n'+'Skor sementara:\n'+skorr+'\n\n'+" Semua telah terjawab.. ketik /mulai untuk pertanyaan lain")
                        with open(sesi + '.txt', 'w+') as bersih:
                            bersih.write(skorr)
                    elif maks >= 350:
                        bot.reply_to(message,"Kuis telah berakhir..\n\nSkor akhir:\n"
                            + skorr + "\n\nSelamat untuk @" +
                            str(message.from_user.username) +
                            ", kamu adalah pemenangnya!")
                        with open(sesi + '.txt', 'w+') as clearr:
                            clearr.write('')
                    else:
                        bot.reply_to(
                            message, kirim + '\n\n' +
                            'Skor sementara:\n' + skorr)
                else:
                    pass


bot.set_update_listener(dimulai)
bot.infinity_polling()
