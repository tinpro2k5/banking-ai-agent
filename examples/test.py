import json

import requests


def main() -> None:
    with open("sample_requests.json", "r", encoding="utf-8") as infile:
        msgs = json.load(infile)

    with open("results.txt", "w", encoding="utf-8") as outfile:
        for m in msgs:
            message = m.get("message", "")
            try:
                response = requests.post("http://localhost:6636/chat", json=m, timeout=60)
            except requests.RequestException as exc:
                line = f"{message} -> REQUEST_ERROR: {exc}"
                print(line)
                outfile.write(line + "\n")
                continue

            try:
                payload = response.json()
                line = f"{message} -> {json.dumps(payload, ensure_ascii=False)}"
            except ValueError:
                # Show raw body when server does not return JSON (e.g., HTML 500 page)
                body = response.text.strip().replace("\n", " ")
                line = f"{message} -> HTTP {response.status_code}: {body}"

            print(line)
            outfile.write(line + "\n")


if __name__ == "__main__":
    main()