import re
import sys

filename = sys.argv[1]
with open(filename) as file_:

  state = "null"
  current_speaker = None
  utterance = ""
  utterance_start = None
  utterance_start_time = None
  last_snippet_end_time = None

  for line in file_:

    line = line.strip()

    if re.match("^\d+$", line):
      state = "start-section"
      continue

    if state == "start-section":
      m = re.match(
        "^(\d{2}):(\d{2}):(\d{2})\.\d{3} --> (\d{2}):(\d{2}):(\d{2})\.\d{3}$", line
      )
      if m is not None:
        state = "at-utterance"
        utterance_start = f"{m.group(1)}:{m.group(2)}:{m.group(3)}"
        utterance_start_time = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        utterance_end_time = int(m.group(4)) * 3600 + int(m.group(5)) * 60 + int(m.group(6))
        continue

    if state == "at-utterance":
      m = re.match("^(.*?): (.*)$", line)
      if m is not None:
        speaker = m.group(1)
        if speaker == "Andrew Head":
          speaker = "Andrew"
        else:
          speaker = "Participant"
        said = m.group(2).strip()
      
        if speaker != current_speaker or utterance_start_time - last_utterance_end_time > 3:
          if not utterance.endswith("."):
            print(".", end="")
          utterance = ""
          if current_speaker is not None:
            print("\n")
          print(f"{speaker} ({utterance_start}):", end="")
          current_speaker = speaker

        if len(utterance) > 0 and not utterance.strip().endswith("."):
          said = said[0].lower() + said[1:]

        print(f" {said}", end="")
        
        utterance += " " + said
        last_utterance_end_time = utterance_end_time

