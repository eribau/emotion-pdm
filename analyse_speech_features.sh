#!/bin/bash

# Loop over all wav files in the emotional speech dataset
for filename in berlin_database_of_emotional_speech/wav/*.wav; do
	file=$(basename -- $filename)
	emotion=${file:5:1}

	if [ "$emotion" = "W" ]; then
		output=anger
	elif [ "$emotion" = "L" ]; then
		output=boredom
	elif [ "$emotion" = "E" ]; then
		output=disgust
	elif [ "$emotion" = "A" ]; then
		output=anxiety
	elif [ "$emotion" = "F" ]; then
		output=happiness
	elif [ "$emotion" = "T" ]; then
		output=sadness
	elif [ "$emotion" = "N" ]; then
		output=neutral
	else
		output=unkown
	fi

	#	echo $emotion
	# extract features from the file
	if [ "$output" != "unknown" ]; then
		SMILExtract -C config/emo_feature_extraction.conf -I berlin_database_of_emotional_speech/wav/$filename -O emotion_analysis/$output.csv
	fi
done
