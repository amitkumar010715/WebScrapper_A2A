# WebScrapper_A2A

An AI-powered web scraper built with AutoGen's Agent-to-Agent (A2A) communication framework. This service uses OpenAI's GPT-4o-mini model to intelligently scrape and process web content.

## Features

- **AI-Powered Web Scraping**: Uses OpenAI's GPT-4o-mini model to intelligently interpret and extract web content
- **Agent-to-Agent Communication**: Built on AutoGen's A2A framework for advanced agent interactions
- **FastAPI Server**: RESTful API for easy integration
- **Environment Configuration**: Supports API key management via environment variables
- **Asynchronous Processing**: Built with uvicorn for high-performance serving

## Prerequisites

- Python 3.8+
- OpenAI API Key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/amitkumar010715/WebScrapper_A2A.git
cd WebScrapper_A2A
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. Make sure your `OPENAI_API_KEY` is set. You can get one from [OpenAI's website](https://platform.openai.com/api-keys).

## Usage

### Local Development

Start the server:
```bash
uvicorn server:server --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Deployment

### Deploy on Render

This project includes a `render.yaml` configuration file for easy deployment to Render.

1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Create a new "Web Service"
4. Select your repository and the `main` branch
5. Render will auto-detect the `render.yaml` configuration
6. Add environment variables in Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
7. Deploy!

**Note**: Set `OPENAI_API_KEY` manually in the Render dashboard under Settings → Environment Variables for security.

## Project Structure

```
.
├── server.py           # Main FastAPI application and A2A agent server
├── client.py           # Client utilities for interacting with the server
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── .env               # Environment variables (local development)
└── README.md          # This file
```

## Dependencies

- **pyautogen**: AutoGen framework for agent development
- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **python-dotenv**: Load environment variables from .env file
- **requests**: HTTP library for web requests
- **openai**: OpenAI API client
- **ag2[a2a]**: AutoGen A2A communication framework
- **bs4**: BeautifulSoup for web scraping
- **google-generativeai**: Google Generative AI integration (optional)

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue or submit a pull request on GitHub.
