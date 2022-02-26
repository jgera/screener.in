# screener.in scraper 
 Web Scraper for screener.in for getting fundamental deta provided in the excel file

To run the scraper just execute, by default it will download few symbols TCS, INFY and WIPRO  
```python
python scraper.py 
```
![scraper](https://raw.githubusercontent.com/jgera/screener.in/main/images/1.png)

You can specify the symboles in a file for expample and path to download the report files as  
```python
python scraper.py -s nifty50.txt -p reports
```
you'll need to change the cookies in the header and post data specified in the scraper.py to make it work.  
![cookies](https://raw.githubusercontent.com/jgera/screener.in/main/images/1.PNG)

This information can be collected from chrome developer tools.
![dev tools](https://raw.githubusercontent.com/jgera/screener.in/main/images/3.PNG)

