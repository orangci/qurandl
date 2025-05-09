import aiofiles
import difflib
import aiohttp
import asyncio
import sys
import os

reciters = [
    "abdallah_abdal",
    "abdul_basit_murattal",
    "abdul_muhsin_alqasim",
    "abdul_wadood_haneef_rare",
    "abdulazeez_al-ahmad",
    "abdulbaset_mujawwad",
    "abdulbaset_warsh",
    "abdulbaset_with_naeem_sultan_pickthall",
    "abdulbasit_w_ibrahim_walk_si",
    "abdulkareem_al_hazmi",
    "abdullaah_3awwaad_al-juhaynee",
    "abdullaah_alee_jaabir",
    "abdullaah_alee_jaabir_studio",
    "abdullaah_basfar",
    "abdullah_basfar_w_ibrahim_walk_si",
    "abdullah_matroud",
    "abdulmun3im_abdulmubdi2",
    "abdulrazaq_bin_abtan_al_dulaimi",
    "abdulwadood_haneef",
    "abdurrahmaan_as-sudays",
    "abdurrashid_sufi",
    "abdurrashid_sufi_-_khalaf_3an_7amza_recitation",
    "abdurrashid_sufi_abi_al7arith",
    "abdurrashid_sufi_doori",
    "abdurrashid_sufi_shu3ba",
    "abdurrashid_sufi_soosi_2020",
    "abdurrashid_sufi_soosi_rec",
    "abu_bakr_ash-shaatree",
    "abu_bakr_ash-shatri_tarawee7",
    "adel_kalbani",
    "adel_kalbani_1437",
    "ahmad_alhuthayfi",
    "ahmad_nauina",
    "ahmed_ibn_3ali_al-3ajamy",
    "akram_al_alaqmi",
    "alhusaynee_al3azazee_with_children",
    "ali_hajjaj_alsouasi",
    "ali_jaber",
    "asim_abdulaleem",
    "aziz_alili",
    "bandar_baleela",
    "fares",
    "fatih_seferagic",
    "hamad_sinan",
    "husary_muallim",
    "husary_muallim_kids_repeat",
    "huthayfi",
    "huthayfi_qaloon",
    "ibrahim_al_akhdar",
    "idrees_akbar",
    "imad_zuhair_hafez",
    "jibreen",
    "khaalid_al-qahtaanee",
    "khalifah_taniji",
    "khayat",
    "maher_256",
    "mahmood_ali_albana",
    "mahmood_khaleel_al-husaree",
    "mahmood_khaleel_al-husaree_doori",
    "mahmood_khaleel_al-husaree_iza3a",
    "mehysni",
    "minshawi_mujawwad",
    "mohammad_altablawi",
    "mohammad_ismaeel_almuqaddim",
    "mostafa_ismaeel",
    "mu7ammad_7assan",
    "muhaisny_1435",
    "muhammad_abdulkareem",
    "muhammad_alhaidan",
    "muhammad_ayub_and_mikaal_waters",
    "muhammad_ayyoob",
    "muhammad_ayyoob_hq",
    "muhammad_khaleel",
    "muhammad_patel",
    "muhammad_siddeeq_al-minshaawee",
    "mustafa_al3azzawi",
    "nabil_rifa3i",
    "nasser_bin_ali_alqatami",
    "noreen_siddiq",
    "rifai",
    "sa3ood_al-shuraym",
    "sadaqat_ali",
    "sahl_yaaseen",
    "salaah_bukhaatir",
    "salah_alhashim",
    "salahbudair",
    "saleh_al_taleb",
    "shakir_qasami_with_english",
    "sodais_and_shuraim",
    "sudais_and_shuraim_with_urdu",
    "sudais_shuraim_and_english",
    "sudais_shuraim_with_naeem_sultan_pickthall",
    "tawfeeq_bin_saeed-as-sawaaigh",
    "thubaity",
    "wadee_hammadi_al-yamani",
    "yasser_ad-dussary",
]

