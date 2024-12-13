# Topic of your semestral work

Streamlit grafické rozhranie pre často používané funkcionality OpenCV, pre demonštračné účely/pochopenie zákl. konceptov
Každý krok bude vizualizovaný, popr. ak posuniem so sliderom/zmením nejaký parameter, obraz sa hneď aktualizuje, aby som
videl čo to s ním robí. Pointa aplikácie je zjednodušiť základy spracovania obrazu, keďže hneď sa pustiť do
programovania v notebooku môže byť náročné.

StreamLit aplikace umožní:

1. Načítať obrázok
2. Predspracovanie
    - Úprava jasu, kontrastu, gamma (3 sliders)
    - Ekvalizace histogramu
    - Morfologické operace
        - Opening, closing
    - aplikovať filtry (možnosť vybrať veľkosť kernelu pri konvolučných filtroch)
        - gaussianBlur
        - median filter
        - Box filter (average)
        - laplace
3. Segmentace obrazu
    - Hranová
        - Canny
        - Laplacian
        - Prewitt
        - A možno ďaľšie
    - Prahovanie double thresholding
        - Pre barevny obrazek 3 sliders, pre HSV slozky.
        - Po každej zmene sa mi obrázok aktualizuje
4. Hľadanie kontúr a ich následná vizualizácia (vyźaduje binárny obraz)
5. Homography (napr. ak sa jedná o fotografiu papieru, chcem snímok skosiť tak, aby boli jeho okraje na okrajoch obrazu)
    - Vyberiem 4 body na obrázku
      Zadám 4 súradnice, na kt. sa majú namapovať (v prípade A4 papieru napr. jeho rozmery)

Požiadavka od cvičiaceho: ak mám viacej spracovaní obrazu za sebou, umožniť úpravu aj predošlých filtrov, nielen
posledného.

# How to run project

`Open ImageProcessor directory`

`$ python3.11 -m venv .env`

`$ source .env/bin/activate`

`$ pip install -r requirements.txt`

`$ python3.11 -m streamlit run src/main.py`

# How to test from ImageProcessor directory

`Open ImageProcessor directory`

`$ pytest`