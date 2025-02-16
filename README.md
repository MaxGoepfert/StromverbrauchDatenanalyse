# Ein prädiktives Modell im Kontext des deutschen Stromverbrauchs

## Projektbeschreibung
Dieses Projekt befasst sich mit der Vorhersage des deutschen Stromverbrauchs mithilfe eines Machine Learning Modells. Wir haben Daten der **Bundesnetzagentur (SMARD)** und des **Deutschen Wetter Dienstes (DWD)** für den Zeitraum von **2017 bis 2024** verwendet.

### Analyse-Schritte:
1. **Deskriptive Analyse**: 
   - Untersuchung des Stromverbrauchs auf Tagesbasis für Deutschland, TransnetBW und 50Hertz.
   - Visualisierung und statistische Auswertung der Verbrauchsdaten.
   - Diese Analyse findet man unter dem Ordener Vorhersage/Analysis_Archive und kann aus dem Projektverzeichnis gestartet werden mit: python Vorhersage/Analysis_Archive/bestimmte_datei.py

2. **Prädiktive Analyse**:
   - Entwicklung eines Vorhersagemodells mit **XGBoost** zur Prognose des Stromverbrauchs.
   - Vorhersagen können für Deutschland, TransNetBW oder 50Hertz getroffen werden.
   - Der Vorhersagehorizont kann ausgewählt werden: ein Tag ("Day-Ahead" Vorhersagen) oder ein Kalenderjahr ("Rolling Window" Ansatz)

# Voraussetzungen

Das Projekt wurde in **Python 3.11** entwickelt. Andere Python-Versionen können geringfügige Einflüsse auf die Ergebnisse haben. Falls eine andere Python-Version verwendet wird, können einige Bibliotheken möglicherweise nicht kompatibel sein oder das Verhalten von Funktionen kann leicht variieren. Es wird daher empfohlen, Python 3.11/3.12 oder eine möglichst ähnliche Version zu nutzen.

Die benötigten Bibliotheken können mit den folgenden Schritten installiert werden.

---

## Installationsoptionen

Es gibt zwei Möglichkeiten, das Projekt zu installieren:

- **Option 1:** Verwendung einer virtuellen Umgebung (empfohlen)
- **Option 2:** Installation ohne virtuelle Umgebung

---

## Option 1: Installation der virtuellen Umgebung

### 1. Repository klonen

```sh
git clone <repository-url>
cd <projektverzeichnis>
```

### 2. Virtual Environment erstellen

**Windows:**

```sh
python -m venv venv
```

**Mac/Linux:**

```sh
python3 -m venv venv
```

### 3. Virtual Environment aktivieren

**Windows (CMD):**

```sh
venv\Scripts\activate
```

**Windows (PowerShell):**

```sh
venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```sh
source venv/bin/activate
```

### 4. Abhängigkeiten installieren

```sh
pip install -r requirements.txt
```

### 5. Projekt starten

Nach der Installation kann das Projekt ausgeführt werden (falls ein Hauptskript vorhanden ist, z. B. `main.py`):

```sh
python main.py
```

---

## Option 2: Installation ohne Virtual Environment

Falls keine virtuelle Umgebung verwendet wird, können die benötigten Bibliotheken direkt installiert werden:

```sh
pip install pandas numpy seaborn holidays matplotlib scikit-learn xgboost
```

### Datenquelle
Die verwendeten Daten stammen aus den folgenden Quellen:
- **SMARD** (Strommarktdaten) - [Downloadlink](https://www.smard.de/home/downloadcenter/download-marktdaten/)
- **Deutscher Wetter Dienst(DWD)** - [Downloadlink](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/)
- Details zu benutzten Wetterstationen können im Ordner StromverbrauchDatenanalyse/Vorhersage/Wetterdaten/meta_wetterdaten.txt gefunden werden.


### Nutzung
Nach der Installation der benötigten Bibliotheken kann das Modell mit den vorhandenen Daten trainiert und zur Vorhersage genutzt werden. Es werden zwei Benutzereingaben erwartet:
1. Regelzone auswählen: [DE / TransNetBW / 50Hertz] für Deutschland, TransNetBW oder 50Hertz
2. Vorhersagehorizont auswählen: [J / beliebige Taste] für "J" Day-Ahead Vorhersagen oder "beliebige andere Taste" für Vorhersagehorizont von einem Kalenderjahr

- Notiz: Für zusätzliche Analysen der Wetterdaten und Feiertags-Anomalien befindet sich eine auskommentierte Funktion:
features.feature_engineering(dataset, zone) (Zeile 156) im Code. 


## Lizenz
Dieses Projekt steht unter der **Creative Commons Namensnennung 4.0 International Lizenz**.
