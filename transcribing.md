# Transcribing trials
If you're reading this, you've probably already [installed Arré](https://github.com/harisont/arre#setup), [downloaded one or more audio recordings](https://github.com/harisont/arre#downloading-audio-recordings), [converted them to WAV](https://github.com/harisont/arre#converting-mp3s-to-wav), [isolated their speech segments](https://github.com/harisont/arre#segmenting-audio-files) and [launched the transcription program](https://github.com/harisont/arre#transcribing). 

It's now time to collaborate with the system and produce a high-quality transcription of your audio recording.

The process is interactive and goes on one segment at a time, ensuring relatively short waits and allowing the user to work in a bite-sized fashion.

Running [`transcribe.py`](transcribe.py) causes the audio player and text editor of choice to be launched on a specific speech segment.

The audio player loops over the segment, and the text editor shows an editable transcription hypothesis. See the [guidelines for editing automatic transcriptions](#guidelines-for-editing-automatic-transcriptions) below.

Once you are done editing the segment, save close both the editor and the audio player. The text will be saved to a _segment file_ named `START-STOP.txt` (`START` and `STOP` being the segment's start and end time of the segment) and the program will continue processing the following segment, launching the editor and the audio player again for you. __Never edit the name of a segment file__, as this affects PDF generation.

If you want to take a break and continue transcribing another day, complete the current fragment. Next time, the program will start from the first unprocessed segment. 

You can always go back to a segment file later (to play a specific segment, you can run `python play WAV_PATH START END`), but it is recommended that you do all major changes during an interactive session.

## Guidelines for editing automatic transcriptions
When editing an automatic transcription, you should of course add/replace any missing/incorrect words.

### Replacements
If you notice that a word that is likely to reoccur, for example a surname like "D'Amico", is consistently wrongly transcribed, e.g. as "l'amico", you can mark it as a "preventable error". 
If you want to do so, instead of replacing it, add the correction preceded by a `>` in square brackets, as in the example below.
In this way, the correction will be used as a suggestion to the human transcriber whenever the sequence "l'amico" occurs again. Unfortunately, Google Speech Recognition itself cannot be informed that "D'Amico" is a preferred keyword and retraining the model to make it actually learn from past mistakes is absolutely unfeasible.

#### Example
Text before manual editing:

```
L'avvocato l'amico sostiene che...
```

Text after manual editing:

```
L'avvocato [l'amico>D'Amico] sostiene che...
```

Automatic transcription of the next occurrence of "l'amico" before manual editing:

```
Inoltre, [l'amico|D'Amico] ha riferito che [l'amico|D'amico] dell'imputato...
```

After manual editing:

```
Inoltre, D'Amico ha riferito che l'amico dell'imputato...
```

### Speakers
On top of this, whenever there is a change of speaker, you should mark it by writing their name, preceeded by a `#` sign, in the preceeding (otherwise empty) line as in the following example:

```
#Presidente
Avvocato, c'é una differenza...

#Avv. D'Amico
In effetti nel volume 40 dell'ordinanza si riportano tutti e due i reati.
```