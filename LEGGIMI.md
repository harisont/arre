# Arré
 
## Prerequisiti
- Python 3.12 e le librerie elencate nel file [requirements.txt](requirements.txt)
- il programma esterno [mpv](https://mpv.io/installation/) (necessario per [scaricare le tracce audio da Radio Radicale](#1-scaricare-una-traccia-audio-da-radio-radicale))
- un programma per l'editing di sottotitoli in formato SRT, ad esempio [Subtitle Composer](https://subtitlecomposer.kde.org/) (Linux e Windows)

## Istruzioni per l'uso

### 1. Scaricare una traccia audio da Radio Radicale
1. individuare la pagina di [radioradicale.it](radioradicale.it) su cui é possibile ascoltare la traccia audio da trascrivere ([questa](https://www.radioradicale.it/scheda/17807/maxiprocesso-a-cosa-nostra), ad esempio, é la pagina web con la registrazione del Maxiprocesso a "Cosa nostra" eseguita in data 25 giugno 1986) e copiarne l'URL
2. aprire un terminale nella cartella "arre" ed eseguire il comando
   ```
   python download.py URL
   ```
   
   dove `URL` é l'URL copiato al passo 1, in questo caso `https://www.radioradicale.it/scheda/17807/maxiprocesso-a-cosa-nostra`

   > __NB:__ potrebbe essere necessario sostituire il comando `python` con `python3` o `py`

Questo comando creerà una cartella chiamata `data/TITOLO-DELLA-PAGINA` contente la traccia audio del processo in questione.

> __NB:__ poiché Radio Radicale non permette di scaricare direttamente i file audio piú vecchi di una certa data, questo comando riproduce e "registra" l'intera traccia audio. Di conseguenza, il processo richiede un tempo pari alla durata della traccia. Tuttavia, in questa fase non é necessario ascoltare l'intera traccia: abbassare o disattivare il volume non costituisce un problema.

### 2. Trascrivere una traccia audio
1. sempre tramite il terminale, spostarsi nella sottocartella di `data` con la registrazione che si vuole trascrivere. Il file con la traccia audio dovrebbe chiamarsi `audio.mp3`
2. eseguire il comando `python transcribe.py audio.mp3`. Il risultato sarà un file con estensione `.srt`, uno dei formati piú utilizzati per i sottotitoli dei film
3. aprire il file audio e il file coi sottotitoli in un programma apposito (vedi [Prerequisiti](#prerequisiti)) e correggere eventuali errori. Mano a mano, aggiungere eventuali parole non riconosciute (sigle, nomi propri, parole pronunciate in modo particolare ecc. al file [asr_prompt.txt](asr_prompt.txt), modificabile con qualsiasi editor di testo)
