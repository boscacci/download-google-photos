# Download Google Photos Album

A way to download lots of google photos from your album(s).

I needed a way to download 2k+ photos from my shared google photos album.

<img 
	src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F1000marcas.net%2Fwp-content%2Fuploads%2F2021%2F05%2FGoogle-Photos-logo-720x720.png&f=1&nofb=1&ipt=77e29e8b8ee41eb9b211e055eec6ff6f1eeb11830c1664b1763713285250d14c&ipo=images" height = 150>

## Steps
1. Log into Google Cloud Console.
2. Create a project with google photos access.
3. Create OAuth **credentials** (client_secret.json).
4. Use the credentials to get a **bearer token**. (This can actually be done by running the .py script here with a bogus album ID)
5. Use the **bearer token** with the bash script in here to find the **album ID(s)**.
6. Use `download_google_photos.py` to get your photos.