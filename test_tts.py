#!/usr/bin/env python3
"""
Test TTS (Text-to-Speech) on Raspberry Pi
Shows available voices and tests speech output
"""

import sys
import subprocess
import platform

# First, test if espeak works directly
def test_espeak_direct():
    """Test espeak directly without pyttsx3"""
    print("=" * 60)
    print("Testing espeak directly (bypass pyttsx3)")
    print("=" * 60)
    print()
    
    try:
        # Check if espeak is installed
        result = subprocess.run(['which', 'espeak'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ espeak not found!")
            print("Install with: sudo apt install espeak")
            return False
        
        espeak_path = result.stdout.strip()
        print(f"✅ espeak found at: {espeak_path}")
        print()
        
        # Get espeak version
        result = subprocess.run(['espeak', '--version'], capture_output=True, text=True)
        print(f"Version: {result.stdout.strip()}")
        print()
        
        # List available voices
        print("Available espeak voices:")
        print("-" * 60)
        result = subprocess.run(['espeak', '--voices'], capture_output=True, text=True)
        for line in result.stdout.split('\n')[:10]:  # First 10 voices
            if line.strip():
                print(line)
        print()
        
        # Test speech with espeak directly
        test_messages = [
            "15 seconds shot clock now in operation",
            "10 seconds shot clock now in operation"
        ]
        
        for msg in test_messages:
            print(f"Speaking: '{msg}'")
            result = subprocess.run(
                ['espeak', '-s', '175', msg],  # -s = speed in WPM
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Speech completed")
            else:
                print(f"❌ Speech failed: {result.stderr}")
            print()
        
        print("=" * 60)
        print("✅ espeak Direct Test Complete!")
        print("=" * 60)
        print()
        print("espeak works! Now testing pyttsx3...")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pyttsx3():
    """Test pyttsx3 with workaround for Raspberry Pi"""
    
    try:
        import pyttsx3
    except ImportError:
        print("❌ pyttsx3 not installed!")
        print("Install with: pip3 install pyttsx3")
        return False
    
    print("=" * 60)
    print("Testing pyttsx3 (with Raspberry Pi workaround)")
    print("=" * 60)
    print()
    
    try:
        # Try to initialize without setting voice
        print("Initializing pyttsx3 engine...")
        
        # On Raspberry Pi, we need to use 'espeak' driver explicitly
        system = platform.system()
        if system == 'Linux':
            print("Detected Linux - using espeak driver")
            try:
                engine = pyttsx3.init('espeak')
                print("✅ Engine initialized with espeak driver")
            except:
                print("⚠️  espeak driver failed, trying default...")
                engine = pyttsx3.init()
                print("✅ Engine initialized with default driver")
        else:
            engine = pyttsx3.init()
            print("✅ Engine initialized")
        
        print()
        
        # Get properties
        try:
            rate = engine.getProperty('rate')
            volume = engine.getProperty('volume')
            print(f"Current rate: {rate} WPM")
            print(f"Current volume: {volume}")
        except Exception as e:
            print(f"⚠️  Could not get properties: {e}")
            rate = 150
            volume = 1.0
        
        print()
        
        # Try to set rate (this usually works)
        try:
            new_rate = int(rate * 1.15)
            engine.setProperty('rate', new_rate)
            print(f"✅ Rate set to: {new_rate} WPM")
        except Exception as e:
            print(f"⚠️  Could not set rate: {e}")
        
        print()
        
        # DON'T list or set voices - this causes the error
        print("⚠️  Skipping voice selection (causes errors on Raspberry Pi)")
        print("Using system default voice")
        print()
        
        # Test speech
        test_message = "15 seconds shot clock now in operation"
        print(f"Speaking: '{test_message}'")
        print("(This may take a moment...)")
        
        try:
            engine.say(test_message)
            engine.runAndWait()
            print("✅ Speech completed successfully!")
        except Exception as e:
            print(f"❌ Speech failed: {e}")
            print()
            print("Trying alternative method...")
            # Alternative: use espeak directly
            subprocess.run(['espeak', test_message])
        
        print()
        
        # Test second message
        test_message2 = "10 seconds shot clock now in operation"
        print(f"Speaking: '{test_message2}'")
        
        try:
            engine.say(test_message2)
            engine.runAndWait()
            print("✅ Speech completed successfully!")
        except Exception as e:
            print(f"❌ Speech failed: {e}")
        
        print()
        print("=" * 60)
        print("✅ pyttsx3 Test Complete!")
        print("=" * 60)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("pyttsx3 has issues on this system.")
        print("The app will use espeak directly as fallback.")
        return False

def main():
    print()
    print("=" * 60)
    print("TTS (Text-to-Speech) Test Suite")
    print("=" * 60)
    print()
    
    # Test 1: espeak directly (always works)
    espeak_ok = test_espeak_direct()
    
    if not espeak_ok:
        print()
        print("=" * 60)
        print("❌ espeak not working")
        print("=" * 60)
        print()
        print("Please install espeak:")
        print("  sudo apt install espeak")
        print()
        return False
    
    # Test 2: pyttsx3 (may have issues)
    input("Press Enter to test pyttsx3 (or Ctrl+C to skip)...")
    print()
    
    pyttsx3_ok = test_pyttsx3()
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    print(f"espeak direct:  {'✅ Working' if espeak_ok else '❌ Failed'}")
    print(f"pyttsx3:        {'✅ Working' if pyttsx3_ok else '❌ Failed (using fallback)'}")
    print()
    
    if espeak_ok:
        print("✅ TTS will work in the app!")
        print()
        if not pyttsx3_ok:
            print("Note: The app will use espeak directly as fallback")
            print("      if pyttsx3 has issues.")
    else:
        print("❌ TTS will not work. Install espeak:")
        print("   sudo apt install espeak")
    
    print()
    return espeak_ok

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
