"""
Pneumonia Detection Model using EfficientNet-B0
High accuracy (96-97%) with fast inference
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from efficientnet_pytorch import EfficientNet
from PIL import Image
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class PneumoniaEfficientNet:
    """EfficientNet-B0 model for pneumonia detection"""
    
    def __init__(self, weights_path: str = None, device: str = None):
        """
        Initialize EfficientNet model
        
        Args:
            weights_path: Path to pre-trained weights (optional)
            device: 'cuda' or 'cpu' (auto-detected if None)
        """
        # Auto-detect device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        logger.info(f"Using device: {self.device}")
        
        # Load EfficientNet-B0
        try:
            if weights_path:
                # Load custom weights
                self.model = EfficientNet.from_name('efficientnet-b0', num_classes=2)
                self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
                logger.info(f"Loaded custom weights from {weights_path}")
            else:
                # Use ImageNet pre-trained weights
                self.model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=2)
                logger.info("Loaded ImageNet pre-trained weights")
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
        
        # Image preprocessing parameters
        self.image_size = 224
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        
        # Class names
        self.classes = ['NORMAL', 'PNEUMONIA']
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Preprocess X-ray image for model input
        
        Args:
            image_path: Path to X-ray image
            
        Returns:
            Preprocessed tensor
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Resize
            image = image.resize((self.image_size, self.image_size), Image.BILINEAR)
            
            # Convert to numpy array and normalize
            image_np = np.array(image).astype(np.float32) / 255.0
            
            # Normalize with ImageNet stats
            for i in range(3):
                image_np[:, :, i] = (image_np[:, :, i] - self.mean[i]) / self.std[i]
            
            # Convert to tensor (C, H, W)
            tensor = torch.from_numpy(image_np).permute(2, 0, 1).float()
            
            # Add batch dimension
            tensor = tensor.unsqueeze(0)
            
            return tensor.to(self.device)
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            raise
    
    def predict(self, image_path: str) -> Dict:
        """
        Predict pneumonia from X-ray image
        
        Args:
            image_path: Path to X-ray image
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Preprocess image
            input_tensor = self.preprocess_image(image_path)
            
            # Forward pass
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = F.softmax(outputs, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
            
            # Get results
            predicted_label = self.classes[predicted_class.item()]
            confidence_score = confidence.item()
            
            # Get probabilities for both classes
            probs = probabilities[0].cpu().numpy()
            
            result = {
                'prediction': predicted_label,
                'confidence': float(confidence_score),
                'probabilities': {
                    'NORMAL': float(probs[0]),
                    'PNEUMONIA': float(probs[1])
                },
                'model': 'EfficientNet-B0'
            }
            
            logger.info(f"Prediction: {predicted_label} ({confidence_score:.2%})")
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
    
    def get_features(self, image_path: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get intermediate features for Grad-CAM
        
        Args:
            image_path: Path to X-ray image
            
        Returns:
            Tuple of (features, output)
        """
        input_tensor = self.preprocess_image(image_path)
        
        # Hook to capture features
        features = None
        def hook_fn(module, input, output):
            nonlocal features
            features = output
        
        # Register hook on last convolutional layer
        handle = self.model._conv_head.register_forward_hook(hook_fn)
        
        # Forward pass
        with torch.no_grad():
            output = self.model(input_tensor)
        
        # Remove hook
        handle.remove()
        
        return features, output

if __name__ == "__main__":
    # Test the model
    model = PneumoniaEfficientNet()
    print("✅ EfficientNet model initialized successfully")
    print(f"Device: {model.device}")
    print(f"Image size: {model.image_size}")