SURAH_NAME_MAP = {
    "al-faatihah": 1,
    "al-baqarah": 2,
    "aali-imran": 3,
    "an-nisa": 4,
    "al-maaidah": 5,
    "al-anam": 6,
    "al-araf": 7,
    "al-anfal": 8,
    "at-tawbah": 9,
    "yunus": 10,
    "hud": 11,
    "yusuf": 12,
    "ar-rad": 13,
    "ibrahim": 14,
    "al-hijr": 15,
    "an-nahl": 16,
    "al-israa": 17,
    "al-kahf": 18,
    "maryam": 19,
    "ta-ha": 20,
    "al-anbiya": 21,
    "al-hajj": 22,
    "al-muminoon": 23,
    "an-nur": 24,
    "al-furqan": 25,
    "ash-shuara": 26,
    "an-naml": 27,
    "al-qasas": 28,
    "al-ankabut": 29,
    "ar-rum": 30,
    "luqman": 31,
    "as-sajdah": 32,
    "al-ahzab": 33,
    "saba": 34,
    "fatir": 35,
    "ya-sin": 36,
    "as-saffat": 37,
    "saad": 38,
    "az-zumar": 39,
    "ghaafir": 40,
    "fussilat": 41,
    "ash-shura": 42,
    "az-zukhruf": 43,
    "ad-dukhaan": 44,
    "al-jathiyah": 45,
    "al-ahqaaf": 46,
    "muhammad": 47,
    "al-fath": 48,
    "al-hujurat": 49,
    "qaf": 50,
    "adh-dhaariyat": 51,
    "at-tur": 52,
    "an-najm": 53,
    "al-qamar": 54,
    "ar-rahman": 55,
    "al-waqiah": 56,
    "al-hadid": 57,
    "al-mujadilah": 58,
    "al-hashr": 59,
    "al-mumtahanah": 60,
    "as-saff": 61,
    "al-jumah": 62,
    "al-munafiqun": 63,
    "at-taghabun": 64,
    "at-talaq": 65,
    "at-tahrim": 66,
    "al-mulk": 67,
    "al-qalam": 68,
    "al-haqqah": 69,
    "al-maarij": 70,
    "nuh": 71,
    "al-jinn": 72,
    "al-muzzammil": 73,
    "al-muddaththir": 74,
    "al-qiyamah": 75,
    "al-insan": 76,
    "al-mursalat": 77,
    "an-naba": 78,
    "an-naziat": 79,
    "abasa": 80,
    "at-takwir": 81,
    "al-infitar": 82,
    "al-mutaffifin": 83,
    "al-inshiqaq": 84,
    "al-buruj": 85,
    "at-tariq": 86,
    "al-ala": 87,
    "al-ghashiyah": 88,
    "al-fajr": 89,
    "al-balad": 90,
    "ash-shams": 91,
    "al-lail": 92,
    "ad-duha": 93,
    "ash-sharh": 94,
    "at-tin": 95,
    "al-alaq": 96,
    "al-qadr": 97,
    "al-bayyinah": 98,
    "az-zalzalah": 99,
    "al-aadiyat": 100,
    "al-qariah": 101,
    "at-takathur": 102,
    "al-asr": 103,
    "al-humazah": 104,
    "al-fil": 105,
    "quraysh": 106,
    "al-maun": 107,
    "al-kawthar": 108,
    "al-kafiroon": 109,
    "an-nasr": 110,
    "al-masad": 111,
    "al-ikhlas": 112,
    "al-falaq": 113,
    "an-nas": 114,
}


def guess_name(name, names):
    match = difflib.get_close_matches(name.lower(), names, n=1, cutoff=0.6)
    return match[0] if match else None


async def download_surah(session, surah_num, surah_name, reciter_id, output_dir, file_format, retries=3):
    filename = file_format.replace("number", str(surah_num)).replace("name", surah_name.title()) + ".mp3"
    url = f"https://download.quranicaudio.com/quran/{reciter_id}/{surah_num:03}.mp3"
    filepath = os.path.join(output_dir, filename)

    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to download Surah {surah_num}: {response.status}")
                    return
                async with aiofiles.open(filepath, "wb") as f:
                    async for chunk in response.content.iter_chunked(1048576 * 50):
                        await f.write(chunk)
            print(f"Downloaded: {filepath}")
            return
        except asyncio.CancelledError:
            return
        except aiohttp.ClientConnectionError:
            print(f"Network error while downloading Surah {surah_num} (attempt {attempt + 1}/{retries})")
        except Exception as e:
            print(f"Unexpected error while downloading Surah {surah_num} (attempt {attempt + 1}/{retries}): {e}")
        await asyncio.sleep(1)
    print(f"Failed after {retries} attempts: Surah {surah_num}")


async def main(args):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("surah", help="Surah number, name, range (e.g., 2-4), or 'all'")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-f", "--file-name", default="number - name", help="Filename format (no .mp3)")
    parser.add_argument("-r", "--reciter", default="yasser_ad-dussary", help="Reciter name")
    parsed_args = parser.parse_args(args)

    try:
        if parsed_args.surah.lower() == "all":
            surah_items = list(SURAH_NAME_MAP.items())
        elif "-" in parsed_args.surah:
            start, end = map(int, parsed_args.surah.split("-"))
            surah_items = [(name, num) for name, num in SURAH_NAME_MAP.items() if start <= num <= end]
        elif parsed_args.surah.isdigit():
            num = int(parsed_args.surah)
            name = next((n for n, i in SURAH_NAME_MAP.items() if i == num), None)
            if not name:
                print(f"Surah number '{num}' not found.")
                return
            surah_items = [(name, num)]
        else:
            name = guess_name(parsed_args.surah.lower(), SURAH_NAME_MAP.keys())
            if not name:
                print(f"Surah name '{parsed_args.surah}' not found.")
                return
            surah_items = [(name, SURAH_NAME_MAP[name])]

        surah_items.sort(key=lambda x: x[1])
        os.makedirs(parsed_args.output, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(download_surah(session, num, name, parsed_args.reciter, parsed_args.output, parsed_args.file_name))
                for name, num in surah_items
            ]
            await asyncio.gather(*tasks, return_exceptions=True)

    except KeyboardInterrupt:
        print("\n\nDownload interrupted by the user. Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if sys.version_info >= (3, 11):
        try:
            asyncio.run(main(sys.argv[1:]))
        except KeyboardInterrupt:
            print("\n\nDownload interrupted by the user. Exiting...")
    else:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main(sys.argv[1:]))
        except KeyboardInterrupt:
            print("\n\nDownload interrupted by the user. Exiting...")
