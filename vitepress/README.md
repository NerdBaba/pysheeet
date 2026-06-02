# Pysheeet (VitePress)

Personal-use VitePress build of the pysheeet Python cheat sheets.

## Run locally

```bash
cd vitepress
npm install
npm run dev
```

Then open the URL VitePress prints (usually `http://localhost:5173`).

## Build for production

```bash
npm run build
npm run preview
```

## Regenerate from source

From the project root:

```bash
./convert.sh docs/notes vitepress
python3 cleanup.py vitepress
python3 gen-config.py vitepress
```

The source `.rst` files in `docs/notes/` are the source of truth and are not
modified by these scripts.
