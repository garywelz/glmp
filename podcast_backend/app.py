#!/usr/bin/env python3
"""
Podcast Generation Backend - Cloud Run Service
Fixes all known issues: filename numbering, multi-voice, duration, logging
"""

import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from google.cloud import storage, texttospeech
import openai
import uuid
import re
from io import BytesIO
import requests
from pydub import AudioSegment
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT', 'regal-scholar-453620-r7')

# Initialize clients
storage_client = storage.Client()
tts_client = texttospeech.TextToSpeechClient()
openai.api_key = OPENAI_API_KEY

class PodcastGenerator:
    """Main podcast generation class with comprehensive error handling and logging"""
    
    def __init__(self):
        self.bucket = storage_client.bucket(BUCKET_NAME)
        self.voice_configs = {
            'narrator': {
                'language_code': 'en-US',
                'name': 'en-US-Journey-D',  # Deep, authoritative voice
                'ssml_gender': texttospeech.SsmlVoiceGender.MALE
            },
            'interviewer': {
                'language_code': 'en-US', 
                'name': 'en-US-Journey-F',  # Warm, engaging voice
                'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE
            },
            'expert1': {
                'language_code': 'en-US',
                'name': 'en-US-Studio-O',  # Professional, clear voice
                'ssml_gender': texttospeech.SsmlVoiceGender.MALE
            },
            'expert2': {
                'language_code': 'en-US',
                'name': 'en-US-Studio-Q',  # Thoughtful, analytical voice
                'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE
            }
        }
    
    def get_next_filename(self, category: str) -> str:
        """Generate next incremental filename with proper numbering"""
        logger.info(f"Generating next filename for category: {category}")
        
        # Category abbreviations
        category_abbrev = {
            'Biology': 'bio',
            'Chemistry': 'chem', 
            'Computer Science': 'compsci',
            'Mathematics': 'math',
            'Physics': 'phys'
        }
        
        abbrev = category_abbrev.get(category, 'misc')
        prefix = f"ever-{abbrev}-"
        
        try:
            # List all files with this prefix to find the highest number
            blobs = list(self.bucket.list_blobs(prefix=f"podcasts/{prefix}"))
            
            max_number = 250000  # Starting number
            for blob in blobs:
                filename = blob.name.split('/')[-1]  # Get just the filename
                if filename.startswith(prefix):
                    # Extract number from filename like "ever-math-250034.mp3"
                    match = re.search(rf"{prefix}(\d+)", filename)
                    if match:
                        number = int(match.group(1))
                        max_number = max(max_number, number)
            
            next_number = max_number + 1
            filename = f"{prefix}{next_number:06d}"
            
            logger.info(f"Generated filename: {filename} (previous max: {max_number})")
            return filename
            
        except Exception as e:
            logger.error(f"Error generating filename: {e}")
            # Fallback to timestamp-based naming
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{prefix}{timestamp}"
    
    def generate_content(self, subject: str, duration: int, speakers: str, 
                        difficulty: str, source_links: List[str], 
                        additional_notes: str) -> Dict[str, Any]:
        """Generate podcast content with proper duration targeting"""
        logger.info(f"Generating content for subject: {subject}, duration: {duration}min, speakers: {speakers}")
        
        # Calculate target word count based on duration
        # Average speaking rate: 150-160 words per minute
        # Multiple speakers = slower pace due to conversation
        words_per_minute = 140 if speakers in ['interview', 'panel', 'debate'] else 160
        target_words = duration * words_per_minute
        
        logger.info(f"Target word count: {target_words} words for {duration} minutes")
        
        # Build comprehensive prompt
        source_context = ""
        if source_links:
            source_context = f"\n\nReference these specific sources:\n" + "\n".join(f"- {link}" for link in source_links)
        
        additional_context = f"\n\nAdditional instructions: {additional_notes}" if additional_notes else ""
        
        # Speaker-specific prompts
        speaker_prompts = {
            'single': f"""Create a {duration}-minute single-narrator podcast script about "{subject}" 
                         for {difficulty.lower()} level audience. Target approximately {target_words} words.
                         
                         Format as a natural, engaging monologue with:
                         - Clear introduction and conclusion
                         - Logical flow between concepts
                         - Appropriate pacing for the duration
                         - Examples and analogies for clarity
                         
                         Return as plain text suitable for text-to-speech.{source_context}{additional_context}""",
            
            'interview': f"""Create a {duration}-minute interview-style podcast script about "{subject}"
                           for {difficulty.lower()} level audience. Target approximately {target_words} words.
                           
                           Format as a conversation between:
                           INTERVIEWER: (asks questions, guides discussion)
                           EXPERT: (provides detailed answers and insights)
                           
                           Include:
                           - Natural conversation flow
                           - Follow-up questions
                           - Clear speaker transitions
                           - Engaging dialogue
                           
                           Format each line as:
                           INTERVIEWER: [text]
                           EXPERT: [text]{source_context}{additional_context}""",
            
            'panel': f"""Create a {duration}-minute panel discussion script about "{subject}"
                       for {difficulty.lower()} level audience. Target approximately {target_words} words.
                       
                       Format as a discussion between:
                       MODERATOR: (guides discussion, asks questions)
                       EXPERT1: (provides one perspective)
                       EXPERT2: (provides alternative viewpoint)
                       
                       Include natural debate and interaction between experts.
                       
                       Format each line as:
                       MODERATOR: [text]
                       EXPERT1: [text]
                       EXPERT2: [text]{source_context}{additional_context}""",
            
            'debate': f"""Create a {duration}-minute debate-style podcast script about "{subject}"
                        for {difficulty.lower()} level audience. Target approximately {target_words} words.
                        
                        Format as a structured debate between:
                        MODERATOR: (introduces topic, asks questions)
                        EXPERT1: (argues one position)
                        EXPERT2: (argues opposing position)
                        
                        Include back-and-forth arguments and rebuttals.
                        
                        Format each line as:
                        MODERATOR: [text]
                        EXPERT1: [text]
                        EXPERT2: [text]{source_context}{additional_context}"""
        }
        
        try:
            # Generate content using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert podcast script writer. Create engaging, informative content that flows naturally when spoken aloud."},
                    {"role": "user", "content": speaker_prompts[speakers]}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            script = response.choices[0].message.content
            word_count = len(script.split())
            
            logger.info(f"Generated script: {word_count} words (target: {target_words})")
            
            # Parse script into segments by speaker
            segments = self._parse_script_segments(script, speakers)
            
            return {
                'script': script,
                'segments': segments,
                'word_count': word_count,
                'target_words': target_words,
                'speakers': speakers
            }
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def _parse_script_segments(self, script: str, speakers: str) -> List[Dict[str, str]]:
        """Parse script into speaker segments"""
        segments = []
        
        if speakers == 'single':
            segments.append({
                'speaker': 'narrator',
                'text': script.strip()
            })
        else:
            # Parse multi-speaker format
            lines = script.strip().split('\n')
            current_speaker = None
            current_text = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Check for speaker labels
                speaker_match = re.match(r'^(INTERVIEWER|EXPERT|EXPERT1|EXPERT2|MODERATOR|NARRATOR):\s*(.*)', line, re.IGNORECASE)
                
                if speaker_match:
                    # Save previous segment
                    if current_speaker and current_text:
                        segments.append({
                            'speaker': current_speaker.lower(),
                            'text': ' '.join(current_text).strip()
                        })
                    
                    # Start new segment
                    current_speaker = speaker_match.group(1).lower()
                    current_text = [speaker_match.group(2)] if speaker_match.group(2) else []
                else:
                    # Continue current speaker's text
                    if current_speaker:
                        current_text.append(line)
            
            # Add final segment
            if current_speaker and current_text:
                segments.append({
                    'speaker': current_speaker.lower(),
                    'text': ' '.join(current_text).strip()
                })
        
        logger.info(f"Parsed {len(segments)} segments from script")
        return segments
    
    def generate_audio(self, segments: List[Dict[str, str]]) -> bytes:
        """Generate multi-voice audio with proper voice assignments"""
        logger.info(f"Generating audio for {len(segments)} segments")
        
        audio_segments = []
        
        for i, segment in enumerate(segments):
            speaker = segment['speaker']
            text = segment['text']
            
            # Map speakers to voice configurations
            voice_mapping = {
                'narrator': 'narrator',
                'interviewer': 'interviewer', 
                'expert': 'expert1',
                'expert1': 'expert1',
                'expert2': 'expert2',
                'moderator': 'interviewer'  # Use interviewer voice for moderator
            }
            
            voice_key = voice_mapping.get(speaker, 'narrator')
            voice_config = self.voice_configs[voice_key]
            
            logger.info(f"Segment {i+1}: {speaker} -> {voice_key} voice ({voice_config['name']})")
            
            try:
                # Prepare TTS request
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=voice_config['language_code'],
                    name=voice_config['name'],
                    ssml_gender=voice_config['ssml_gender']
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=0.95,  # Slightly slower for clarity
                    pitch=0.0
                )
                
                # Generate audio
                response = tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                
                # Convert to AudioSegment
                audio_segment = AudioSegment.from_mp3(BytesIO(response.audio_content))
                
                # Add pause between speakers (except for first segment)
                if i > 0:
                    pause = AudioSegment.silent(duration=800)  # 0.8 second pause
                    audio_segments.append(pause)
                
                audio_segments.append(audio_segment)
                
                logger.info(f"Generated audio for segment {i+1}: {len(audio_segment)}ms")
                
            except Exception as e:
                logger.error(f"Error generating audio for segment {i+1}: {e}")
                raise
        
        # Combine all audio segments
        if not audio_segments:
            raise ValueError("No audio segments generated")
        
        final_audio = audio_segments[0]
        for segment in audio_segments[1:]:
            final_audio += segment
        
        # Export as MP3
        mp3_buffer = BytesIO()
        final_audio.export(mp3_buffer, format="mp3", bitrate="128k")
        mp3_data = mp3_buffer.getvalue()
        
        duration_minutes = len(final_audio) / (1000 * 60)  # Convert ms to minutes
        logger.info(f"Final audio: {duration_minutes:.1f} minutes, {len(mp3_data)} bytes")
        
        return mp3_data
    
    def upload_to_storage(self, filename: str, audio_data: bytes, metadata: Dict[str, Any]) -> str:
        """Upload podcast to Google Cloud Storage with metadata"""
        logger.info(f"Uploading podcast: {filename}")
        
        # Audio file path
        audio_path = f"podcasts/{filename}.mp3"
        audio_blob = self.bucket.blob(audio_path)
        
        # Set metadata
        audio_blob.metadata = {
            'subject': metadata['subject'],
            'category': metadata['category'],
            'duration_minutes': str(metadata.get('duration_minutes', 0)),
            'speakers': metadata['speakers'],
            'difficulty': metadata['difficulty'],
            'generated_at': datetime.utcnow().isoformat(),
            'word_count': str(metadata.get('word_count', 0))
        }
        
        # Upload audio
        audio_blob.upload_from_string(audio_data, content_type='audio/mpeg')
        audio_blob.make_public()
        
        # Create metadata file
        metadata_path = f"podcasts/{filename}_metadata.json"
        metadata_blob = self.bucket.blob(metadata_path)
        metadata_blob.upload_from_string(
            json.dumps(metadata, indent=2),
            content_type='application/json'
        )
        
        audio_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{audio_path}"
        logger.info(f"Uploaded successfully: {audio_url}")
        
        return audio_url

    def generate_podcast(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main podcast generation method"""
        job_id = str(uuid.uuid4())
        logger.info(f"Starting podcast generation - Job ID: {job_id}")
        logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
        
        try:
            # Extract parameters
            subject = request_data['subject']
            category = request_data['category']
            duration = int(request_data['duration'])
            speakers = request_data['speakers']
            difficulty = request_data['difficulty']
            source_links = request_data.get('source_links', [])
            additional_notes = request_data.get('additional_notes', '')
            
            # Generate filename FIRST
            filename = self.get_next_filename(category)
            logger.info(f"Generated filename: {filename}")
            
            # Generate content
            content_result = self.generate_content(
                subject, duration, speakers, difficulty, 
                source_links, additional_notes
            )
            
            # Generate audio with multiple voices
            audio_data = self.generate_audio(content_result['segments'])
            
            # Prepare metadata
            metadata = {
                'job_id': job_id,
                'filename': filename,
                'subject': subject,
                'category': category,
                'duration_requested': duration,
                'duration_minutes': len(audio_data) / (1000 * 60 * 128 * 1024 / 8),  # Rough estimate
                'speakers': speakers,
                'difficulty': difficulty,
                'source_links': source_links,
                'additional_notes': additional_notes,
                'word_count': content_result['word_count'],
                'segments_count': len(content_result['segments']),
                'generated_at': datetime.utcnow().isoformat()
            }
            
            # Upload to storage
            audio_url = self.upload_to_storage(filename, audio_data, metadata)
            
            logger.info(f"Podcast generation completed successfully - Job ID: {job_id}")
            
            return {
                'success': True,
                'job_id': job_id,
                'filename': filename,
                'audio_url': audio_url,
                'metadata': metadata,
                'message': f"Podcast '{filename}' generated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error in podcast generation - Job ID: {job_id}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/generate-podcast', methods=['POST'])
def generate_podcast():
    """Main podcast generation endpoint"""
    logger.info("Received podcast generation request")
    
    try:
        # Get request data
        request_data = request.get_json()
        if not request_data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['subject', 'category', 'duration', 'speakers', 'difficulty']
        missing_fields = [field for field in required_fields if not request_data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Initialize generator and create podcast
        generator = PodcastGenerator()
        result = generator.generate_podcast(request_data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in generate_podcast endpoint: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'message': 'Internal server error during podcast generation'
        }), 500

@app.route('/generate-legacy-podcast', methods=['POST'])
def generate_legacy_podcast():
    """Legacy endpoint - redirects to main endpoint"""
    logger.warning("Legacy endpoint called - redirecting to main endpoint")
    return generate_podcast()

@app.route('/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get status of a podcast generation job"""
    try:
        # Check if metadata file exists
        metadata_blobs = list(self.bucket.list_blobs(prefix=f"podcasts/"))
        
        for blob in metadata_blobs:
            if blob.name.endswith('_metadata.json'):
                metadata_content = blob.download_as_text()
                metadata = json.loads(metadata_content)
                
                if metadata.get('job_id') == job_id:
                    return jsonify({
                        'job_id': job_id,
                        'status': 'completed',
                        'result': metadata
                    })
        
        return jsonify({
            'job_id': job_id,
            'status': 'not_found',
            'message': 'Job not found'
        }), 404
        
    except Exception as e:
        logger.error(f"Error checking job status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/list-podcasts', methods=['GET'])
def list_podcasts():
    """List all generated podcasts"""
    try:
        podcasts = []
        blobs = list(storage_client.bucket(BUCKET_NAME).list_blobs(prefix="podcasts/"))
        
        for blob in blobs:
            if blob.name.endswith('.mp3'):
                filename = blob.name.split('/')[-1].replace('.mp3', '')
                
                # Try to get metadata
                metadata_path = f"podcasts/{filename}_metadata.json"
                try:
                    metadata_blob = storage_client.bucket(BUCKET_NAME).blob(metadata_path)
                    metadata_content = metadata_blob.download_as_text()
                    metadata = json.loads(metadata_content)
                except:
                    metadata = {'filename': filename}
                
                podcasts.append({
                    'filename': filename,
                    'url': f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}",
                    'size': blob.size,
                    'created': blob.time_created.isoformat() if blob.time_created else None,
                    'metadata': metadata
                })
        
        return jsonify({
            'podcasts': sorted(podcasts, key=lambda x: x.get('created', ''), reverse=True),
            'count': len(podcasts)
        })
        
    except Exception as e:
        logger.error(f"Error listing podcasts: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)