import os
import os.path
import telebot
import fungsi

bot = telebot.TeleBot(os.environ['API_KEY'])


def dimulai(messages):
    for message in messages:
        a = str(message.text).lower()
        sesi = str(message.chat.id)
        if a == "/mulay" or a == "/mulay@kuistrivia_bot":
            if os.path.exists(sesi + '.txt') == False:
                with open(sesi + '.txt', 'w+') as buatfile:
                    buatfile.close()
            with open(sesi + '.txt') as baca:
                jml_pert = baca.read(1)
            if not jml_pert:
                with open(sesi + '.txt', 'w+') as logg:
                    jml = fungsi.cek_jml_pert()
                    blok_pert = fungsi.ambil_blok_pert(jml)
                    print(blok_pert)
                    soal = '\n'.join(blok_pert)
                    pertanyaan = fungsi.cetak_pert(blok_pert)
                    logg.write(blok_pert[0])
                    nomer = []
                    for n in range(1, len(blok_pert)):
                        nomer.append(str(n) + '. ' + '???')
                    logg.write('\n'.join(nomer))
                    logg.write('\n' + '#' + soal + '\n' + ':end')
                bot.reply_to(message, pertanyaan)
            else:
                with open(sesi + '.txt', 'r') as cek:
                    isi = cek.readlines()
                    rewrite = []
                    if not "???" in ''.join(isi):
                        for vol in isi:
                            rewrite.append(vol)
                        with open(sesi + '.txt', 'w+') as restart:
                            jml = fungsi.cek_jml_pert()
                            blok_pert = fungsi.ambil_blok_pert(jml)
                            print(blok_pert)
                            soal = '\n'.join(blok_pert)
                            pertanyaan = fungsi.cetak_pert(blok_pert)
                            restart.write(blok_pert[0])
                            nomer = []
                            for n in range(1, len(blok_pert)):
                                nomer.append(str(n) + '. ' + '???')
                            restart.write('\n'.join(nomer))
                            restart.write('\n' + '#' + soal + '\n' + ':end')
                            restart.write('\n' + ''.join(rewrite))
                        bot.reply_to(message, pertanyaan)
                    else:
                        soal = []
                        indek = [v for v, t in enumerate(isi) if '#' in t]
                        for u in isi:
                            if isi.index(u) < indek[0]:
                                soal.append(u.strip())
                        soali = "\n".join(soal)
                        bot.reply_to(
                            message,
                            "Kuis sudah dimulai.." + '\n' + '\n' + soali)
        elif a == "/pass" or a == "/pass@kuistrivia_bot":
            rewrite = []
            with open(sesi + '.txt', 'r') as cek:
                isi = cek.readlines()
                if ": " in ''.join(isi):
                    skor = [i for i, s in enumerate(isi) if ": " in s]
                    for vol in isi:
                        if isi.index(vol) in skor:
                            rewrite.append(isi[isi.index(vol)])
            with open(sesi + '.txt', 'w+') as logg:
                jml = fungsi.cek_jml_pert()
                blok_pert = fungsi.ambil_blok_pert(jml)
                print(blok_pert)
                soal = '\n'.join(blok_pert)
                pertanyaan = fungsi.cetak_pert(blok_pert)
                logg.write(blok_pert[0])
                nomer = []
                for n in range(1, len(blok_pert)):
                    nomer.append(str(n) + '. ' + '???')
                logg.write('\n'.join(nomer))
                logg.write('\n' + '#' + soal + '\n' + ':end')
                logg.write('\n' + ''.join(rewrite))
            bot.reply_to(message, pertanyaan)
        else:
            with open(sesi + '.txt', 'r+') as woco:
                cek = woco.read(1)
                if not cek:
                    pass
                else:
                    woco.seek(0)
                    konten = woco.readlines()
                    no_baris = [i for i, s in enumerate(konten) if '#' in s]
                    no_baris2 = [i for i, s in enumerate(konten) if ':' in s]
                    kunci_jwb = []
                    for isi in konten:
                        if konten.index(isi) >= no_baris[0] and konten.index(
                                isi) < no_baris2[0]:
                            if isi.startswith('#'):
                                kunci_jwb.append(isi[1:-1].strip())
                            else:
                                kunci_jwb.append(isi.strip())
                    if a in kunci_jwb:
                        b = []
                        for li in konten:
                            if konten.index(li) > 1 and konten.index(
                                    li) < no_baris[0]:
                                b.append(li[3:-1].split(' ')[0])
                        if a in b:
                            pass
                        else:
                            p = kunci_jwb.index(a)
                            pengirim = str(message.from_user.username)
                            skor = [
                                1, 4, 7, 10, 14, 18, 22, 27, 33, 39, 46, 52
                            ]
                            for z in range(1, len(kunci_jwb)):
                                if p == z:
                                    konten[z - 1] = str(
                                        z - 1) + '. ' + a + ' (' + str(
                                            skor[z - 1]
                                        ) + ')' + ' [@' + pengirim + ']' + '\n'
                                    if not pengirim + ':' in ''.join(konten):
                                        konten.append('\n' + '@' + pengirim +
                                                      ': ' + str(skor[z - 1]) +
                                                      '\n')
                                    else:
                                        noskor = [
                                            i for i, s in enumerate(konten)
                                            if pengirim + ':' in s
                                        ]
                                        bariskor = konten[noskor[0]]
                                        ekstrak = bariskor.split(' ')[-1]
                                        jmlskor = int(ekstrak) + skor[z - 1]
                                        konten[noskor[
                                            0]] = '@' + pengirim + ': ' + str(
                                                jmlskor)
                            woco.seek(0)
                            woco.read(0)
                            woco.write(''.join(konten))
                            woco.close()
                            with open(sesi + '.txt', 'r+') as boh:
                                skan = boh.readlines()
                                disp = []
                                disp2 = []
                                makskor = []
                                tanda = [
                                    i for i, s in enumerate(skan) if '#' in s
                                ]
                                mark = [
                                    i for i, s in enumerate(skan) if ': ' in s
                                ]
                                for hasil in skan:
                                    if skan.index(hasil) < tanda[0]:
                                        disp.append(hasil.strip())
                                for asil in skan:
                                    if skan.index(asil) in mark:
                                        disp2.append(asil.strip())
                                        for stat in disp2:
                                            inte = stat.split(' ')[-1]
                                            makskor.append(int(inte))
                                kirim = '\n'.join(disp)
                                skorr = '\n'.join(disp2)
                                maks = 0
                                for t in makskor:
                                    if t > 349:
                                        maks = t
                                if not '???' in kirim:
                                    bot.reply_to(
                                        message, kirim + '\n\n' +
                                        'Skor sementara:\n' + skorr + '\n\n' +
                                        " Semua telah terjawab.. ketik /mulay untuk pertanyaan lain"
                                    )
                                    with open(sesi + '.txt', 'w+') as bersih:
                                        bersih.write(skorr)
                                elif maks >= 350:
                                    bot.reply_to(
                                        message,
                                        "Kuis telah berakhir..\n\nSkor akhir:\n"
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
