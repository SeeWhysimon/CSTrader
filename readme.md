# CSTrader

## Introduction

Preview:

![k-line example](figs/kline.png)
![pred example](figs/pred.png)


## How to use

First of all, you need to fill config files. 
Open any colletor directory under `scripts/data_collector/` and create `.json` file respectively.
For example, if you want to collect data from BUFF, you should direct to `scripts/data_collector/buff` and create `buff_config.json`. Then, fill your `buff_config.json` by following the template `example_config.json`. The most important part of your json file is the cookie. To fill it, you should do as follows:

1. Direct to referer page in your web browser and press F12(Inspect Elements).
2. Open the network tab and filter XHR/Fetch files(If you don't see any files, refresh the website).
3. Select `bill_order`(or any target file you are interested in) and select Cookie tab.
4. Notice the Request Cookie, use the value and fill your json file respectively.

![example](figs/example.png)

```
pip install -r requirements.txt
python main.py
```


## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
