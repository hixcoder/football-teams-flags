# ⚽ Football Teams Flags

A comprehensive collection of football (soccer) team logos, names, and country information scraped from [football-logos.cc](https://football-logos.cc/). This project includes a Python scraper and a JSON dataset containing thousands of football teams from around the world.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Example Data](#example-data)
- [Statistics](#statistics)
- [Requirements](#requirements)
- [Notes](#notes)

## ✨ Features

- **Comprehensive Dataset**: Contains thousands of football teams from multiple countries
- **Rich Metadata**: Each team entry includes:
  - Team name
  - Country name
  - Country flag emoji
  - High-quality logo URL (256x256px)
- **Automated Scraping**: Python script automatically collects data from multiple country pages
- **Deduplication**: Prevents duplicate entries during scraping
- **JSON Format**: Easy to integrate with any application or framework

## 📁 Project Structure

```
football-teams-flags/
├── scrape_football_logos.py    # Python scraper script
├── football_teams.json         # Generated JSON dataset
└── README.md                   # This file
```

## 🚀 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd football-teams-flags
```

2. Install required Python packages:
```bash
pip install requests beautifulsoup4
```

## 💻 Usage

### Running the Scraper

To scrape and update the football teams data:

```bash
python scrape_football_logos.py
```

The script will:
1. Scrape the main page of football-logos.cc
2. Discover all country-specific pages
3. Extract team information from each page
4. Handle pagination automatically
5. Save the data to `football_teams.json`

**Note**: The scraper includes polite delays between requests to avoid overloading the server.

### Using the JSON Data

The `football_teams.json` file can be directly imported into your application:

```python
import json

with open('football_teams.json', 'r', encoding='utf-8') as f:
    teams = json.load(f)

# Example: Find all teams from a specific country
england_teams = [team for team in teams if team['country'] == 'England']
print(f"Found {len(england_teams)} teams from England")
```

```javascript
// JavaScript/Node.js example
const teams = require('./football_teams.json');

// Find teams by country
const spainTeams = teams.filter(team => team.country === 'Spain');
console.log(`Found ${spainTeams.length} teams from Spain`);
```

## 📊 Data Format

Each team entry in the JSON file follows this structure:

```json
{
  "name": "Team Name",
  "country": "Country Name",
  "flagEmoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
  "logoUrl": "https://assets.football-logos.cc/logos/country/256x256/team-name.hash.png"
}
```

### Field Descriptions

- **`name`**: The official or common name of the football team
- **`country`**: The country where the team is based
- **`flagEmoji`**: Unicode flag emoji representing the team's country
- **`logoUrl`**: Direct URL to the team's logo image (256x256 pixels)

## 📝 Example Data

```json
[
  {
    "name": "Liverpool FC",
    "country": "England",
    "flagEmoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "logoUrl": "https://assets.football-logos.cc/logos/england/256x256/liverpool.99c48ae3.png"
  },
  {
    "name": "Real Madrid",
    "country": "Spain",
    "flagEmoji": "🇪🇸",
    "logoUrl": "https://assets.football-logos.cc/logos/spain/256x256/real-madrid.5ce15611.png"
  },
  {
    "name": "Paris Saint-Germain",
    "country": "France",
    "flagEmoji": "🇫🇷",
    "logoUrl": "https://assets.football-logos.cc/logos/france/256x256/paris-saint-germain.579907dc.png"
  }
]
```

## 📈 Statistics

The dataset includes:
- **Thousands of teams** from multiple countries
- **Coverage** of major football leagues worldwide
- **High-quality logos** in 256x256 pixel resolution
- **Country flag emojis** for easy visual identification

## 📦 Requirements

- Python 3.6+
- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing

Install all requirements:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4
```

## ⚠️ Notes

- **Respectful Scraping**: The scraper includes delays between requests to be respectful to the source website
- **Data Source**: All data is scraped from [football-logos.cc](https://football-logos.cc/)
- **Logo URLs**: Logo URLs point directly to the CDN and should remain stable, but may change over time
- **Updates**: Run the scraper periodically to keep the dataset up-to-date with new teams
- **Flutter Integration**: This dataset is designed for use in Flutter applications, but can be used with any framework or language

## 🤝 Contributing

Contributions are welcome! If you find any issues or want to improve the scraper:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is provided as-is. Please respect the terms of service of the source website (football-logos.cc) when using this scraper.

---

**Made with ⚽ for football fans and developers**
