from django.shortcuts import render
from django.http import HttpResponse
from summarizer.utils.youtube_transcript_extractor import extract_video_id, get_youtube_transcript
from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize the BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

def index(request):
    return render(request, 'summarizer/index.html')

def summarize_text(text):
    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def get_summary(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        
        try:
            video_id = extract_video_id(youtube_url)

            # Get the transcript of the video
            transcript = get_youtube_transcript(youtube_url)
            summary = summarize_text(transcript)
            context = {
                'video_id': video_id,
                'summary': summary,
            }

            return render(request, 'summarizer/output.html',context)

        except ValueError as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    return HttpResponse(status=405)

    # https://youtu.be/dBVIlxbyBLk?si=sbKdqt_-EDilizcr