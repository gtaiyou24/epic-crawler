# Epic Crawler
汎用型Webクローラー

## How to

<details><summary>docker-composeの起動</summary>

```bash
# at local

$ docker-compose up --build
```
</details>

<details><summary>クローリングバッチの実行</summary>

```bash
$ docker-compose run --rm crawler python start_crawling.py 

# ZARA
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://www.zara.com/jp/ja/woman-must-have-l4108.html?v1=1233942" \
  "https://www\.zara\.com/jp/ja/[\S-]+-p[0-9]+\.html"

# DHOLIC
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://m.dholic.co.jp/product/favorite_ranking_list.asp?site=F" \
  "https://m\.dholic\.co\.jp/product/goodview_item\.asp\?gserial=[0-9]+" \
  "#list_more_bt"

# SNIDEL
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://snidel.com/Form/Product/ProductList.aspx?shop=0&cat=&pgi=&cicon=&dosp=&dpcnt=-1&img=1&disp=pro&max=&min=&sort=16&swrd=&udns=2&fpfl=0&cid=&bid=SND01&rrlt=&_color=&_size=&_type=&pno=1&pslid=&pslkbn=" \
  "https://snidel\.com/Form/Product/ProductDetail\.aspx\?.+" \
  "#productsListArea > div.block-pager.pager > a:nth-last-child(1)"

# GRL
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://www.grail.bz/disp/itemlist/?sk=01&d=0&pp=150&pmin=0&pmax=10000" \
  "https://www\.grail\.bz/item/[0-9a-zA-Z]+/" \
  "body > div.wrapper > main > div.contents-main-upper > div > div.box-pagination-01 > ul > li > a.btn-next"

# Calvin Klein
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://japan.calvinklein.com/shop/itemList?shopCode=WOMENS,UNISEX&largeCategoryCode=TS,TP,HT,KN,OW,OP,SK,JS,BT,SP,SW" \
  "https://japan\.calvinklein\.com/shop/item/[0-9a-zA-Z]+" \
  "#martha-app > div.lSticky > main > div > div > div.search > div.main > div.product > div > div.product-pagination > div > ul.product-pagination-next > li > a"

# ROYAL PARTY
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://roomys-webstore.jp/ap/s/s?fq=bd:RW040&fq=scls:n_usual&rows=120&sort=salesCD+desc,fsdt+desc" \
  "https://roomys-webstore\.jp/ap/item/i/[0-9A-Z]+\?aid4=[0-9]+" \
  "#main > div:nth-child(4) > div > ol > li.next > a"

# LIP SERVICE
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://atomicboxx.com/ap/s/s?fq=scls:n_*&fq=bd:AB000&rows=120&sort=rk+desc%2Cfsdt+desc" \
  "https://atomicboxx\.com/ap/item/i/[0-9A-Z]+" \
  "#search_result > ol > li.pager_next > a"
  
# apres jour
docker-compose run --rm crawler python start_crawling.py scroll \
  "https://zozo.jp/sp/women-shop/apresjour/?displaycolor=1" \
  "https://zozo\.jp/sp/shop/apresjour/goods/[0-9]+/.*" \
  "#fastLoad > div.c-pager > a"
```
</details>

<details><summary>テストコードの実行方法</summary>

```bash
$ pytest -v src/
```
</details>
