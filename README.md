Sure, here's the documentation for the `News-api` in a structured format:

---

# News-api

## Overview
The `News-api` is a Django RESTful API designed to scrape homepage headlines from news websites such as Aaj Tak and NDTV. It stores the scraped news headlines in a database and provides endpoints to fetch the latest headlines and post new news articles.

## Endpoints
- `GET /aajtak/`: Fetches the latest headlines from Aaj Tak.
- `GET /ndtv/`: Fetches the latest headlines from NDTV.
- `POST /post/`: Allows posting of a new news article to the database.

## Models
### News
The `News` model stores news articles with the following fields:
- `heading`: The headline of the news article.
- `subheading`: The sub-heading of the news article.
- `article`: The main content of the news article.

## Installation and Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/Tanish0907/everything_api.git
    cd everything_api
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations and start the server**:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Usage

### GET /aajtak/
Fetches the latest headlines from Aaj Tak.

**Response**:
```json
{
  "Breaking_news": [
    "Breaking News Headline 1",
    "Breaking News Headline 2",
    ...
  ],
  "news": [
    {
      "heading": "News Heading 1",
      "subheading": "Subheading 1",
      "article": ["Paragraph 1", "Paragraph 2", ...]
    },
    ...
  ]
}
```

### GET /ndtv/
Fetches the latest headlines from NDTV.

**Response**:
```json
{
  "news": [
    {
      "heading": "News Heading 1",
      "subheading": "Subheading 1",
      "article": ["Paragraph 1", "Paragraph 2", ...]
    },
    ...
  ]
}
```

### POST /post/
Allows posting of a new news article to the database.

**Request Body**:
```json
{
  "heading": "New News Heading",
  "subheading": "New Subheading",
  "article": "New Article Content"
}
```

**Response**:
```json
{
  "status": "object created"
}
```

## Implementation
The API uses the BeautifulSoup library to scrape news headlines from the Aaj Tak and NDTV websites. The scraped data is then saved into the Django models and can be retrieved via the provided endpoints.

## Note
Ensure you have the necessary dependencies installed, and your Django project is correctly set up to use the API. Refer to the Installation and Setup section for more details.

---
