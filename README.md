# Youtube Audio Transcriber

**YT Audio Transcriber** is a straightforward command-line tool designed to bridge the gap in YouTube content where transcriptions are unavailable or when a user prefers a personalized transcription. 

- 📝 **Easy-to-Use**: Simply input a YouTube channel URL, and this tool will generate a .txt file with transcribed content from the channel's videos.

- 🔍 **Prioritized Content**: Videos are transcribed based on view count, ensuring you start with the most popular content first.
  
- 🤖 **Powered by OpenAI**: Built upon OpenAI's Whisper, the transcriptions offer high accuracy.

- 🛠️ **Installation**: Everything you need to get started is included in the `requirements.txt`. Install necessary dependencies with `pip install -r requirements.txt`.

- ⚙️ **Customizable CLI**: Input the desired title for the transcriptions and your OpenAI API key. For those who prefer, you can also hard-code your OpenAI API key or use an environment variable by making modifications in the main function.
