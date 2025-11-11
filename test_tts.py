#!/usr/bin/env python3
"""
Test TTS (Text-to-Speech) on Raspberry Pi
Shows available voices and tests speech output
"""

import sys

try:
    import pyttsx3
except ImportError:
    print("❌ pyttsx3 not installed!")
    print("Install with: pip3 install pyttsx3")
    sys.exit(1)

def test_tts():
    """Test TTS functionality and list available voices"""
    
    print("=" * 60)
    print("TTS (Text-to-Speech) Test")
    print("=" * 60)
    print()
    
    try:
        # Initialize TTS engine
        print("Initializing TTS engine...")
        engine = pyttsx3.init()
        print("✅ TTS engine initialized")
        print()
        
        # Get current properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        
        print("Current Settings:")
        print("-" * 60)
        print(f"Rate (WPM): {rate}")
        print(f"Volume: {volume}")
        print()
        
        # List available voices
        voices = engine.getProperty('voices')
        print(f"Available Voices ({len(voices)}):")
        print("-" * 60)
        
        for i, voice in enumerate(voices, 1):
            print(f"{i}. {voice.name}")
            print(f"   ID: {voice.id}")
            if hasattr(voice, 'languages'):
                print(f"   Languages: {voice.languages}")
            if hasattr(voice, 'gender'):
                print(f"   Gender: {voice.gender}")
            print()
        
        # Test speech
        print("=" * 60)
        print("Speech Test")
        print("=" * 60)
        print()
        
        test_message = "15 seconds shot clock now in operation"
        
        print(f"Testing with first voice: {voices[0].name}")
        print(f"Message: '{test_message}'")
        print()
        
        engine.setProperty('voice', voices[0].id)
        
        # Increase rate by 15%
        new_rate = int(rate * 1.15)
        engine.setProperty('rate', new_rate)
        print(f"Using rate: {new_rate} WPM (original: {rate})")
        print()
        
        print("Speaking... (listen for audio)")
        engine.say(test_message)
        engine.runAndWait()
        print("✅ Speech completed")
        print()
        
        # Test second message
        test_message2 = "10 seconds shot clock now in operation"
        print(f"Testing second message: '{test_message2}'")
        print("Speaking...")
        engine.say(test_message2)
        engine.runAndWait()
        print("✅ Speech completed")
        print()
        
        print("=" * 60)
        print("✅ TTS Test Complete!")
        print("=" * 60)
        print()
        print("If you heard the messages, TTS is working correctly.")
        print("If not, check:")
        print("  1. Audio output is enabled (speaker-test -t wav -c 2)")
        print("  2. Volume is turned up")
        print("  3. espeak is installed (sudo apt install espeak)")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Install espeak: sudo apt install espeak")
        print("  2. Install pyttsx3: pip3 install pyttsx3")
        print("  3. Test audio: speaker-test -t wav -c 2")
        return False

if __name__ == "__main__":
    success = test_tts()
    sys.exit(0 if success else 1)
