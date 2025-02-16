# Smart-Shopping-List
# Smart Shopping List

Smart Shopping List is an interactive web application built with Python and [Streamlit](https://streamlit.io/) that helps users to:
- **Search for Groceries:** Find out which store offers your selected groceries at the best price.
- **Find Ingredients for a Dish:** Enter the name of a dish and get an AI-generated list of necessary ingredients.

## Project Structure

The repository is organized into several modules:

- **`app.py`**  
  The main application file which includes:
  - Streamlit configuration (e.g., page title and icon).
  - A sidebar menu for navigating between:
    - "Search for Groceries"
    - "Find Ingredients for a Dish"
    - "Search History"
    - "Summary"
  - Calls to functions from other modules to handle user input, fetch real-time price data, and communicate with AI APIs.

- **`real_time_price_scraper.py`**  
  Contains functions to:
  - `get_results_dictionary(grocery_list)`: Fetch data from a CSV file and scrape current prices from various websites.
  - `get_prices(results)`: Extract the lowest and highest prices from the scraped data.
  - `get_output_string(results)`: Generate a formatted shopping list with price comparisons and calculated savings.

- **`df_converter.py`**  
  Provides utility functions for handling CSV data:
  - Reads a CSV file (e.g., `food_data.csv`) and returns lists of product names, prices, and URL links via `get_food_list()`.

- **`llm_api.py`**  
  Manages interactions with AI APIs:
  - `get_grok_api_key()` and `get_gemini_api_key()`: Read the respective API keys from local files
  - `client_configuration(api_key)`: Configures the AI client.
  - `get_grok_response(client, food)` and `get_gemini_response(food)`: Send a request to the AI models (Grok or Gemini) and return a list of ingredients for the given dish.

- **`scraper.py`** (or the file containing the scraping logic)  
  Contains functions to:
  - Scrape the website [akcniceny.cz](https://www.akcniceny.cz/) to collect product names, prices, and URL links.
  - Save the scraped data into a CSV file (e.g., `results.csv`), which is then used by `df_converter.py`.

- **CSV Data Files**  
  - **`food_data.csv`** / **`results.csv`**: CSV files that contain product data with the following columns:
    - `Název` (Name)
    - `Cena` (Price)
    - `Url odkaz` (URL Link)
