import os
os.system("cls")

import asyncio
import aiohttp
from pathlib import Path
from tqdm.asyncio import tqdm_asyncio


from datetime import datetime
from random import randrange
import re

# ------------------ Konfiguration ------------------



dir_path = os.path.dirname(os.path.realpath(__file__))



TIMEOUT_SECONDS = 8
MAX_CONCURRENT_REQUESTS = 50

GEO_STATUS_CODES = {401, 403, 451}
GEO_KEYWORDS = (
    "geo", "country", "region",
    "not available", "blocked",
    "unavailable in your"
)

# ---------------------------------------------------

async def check_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=TIMEOUT_SECONDS),
                allow_redirects=True
            ) as response:

                if response.status in GEO_STATUS_CODES:
                    try:
                        text = (await response.text()).lower()
                        if any(k in text for k in GEO_KEYWORDS):
                            return "GEO"
                    except Exception:
                        return "GEO"

                if response.status < 400:
                    return "OK"

                return "DEAD"

        except Exception:
            return "DEAD"


def parse_m3u(lines):
    blocks = []
    meta_buffer = []

    for line in lines:
        line = line.rstrip("\n")
        if not line:
            continue

        if line.startswith("#"):
            meta_buffer.append(line)
        else:
            blocks.append((meta_buffer.copy(), line))
            meta_buffer.clear()

    return blocks


async def process_m3u(input_file):
    lines = Path(input_file).read_text(
        encoding="utf-8", errors="ignore"
    ).splitlines()

    blocks = parse_m3u(lines)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession(
        headers={"User-Agent": "M3U-Checker/1.2"}
    ) as session:

        tasks = [
            check_url(session, url, semaphore)
            for _, url in blocks
        ]

        print(f"Prüfe {len(tasks)} Links …")

        # 🔥 Fortschrittsbalken hier
        results = await tqdm_asyncio.gather(
            *tasks,
            desc="Überprüfe Streams",
            unit="link"
        )

    ok_count = geo_count = dead_count = 0

    with open(OUTPUT_OK, "w", encoding="utf-8") as ok_f, \
         open(OUTPUT_GEO, "w", encoding="utf-8") as geo_f:

        ok_f.write("#EXTM3U\n")
        geo_f.write("#EXTM3U\n")

        for (meta, url), result in zip(blocks, results):

            target = None

            if result == "OK":
                ok_count += 1
                target = ok_f
            elif result == "GEO":
                geo_count += 1
                target = geo_f
            else:
                dead_count += 1

            if target:
                for m in meta:
                    target.write(m + "\n")
                target.write(url + "\n")

    print("\n---- Ergebnis ----")
    print(f"OK         : {ok_count}")
    print(f"Geo-Block  : {geo_count}")
    print(f"Tot/Fehler: {dead_count}")




if __name__ == "__main__":


    newpath = dir_path + "/" + "proofed_m3u" 
    if not os.path.exists(newpath):
        os.makedirs(newpath)


    while True:

        os.system("cls")

        print("M3U Link Checker ")

        print("\n\n")

        inp=input("M3U Liste ")
        if inp=="" or inp==None:
            print("no m3u found")
            a=input("wait key")
            exit

        inp=inp.replace('"',"")

        #INPUT_M3U  = "input.m3u"
        INPUT_M3U = inp

        # get file text clean
        name=os.path.splitext(inp)[0]  
        name=os.path.basename(name)
        clean = re.sub("[^A-Za-z0-9]", "", name)
        #print(clean)

        # set file date
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")

        

        
        OUTPUT_OK  = newpath + "/" + dt_string + "_" + clean + "_working_links.m3u"
        OUTPUT_GEO = newpath + "/" + dt_string + "_" + clean + "_geoblocked_links.m3u"


        asyncio.run(process_m3u(INPUT_M3U))

        a=input("wait key")
