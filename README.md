# Otomoto Deal Scraper
Find the best value to price car based on set car filters to speed up finding the best deal for your dream car

# How it works
The program searches all possible offers based on the filters you have set and finds the best car based on its:

* Mileage
* Price
* Year of production (the newer the better)
* Type of fuel it uses (right now it's diesel > gasoline > gasoline+lpg > lpg, you can't change this yet sorry)
* Horse power

Every of the following properties will determine the amount of points the car gets (the more the better)

## [!] NOTE: This program might not always find the best offer, for example a car with parts swapped and with higher actual value might be still ranked low as there is no way to differentiate between them from the amount of data that is collected during scraping, use this program as a tool to help you find the best deal, but always do your own research and verify the information before making a purchase.

# Installation
<b>Requirements:</b> 

- <b>Python3 or greater</b>

1. Download the repository as zip or clone it using git
    ```bash
    git clone https://github.com/maacnt/otomoto_deal_scraper.git
    ```

<b>In the working directory of the project:</b>

2. Create a python virtual environment
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment
    ```bash
    source venv/bin/activate    # For Linux/macOS
    .\\venv\\Scripts\\activate  # For Windows
    ```

NOTE: The commands may vary depending on your shell, operating system, and Python installation.

4. Install all dependencies from requirements.txt
    ```bash
    pip install -r requirements.txt
    ```

# Usage

1. Go into <a href="https://www.otomoto.pl/osobowe?search%5Border%5D=relevance_web&search%5Badvanced_search_expanded%5D=true">otomoto expanded search options</a>

2. Set your filters on the website 
3. Copy the link with the filters already set

    <b>NOTE: Car's brand and car's models are <i>VERY HEAVILY</i> recommended</b> as to narrow down the search results.

    The following settings are optional and will default to set settings if not set:

    * Minimum price (0)
    * Maximum price (35 000) 
    * Minimum year (1998)
    * Maximum year (2025)      

    <b>If these settings will not be set, the program will still search for every car but cars not in the default range will be ranked lower.</b>


<b>In the working directory of the project:</b>

4. Run the python main.py file
```bash
python3 main.py
```

5. Paste the link into the terminal with the set filters 

The program after completing the scraping process will create a <b>output.csv</b> file with all the cars in the current directory.

<b> If the filter for undamaged/damaged cars was not set, the program will mark them in output.csv file with a "[D]! in front of the title offer"</b>

<b>NOTE:</b> The output file will be overwritten each time the program is run. Create copies if you want to keep the results.





# Misc.

I am going to keep updating this every so often when i see that it got broken

You can set a static link in shared.py at line 9 file in case of needing to run the program multiple times

If the website would change its structure the program will <i>likely break</i>. i will try to maintain the code as long as i will need this program

In the CSV file there are blank characters in mileage and price columns, this is normal and expected behavior. I do that to avoid weird formatting issues in spreadsheet applications. (tested only in onlyoffice, no idea how it looks like in other applications)

There is also a chance that some of the data may be missing or incomplete, this is due to the nature of web scraping and the way the data is presented on the website.

There is no way currently to see the new offers made from last scrape, i will try to implement this feature in the future.

in shared.py file there are settings for debugging for anyone intrested on expanding on the code

The program doesn't use any API requests to the website as that would require an API token to be created and used and it would require a lot more of work to set up. I might add that as an optional feature in the future.

# Contribution

<b>THIS PROJECT IS WORK IN PROGRESS!</b>

If you find any bugs or have any suggestions feel free to open an issue or a pull request, i will try to address them as soon as possible.
I know that this code isn't perfect and there is always room for improvement, as i've made it originally for my own needs and it may not cover all use cases. so all contributions are welcome.

If you want to contribute to the project, please fork the repository and create a new branch for your feature or bug fix. Then, create a pull request and i will try to review it as soon as possible.
