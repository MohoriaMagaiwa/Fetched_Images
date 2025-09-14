import requests
import os
import hashlib
from urllib.parse import urlparse

def get_filename_from_url(url):
    """Extracts a clean filename from the URL or generates one."""
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    if not name or "." not in name:
        name = f"image_{hashlib.md5(url.encode()).hexdigest()[:8]}.jpg"
    return name

def is_duplicate(content, folder):
    """Checks if an image is already downloaded by comparing file hashes."""
    new_hash = hashlib.md5(content).hexdigest()
    for file in os.listdir(folder):
        existing_path = os.path.join(folder, file)
        with open(existing_path, 'rb') as f:
            if hashlib.md5(f.read()).hexdigest() == new_hash:
                return True
    return False

def main():
    print("🌍 Welcome to the Ubuntu Image Gatherer")
    print("💛 I am because we share — Collecting community images mindfully\n")

    # Get multiple URLs from user
    urls = input("🔗 Enter image URLs (separated by commas): ").split(",")

    # Prepare directory
    os.makedirs("Fetched_Images", exist_ok=True)

    headers = {
        "User-Agent": "UbuntuFetcher/1.0 (Respectful Bot)"
    }

    for raw_url in urls:
        url = raw_url.strip()
        if not url:
            continue

        print(f"\n📡 Connecting to: {url}")

        try:
            # Fetch with timeout and respectful headers
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Validate content type
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"⚠️ Skipped: Not an image (Content-Type: {content_type})")
                continue

            # Avoid duplicates
            if is_duplicate(response.content, "Fetched_Images"):
                print("♻️ Already in community collection — skipping duplicate.")
                continue

            filename = get_filename_from_url(url)
            filepath = os.path.join("Fetched_Images", filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ Successfully fetched and saved: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    print("\n🤝 Connection strengthened. Community enriched. 🌱")

if __name__ == "__main__":
    main()
