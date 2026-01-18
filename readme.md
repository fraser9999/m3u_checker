
---

## 📄 `README.md`

````markdown
# Async M3U / M3U8 Stream Checker

An asynchronous bulk checker for **M3U / M3U8 playlist files** that validates internet streams, detects **geo-blocked URLs**, and outputs cleaned playlists while preserving the original M3U formatting.

Designed for **large IPTV playlists** with thousands of links.

---

## ✨ Features

- ✅ Supports `.m3u` and `.m3u8` playlists
- ⚡ Fully **asynchronous** (high performance, bulk-friendly)
- 📊 **Progress bar** for real-time feedback
- 🌍 **Geo-block detection**
- 🗂️ Separate output files:
  - working streams
  - geo-blocked streams
- 🧾 Preserves original `#EXTINF` metadata
- 🛑 Automatically removes dead / unreachable links

---

## 🌍 Geo-Block Detection Logic

A stream is classified as **geo-blocked** if:

- HTTP status code is `401`, `403`, or `451`
- AND the response body contains keywords like:
  - `geo`
  - `country`
  - `region`
  - `not available`
  - `blocked`

This heuristic works reliably for most IPTV and HLS providers.

---

## 📁 Output Files

| File | Description |
|-----|------------|
| `working_links.m3u` | All reachable, working streams |
| `geoblocked_links.m3u` | Streams blocked by geographic restrictions |
| *(discarded)* | Dead, timed-out, or invalid URLs |

---

## 🚀 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/m3u-async-checker.git
cd m3u-async-checker
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

1. Place your playlist file in the project directory
2. Edit the input filename if necessary:

```python
INPUT_M3U = "input.m3u"
```

3. Run the checker:

```bash
python m3u_checker.py
```

---

## ⚙️ Configuration

You can adjust performance and behavior via constants in the script:

```python
TIMEOUT_SECONDS = 8
MAX_CONCURRENT_REQUESTS = 50
```

| Setting                   | Description              |
| ------------------------- | ------------------------ |
| `TIMEOUT_SECONDS`         | Max wait time per stream |
| `MAX_CONCURRENT_REQUESTS` | Parallel async requests  |

---

## 🖥️ Example Output

```
Checking 2450 streams...
Checking streams:  72%|████████████▋     | 1765/2450 [01:21<00:31, 21.8 links/s]

---- Result ----
OK         : 1380
Geo-Block  : 420
Dead       : 650
```

---

## 🧩 Typical Use Cases

* IPTV playlist cleanup
* Stream availability testing
* Geo-block analysis
* Bulk stream validation
* Playlist maintenance automation

---

## 🔒 Disclaimer

This tool is intended for **educational and testing purposes only**.
The author does **not encourage illegal streaming** or copyright infringement.
Always respect local laws and content provider terms.

---

## 📜 License

MIT License — feel free to use, modify, and contribute.

````

---

## 📦 `requirements.txt`

```txt
aiohttp>=3.8
tqdm>=4.65
````

---



