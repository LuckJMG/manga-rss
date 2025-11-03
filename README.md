# Manga RSS Tracker

Automated system to generate RSS feeds for manga sites that don't provide their own feeds. Uses GitHub Actions for periodic scraping and GitHub Pages to host the generated RSS feeds.

## Features

- Automated scraping of multiple manga sites
- Individual RSS feed generation per manga
- Daily scheduled execution via GitHub Actions
- Free feed hosting on GitHub Pages
- Flexible per-site configuration (customizable CSS selectors)
- Customizable weekly schedule per manga

## Project Structure

```
manga-rss-tracker/
├── .github/
│   └── workflows/
│       └── update-feeds.yml    # GitHub Action for automation
├── main.py                     # Main scraping script
├── feeds/                      # Directory with generated RSS feeds
│   ├── blue-lock.xml
│   ├── infinite-mage.xml
│   └── ...
└── README.md
```

## Requirements

- GitHub account
- Python 3.11+
- Dependencies:
  - `feedgenerator`
  - `requests`
  - `beautifulsoup4`

## Initial Setup

### 1. Clone or create the repository

```bash
git clone https://github.com/your-username/manga-rss-tracker.git
cd manga-rss-tracker
```

### 2. Create branch for feeds

```bash
git checkout -b github-pages
git push -u origin github-pages
git checkout main
```

### 3. Configure GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Select **github-pages** branch and **/ (root)** folder
4. Save changes

### 4. Enable write permissions for GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Save changes

## Manga Configuration

Edit `main.py` and add your manga to the `MANGA_PAGES` list:

```python
MANGA_PAGES = [
    MangaPage(
        name="file-name",                # XML file name (without extension)
        url="https://site.com/manga",    # Manga page URL
        title="Manga Title",             # Title for RSS feed
        schedule=2,                      # Day of week (0=Monday, 6=Sunday)
        list_select=".chapter-item",     # CSS selector for chapter list
        title_select=".chapter-title",   # CSS selector for chapter title
        skip_first=False                 # Optional: skip first element
    ),
]
```

## Usage

### Local Execution (Testing)

```bash
# Install dependencies
pip install feedgenerator requests beautifulsoup4

# Run scraper
python main.py
```

### Automated Execution

The GitHub Action runs automatically every day at 8:00 AM UTC. You can also run it manually:

1. Go to the **Actions** tab on GitHub
2. Select **Update RSS Feeds**
3. Click **Run workflow**

## Subscribe to Feeds

Your RSS feed URLs will be available at:

```
https://your-username.github.io/repo-name/feeds/file-name.xml
```

## How to Find CSS Selectors

1. Open the manga page in your browser
2. Right-click on a chapter element → **Inspect**
3. Identify the CSS classes that contain:
   - The complete chapter list (`list_select`)
   - Each chapter's title (`title_select`)

**Example:**
```html
<div class="chapter-list">
  <div class="chapter-item">
    <a href="/chapter-1">
      <span class="chapter-title">Chapter 1</span>
    </a>
  </div>
</div>
```

Selectors:
- `list_select`: `.chapter-item`
- `title_select`: `.chapter-title`

## Respecting robots.txt

Before adding a site, check its `robots.txt`:

```
https://site.com/robots.txt
```

The script respects scraping policies and executes requests with a 10-second timeout.

## Limitations

- Only works with sites that don't require JavaScript to load chapters
- Doesn't work with sites requiring authentication
- GitHub Actions limits: 2000 minutes/month (free plan)

## License

This project is open source. Use it responsibly and respect the terms of service of the sites you scrape.

