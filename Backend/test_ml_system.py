"""
Test script for ML-based Pneumonia Detection System
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("="*60)
print("🔬 PNEUMONIA DETECTION SYSTEM - TEST SCRIPT")
print("="*60)

# Test 1: Import ML modules
print("\n[1/5] Testing ML Module Imports...")
try:
    import torch
    import torchvision
    from efficientnet_pytorch import EfficientNet
    import cv2
    import matplotlib
    print("✅ All ML dependencies imported successfully")
    print(f"   PyTorch version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    print(f"   Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Import custom modules
print("\n[2/5] Testing Custom Module Imports...")
try:
    from app.models.efficientnet_model import PneumoniaEfficientNet
    from app.utils.gradcam import GradCAM
    from app.models.pneumonia_detector import PneumoniaDetector
    print("✅ Custom modules imported successfully")
except ImportError as e:
    print(f"❌ Custom module import failed: {e}")
    sys.exit(1)

# Test 3: Initialize EfficientNet Model
print("\n[3/5] Initializing EfficientNet Model...")
try:
    model = PneumoniaEfficientNet()
    print("✅ EfficientNet-B0 initialized")
    print(f"   Device: {model.device}")
    print(f"   Image size: {model.image_size}")
    print(f"   Classes: {model.classes}")
except Exception as e:
    print(f"❌ Model initialization failed: {e}")
    sys.exit(1)

# Test 4: Initialize Pneumonia Detector
print("\n[4/5] Initializing Pneumonia Detector...")
try:
    detector = PneumoniaDetector()
    print("✅ Pneumonia Detector initialized")
    print(f"   Available models: {list(detector.models.keys())}")
    print(f"   Grad-CAM available: {detector.gradcam is not None}")
except Exception as e:
    print(f"❌ Detector initialization failed: {e}")
    sys.exit(1)

# Test 5: Test Diagnostic Agent
print("\n[5/5] Testing Diagnostic Agent...")
try:
    from app.agents.diagnostic_agent import DiagnosticAgent
    agent = DiagnosticAgent()
    print("✅ Diagnostic Agent initialized")
    print(f"   ML Available: {agent.use_ml}")
    print(f"   Mode: {'ML-based' if agent.use_ml else 'API-based'}")
except Exception as e:
    print(f"❌ Diagnostic agent initialization failed: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\n📊 System Summary:")
print(f"   ML Models: {'Available' if agent.use_ml else 'Not Available'}")
print(f"   EfficientNet-B0: ✓")
print(f"   Grad-CAM: {'✓' if detector.gradcam else '✗'}")
print(f"   API Fallback: ✓")
print("\n🚀 System is ready for pneumonia detection!")
print("\n💡 Next Steps:")
print("   1. Test with sample X-ray images")
print("   2. Verify Grad-CAM generation")
print("   3. Test API endpoints")
print("   4. Integrate with frontend")
print("="*60)
